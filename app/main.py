from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import io
from app.services.ocr import OCR
from app.services.tmdb import MakeCSV

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/scan")
async def scan(file: UploadFile = File(...)):
    image_bytes = await file.read()
    titles = OCR(image_bytes)
    return {"titles": titles.strip().split("\n")}

@app.post("/generate")
async def generate(titles: list[str]):
    csv_content = MakeCSV(titles)
    return StreamingResponse(
        io.StringIO(csv_content), 
        media_type="text/csv", 
        headers={"Content-Disposition": "attachment; filename=movies.csv"})

@app.get("/")
async def root():
    with open(os.path.join(os.path.dirname(__file__), "static", "index.html"), encoding="utf-8") as f:
        return HTMLResponse(f.read())