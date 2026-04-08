from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ekant AI Typing Running 🚀"}

# 👉 OCR API
@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    text = pytesseract.image_to_string(image)
    return {"text": text}

# 👉 UI (Voice typing)
@app.get("/ui", response_class=HTMLResponse)
def ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
