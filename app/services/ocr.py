import io
import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types
from PIL import Image
import io

load_dotenv(find_dotenv())
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def OCR(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))

    # Load image as bytes for Google API
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()

    # Make request to Google API to extract text from image
    contents = [
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        types.Part.from_text(
            text="This image contains a handwritten list of film titles. Extract every film title you can see, one per line, nothing else. No numbering, no bullet points, no explanations, no comments. Just the titles, one per line."
        )
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents # type: ignore
    )

    return response.text # type: ignore
