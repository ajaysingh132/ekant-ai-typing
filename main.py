from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ekant AI Typing Running 🚀"}

# 🔥 OCR API (सबसे जरूरी)
@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    text = pytesseract.image_to_string(image)
    return {"text": text}

# 🔥 UI
@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <h1>🚀 AI Typing System</h1>

    <h2>🎤 Voice</h2>
    <button onclick="start()">Start Speaking</button>
    <p id="voice"></p>

    <h2>📸 OCR (Photo / Handwriting)</h2>
    <input type="file" id="file">
    <button onclick="upload()">Convert</button>
    <p id="ocr"></p>

    <script>
    function start() {
        const r = new webkitSpeechRecognition();
        r.lang = "hi-IN";
        r.onresult = e => {
            document.getElementById("voice").innerText =
            e.results[0][0].transcript;
        };
        r.start();
    }

    async function upload() {
        let f = document.getElementById("file").files[0];
        let fd = new FormData();
        fd.append("file", f);

        let res = await fetch("/ocr", {
            method: "POST",
            body: fd
        });

        let data = await res.json();
        document.getElementById("ocr").innerText = data.text;
    }
    </script>
    """
