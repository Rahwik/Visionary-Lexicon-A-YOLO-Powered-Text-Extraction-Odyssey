Here's an extensive guide to creating a Flask-based Optical Character Recognition (OCR) project using YOLO and Tesseract for extracting text from PDFs. This guide will include the project structure, setup instructions, code for each component, and detailed explanations for each step.

### Project Overview
This project will allow users to upload a PDF file, convert the PDF pages to images, detect text regions using YOLO, and extract text from those regions using Tesseract OCR.

### Directory Structure
Here’s the detailed directory structure for your Flask application:

```
ocr_flask_yolo_tesseract/
│
├── app/                    # Flask application folder
│   ├── static/             # Static files (CSS, JavaScript, etc.)
│   ├── templates/          # HTML templates
│   │   ├── index.html      # Main HTML file for uploading PDF
│   │   └── results.html     # HTML file for displaying extracted text
│   ├── __init__.py         # Initializes the Flask app
│   ├── routes.py           # Application routes
│   ├── pdf_to_images.py    # Script to convert PDF to images
│   ├── detect_text.py      # Script to detect text using YOLO
│   ├── extract_text.py      # Script to extract text using Tesseract
│   └── config.py           # Configuration file for the app
│
├── requirements.txt        # Project dependencies
├── yolov3.weights          # Pre-trained YOLO weights
├── README.md               # Project documentation
└── run.py                  # Main entry point for the Flask application
```

### Step 1: Setting Up the Environment

#### 1.1 Create a Virtual Environment
Run the following commands in your terminal to set up a virtual environment:

```bash
# Create a virtual environment
python -m venv ocr_env

# Activate the virtual environment
# On Windows
ocr_env\Scripts\activate

# On macOS/Linux
source ocr_env/bin/activate
```

#### 1.2 Install Required Libraries
Create a `requirements.txt` file in your project directory with the following content:

```
Flask
opencv-python
pytesseract
pdf2image
torch
torchvision
numpy
Pillow
```

Now, install the dependencies:

```bash
pip install -r requirements.txt
```

### Step 2: Download YOLO Weights
Download the pre-trained YOLO weights (v3) from the official YOLO website or the link below:

