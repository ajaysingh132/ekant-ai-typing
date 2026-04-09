from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pytesseract
from PIL import Image
import io

app = FastAPI()

# Home
@app.get("/")
def home():
    return {"message": "Ekant AI Typing Running 🚀"}

# OCR API
@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # OCR (English + Hindi)
    text = pytesseract.image_to_string(image, lang='eng')

    return {"text": text}


# UI
@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI Typing System</title>
<style>
body { font-family: Arial; padding:20px; background:#f5f5f5; }
.container { max-width:600px; margin:auto; background:white; padding:20px; border-radius:10px; }
button { padding:10px; margin-top:10px; }
</style>
</head>
<body>

<div class="container">
<h1>🚀 AI Typing System</h1>

<h2>🎤 Voice Typing</h2>
<button onclick="start()">Start Speaking</button>
<p id="voice_output"></p>

<h2>📸 OCR (Photo / Handwriting)</h2>
<input type="file" id="file">
<br>
<button onclick="upload()">Convert</button>
<p id="ocr_output"></p>

</div>

<script>
// Voice
function start() {
    const r = new webkitSpeechRecognition();
    r.lang = "hi-IN";

    r.onresult = e => {
        document.getElementById("voice_output").innerText =
        e.results[0][0].transcript;
    };

    r.start();
}

// OCR
async function upload() {
    let fileInput = document.getElementById("file");
    let file = fileInput.files[0];

    let formData = new FormData();
    formData.append("file", file);

    let res = await fetch("/ocr", {
        method: "POST",
        body: formData
    });

    let data = await res.json();
    document.getElementById("ocr_output").innerText = data.text;
}
</script>

</body>
</html>
"""
