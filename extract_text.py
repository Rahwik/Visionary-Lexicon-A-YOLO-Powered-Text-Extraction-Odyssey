# extract_text.py

import pytesseract
from PIL import Image

def extract_text(image_path):
    # Load image using PIL
    img = Image.open(image_path)

    # Use Tesseract to extract text
    text = pytesseract.image_to_string(img)
    
    # Return extracted text
    return text