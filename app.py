# app.py
#
# This file starts a small local website (using Flask) so you can
# use the translator from a browser instead of the terminal.
#
# Flow:
#   Browser (index.html) --> sends Hindi text --> app.py --> translate.py
#   translate.py returns Santali text --> app.py --> back to browser

from flask import Flask, render_template, request, jsonify, send_file
from translate import translate_hindi_to_santali
from worksheet import generate_worksheet, load_topics
from explain import get_word_breakdown, get_plain_explanation

app = Flask(__name__)


@app.route("/")
def home():
    # Shows the webpage in templates/index.html
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate_route():
    # The browser sends JSON like: {"text": "आज हम गिनती सीखेंगे।"}
    data = request.get_json()
    hindi_text = data.get("text", "")

    santali_text = translate_hindi_to_santali(hindi_text)
    word_breakdown = get_word_breakdown(hindi_text)
    explanation = get_plain_explanation(hindi_text)

    # Send everything back to the browser as JSON
    return jsonify({
        "santali": santali_text,
        "breakdown": word_breakdown,
        "explanation": explanation,
    })


@app.route("/download-worksheet")
def download_worksheet():
    # Build the PDF fresh each time the button is clicked
    # (unchanged - still generates the same fixed 3-topic worksheet
    # it always did, since generate_worksheet defaults to those
    # topics when topic_keys isn't given)
    output_path = "sample_worksheet.pdf"
    generate_worksheet(output_path)
    return send_file(output_path, as_attachment=True)


# ---------------------------------------------------------------
# NEW: topic-picker worksheet feature.
# These are additions only - nothing above this line was changed.
# ---------------------------------------------------------------

@app.route("/topics", methods=["GET"])
def get_topics():
    # Returns the list of available topics (key + title) so the
    # webpage can show them in a dropdown for the teacher to pick from.
    topics = load_topics()
    return jsonify([{"key": k, "title": v["title"]} for k, v in topics.items()])


@app.route("/generate-worksheet", methods=["POST"])
def generate_worksheet_route():
    # The browser sends JSON like: {"topics": ["numbers", "animals"]}
    data = request.get_json()
    selected_keys = data.get("topics", [])
    if not selected_keys:
        return jsonify({"error": "No topics selected"}), 400

    output_path = "generated_worksheet.pdf"
    generate_worksheet(output_path, selected_keys)
    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    # debug=False and use_reloader=False: we turn these off on purpose.
    # Debug mode normally loads the app twice (for auto-reloading when
    # you edit code), which loads our big AI model into memory twice —
    # that can crash on computers with limited RAM. We don't need
    # auto-reload for a prototype, so we keep it simple and load once.
    app.run(debug=False, use_reloader=False, port=5000)
