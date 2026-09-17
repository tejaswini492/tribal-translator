prototype link
https://tribal-translator.onrender.com/

# Hindi → Santali Classroom Translator (Prototype)

Uses Meta's already-trained NLLB-200 translation model — no training required.

## What each file does
- `translate.py` — loads the pretrained AI model, has one function: Hindi text in, Santali text out
- `app.py` — a tiny local web server (Flask) that connects the webpage to `translate.py`
- `templates/index.html` — the webpage: type or speak Hindi, see Santali on screen
- `requirements.txt` — list of Python packages this needs

## Step-by-step setup

### 1. Install Python (if you don't have it)
Download from https://python.org (get 3.10 or 3.11). During install, check "Add Python to PATH".
Check it worked by opening a terminal / command prompt and typing:
```
python --version
```

### 2. Put these files in a folder
Keep the folder structure exactly as given:
```
tribal-translator/
  app.py
  translate.py
  requirements.txt
  templates/
    index.html
```

### 3. Open a terminal in that folder
Windows: open the folder, click the address bar, type `cmd`, press Enter.
Mac/Linux: right-click the folder → "Open Terminal here" (or `cd` into it).

### 4. Create a virtual environment (keeps this project's packages separate)
```
python -m venv venv
```
Activate it:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`
You'll see `(venv)` appear in your terminal — that means it worked.

### 5. Install the required packages
```
pip install -r requirements.txt
```
This installs Flask (the web server) and Transformers + PyTorch (the AI library that runs the pretrained model). This step can take a few minutes.

### 6. Test the translation function by itself (optional but recommended first)
```
python translate.py
```
First run will download the model (~600MB, one-time, needs internet). You should see a Hindi test sentence and its Santali translation printed.

### 7. Run the full web app
```
python app.py
```
You'll see something like `Running on http://127.0.0.1:5000`.

### 8. Open it in your browser
Go to: `http://127.0.0.1:5000`
- Type a Hindi sentence and click "Translate", OR
- Click "🎤 Speak Hindi" (Chrome only) and say a sentence — it fills in and translates automatically.


<img width="1920" height="1080" alt="Screenshot (61)" src="https://github.com/user-attachments/assets/d2044de4-f433-4438-b0cd-28752de5531f" />
