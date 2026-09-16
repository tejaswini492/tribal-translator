# translate.py  (deployment version — uses Hugging Face's API)
#
# This version sends your Hindi sentence to Hugging Face's servers
# instead of running the AI model locally. This keeps our own app
# small and lightweight, which is REQUIRED for free hosting (Render's
# free tier only gives 512MB of memory — nowhere near enough to hold
# the full model, but plenty for just sending a web request).

import os
import time
from huggingface_hub import InferenceClient

# We read the token from an environment variable — never hard-code
# it here. Locally, you set this with "set HF_TOKEN=..." (Windows).
# On Render, you'll set this in their dashboard as a "Secret" instead.
HF_TOKEN = os.environ.get("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)

MODEL_NAME = "facebook/nllb-200-distilled-600M"
SRC_LANG = "hin_Deva"   # Hindi, Devanagari script
TGT_LANG = "sat_Beng"   # Santali, Bengali script


def translate_hindi_to_santali(hindi_text: str) -> str:
    """
    Sends one Hindi sentence to Hugging Face's hosted model and
    returns the Santali translation. Retries a few times if the
    model is still "waking up" on their end (normal for free tier).
    """
    if not hindi_text or not hindi_text.strip():
        return ""

    max_attempts = 4
    wait_seconds = 8

    for attempt in range(1, max_attempts + 1):
        try:
            result = client.translation(
                text=hindi_text,
                model=MODEL_NAME,
                src_lang=SRC_LANG,
                tgt_lang=TGT_LANG,
            )
            return getattr(result, "translation_text", result)
        except Exception as error:
            print(f"Attempt {attempt} failed: {error}")
            if attempt < max_attempts:
                time.sleep(wait_seconds)
            else:
                return "(translation temporarily unavailable — please try again)"


if __name__ == "__main__":
    if not HF_TOKEN:
        print("WARNING: HF_TOKEN is not set!")
    test_sentence = "आज हम गिनती सीखेंगे।"
    print("Hindi:  ", test_sentence)
    print("Santali:", translate_hindi_to_santali(test_sentence))
