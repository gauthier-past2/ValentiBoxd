from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import gradio as gr
from PIL import Image
import io

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def OCR(image):
    if image is None:
        return "Please upload an image."

    # Convert PIL image to bytes
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            "Extract all the film titles from this handwritten list. Return only the titles, one per line, nothing else. Put the result in a csv format."
        ]
    )
    
    return response.text

demo = gr.Interface(
    fn=OCR,
    inputs=gr.Image(type="pil", label="Upload an image"),
    outputs=gr.Textbox(label="Detected text"),
    title="ValentiBoxd OCR",
    description="Upload a photo of your film list to extract titles.",
)

demo.launch(share=True)