- [YOLOv3 weights](https://pjreddie.com/media/files/yolov3.weights)

Place the `yolov3.weights` file in the root of your project directory.

### Step 3: Create the Flask Application

#### 3.1 Initialize the Flask App
Create an `__init__.py` file in the `app/` directory:

```python
# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with app.app_context():
        from . import routes

    return app
```

#### 3.2 Set Up Routes
Create a `routes.py` file in the `app/` directory:

```python
# app/routes.py

import os
from flask import render_template, request, redirect, url_for, flash, send_file
from . import create_app
from .pdf_to_images import pdf_to_images
from .detect_text import detect_text
from .extract_text import extract_text

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['pdf_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)

            # Convert PDF to images
            output_folder = 'output_images'
            os.makedirs(output_folder, exist_ok=True)
            pdf_to_images(pdf_path, output_folder)

            # Detect text in the images
            detected_folder = 'detected_images'
            os.makedirs(detected_folder, exist_ok=True)
            for filename in os.listdir(output_folder):
                if filename.endswith('.png'):
                    image_path = os.path.join(output_folder, filename)
                    detect_text(image_path, detected_folder)

            # Extract text from detected images
            extracted_text_file = 'extracted_text.txt'
            with open(extracted_text_file, 'w') as f:
                for filename in os.listdir(detected_folder):
                    if filename.endswith('.png'):
                        image_path = os.path.join(detected_folder, filename)
                        text = extract_text(image_path)
                        f.write(f'--- Text from {filename} ---\n{text}\n\n')

            return redirect(url_for('results', filename=extracted_text_file))

    return render_template('index.html')

@app.route('/results/<filename>')
def results(filename):
    with open(filename, 'r') as f:
        extracted_text = f.read()
    return render_template('results.html', extracted_text=extracted_text)

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)
```

#### 3.3 Create HTML Templates
Create a `templates` folder in the `app/` directory and add the following HTML files:

1. **index.html** (main upload page):

```html
<!-- app/templates/index.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OCR with YOLO and Tesseract</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Upload PDF for OCR</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="pdf_file" accept=".pdf" required>
            <button type="submit">Upload</button>
        </form>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>
            {% for message in messages %}
              <li>{{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
    </div>
</body>
</html>
```

2. **results.html** (display extracted text):

```html
<!-- app/templates/results.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extracted Text</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Extracted Text</h1>
        <pre>{{ extracted_text }}</pre>
        <a href="{{ url_for('index') }}">Upload Another PDF</a>
        <a href="{{ url_for('download', filename='extracted_text.txt') }}">Download Extracted Text</a>
    </div>
</body>
</html>
```

#### 3.4 Create Static Files
Create a `static` folder in the `app/` directory and add a `style.css` file for basic styling:

```css
/* app/static/style.css */

body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: #fff;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
}

input[type="file"] {
    margin: 20px 0;
}

button {
    padding: 10px 20px;
    font-size: 16px;
}
```

### Step 4: Create Utility Scripts

#### 4.1 PDF to Images Conversion
Create a `pdf_to_images.py` file in the `app/` directory:

```python
# app/pdf_to_images.py

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
```

Certainly! Here’s the continuation of the **`detect_text.py`** script, along with the remaining files needed for the project:

#### **4.2 Text Detection Using YOLO (Continued)**

```python
# app/detect_text.py

import cv2
import torch
import os

def detect_text(image_path, output_folder):
    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    # Read the image
    img = cv2.imread(image_path)

    # Perform inference
    results = model(img)

    # Parse results
    detections = results.xyxy[0]  # Get detections for the first image

    # Draw bounding boxes on detected text
    for *box, conf, cls in detections:
        if conf > 0.5:  # Confidence threshold
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Save the detected image
    detected_image_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(detected_image_path, img)
    print(f'Detected text in: {detected_image_path}')
```

### **4.3 Text Extraction Using Tesseract**

Create an **`extract_text.py`** file in the **`app/`** directory:

```python
# app/extract_text.py

import pytesseract
import cv2

def extract_text(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Use Tesseract to extract text
    text = pytesseract.image_to_string(img_rgb)

    return text
```

### **Step 5: Configure Tesseract**

Make sure to install Tesseract OCR on your machine:

- **Windows**: You can download the Tesseract installer from [this link](https://github.com/UB-Mannheim/tesseract/wiki).
- **macOS**: Use Homebrew: `brew install tesseract`.
- **Linux**: Install using `apt`: `sudo apt install tesseract-ocr`.

After installation, make sure to add the Tesseract executable to your system’s PATH. If it's not in your PATH, you can specify the path in your code. For example, in **`extract_text.py`**, add:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path as needed
```

### **Step 6: Create the Main Entry Point**

Create a **`run.py`** file in the root directory of your project:

```python
# run.py

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

### **Step 7: Running the Application**

1. Make sure your virtual environment is activated.
2. Navigate to the project directory.
3. Run the application with the command:

   ```bash
   python run.py
   ```

4. Open your browser and go to **`http://127.0.0.1:5000`**. You should see the PDF upload form.

### **Step 8: Testing the Application**

1. Upload a PDF file containing text.
2. After the file is uploaded, the application will convert the PDF pages to images, detect the text regions, and extract the text.
3. The extracted text will be displayed on the results page, and you will have the option to download the text file.

### **Step 9: Data Sources for Testing**

To test your application, you can use any sample PDF files containing text. You can create a PDF file using a word processor or download sample PDF documents from websites like:

- [Sample PDF Files](http://www.pdf995.com/samples/)
- [PDF Archive](https://www.pdf-archive.com/)

### **Step 10: Final Thoughts and Enhancements**

- **Enhancements**: Consider adding features like error handling, support for multiple file formats, or improved UI/UX design.
- **Performance Optimization**: If you're working with large PDFs, consider optimizing the image processing or allowing for batch processing.

### **Conclusion**

You now have a fully functional OCR application built using Flask, YOLO for text detection, and Tesseract for text extraction from PDFs. This detailed guide should help you understand each part of the project and customize it according to your needs. If you have any questions or need further assistance, feel free to ask!
