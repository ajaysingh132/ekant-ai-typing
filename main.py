from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import pytesseract
from PIL import Image
import io

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Ekant AI Typing</title>
<style>
body { font-family: Arial; text-align:center; padding:20px; }
textarea { width:100%; height:200px; }
button { padding:10px; margin:10px; }
</style>
</head>

<body>

<h2>📄 Ekant AI Typing (LIVE)</h2>

<input type="file" id="file" accept="image/*" capture="environment"><br>

<button onclick="upload()">Scan</button>

<textarea id="output"></textarea><br>

<button onclick="pay()">Pay ₹20</button>

<script>
async function upload(){
 let file=document.getElementById("file").files[0];
 let form=new FormData();
 form.append("file",file);

 let res=await fetch("/process/",{method:"POST",body:form});
 let data=await res.json();
 document.getElementById("output").value=data.text;
}

function pay(){
 window.location.href="upi://pay?pa=YOUR_UPI_ID&pn=EkantTyping&am=20&cu=INR";
}
</script>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.post("/process/")
async def process(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    text = pytesseract.image_to_string(image, lang='eng')
    return {"text": text}
