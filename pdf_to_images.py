# pdf_to_images.py

import os
from pdf2image import convert_from_path

def pdf_to_images(pdf_path, output_folder):
    # Convert PDF to images
    images = convert_from_path(pdf_path)

    # Save images to the output folder
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i + 1}.png')
        image.save(image_path, 'PNG')
        print(f'Saved: {image_path}')