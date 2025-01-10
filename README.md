# OCR Flask Application with YOLO and Tesseract

## Overview
This project enables users to upload a PDF, convert its pages to images, detect text regions using YOLO, and extract text from those regions using Tesseract OCR. The application is built with Flask and provides a simple web interface for uploading PDFs and viewing the extracted text.

---

## Features
- **PDF to Image Conversion:** Converts uploaded PDF files into individual images for processing.
- **Text Detection:** Uses YOLO to detect text regions within the images.
- **Text Extraction:** Extracts text from the detected regions using Tesseract OCR.
- **Web Interface:** A user-friendly web application to upload files and view results.

---

## Installation

### 1. Clone the Repository
```bash
git clone <repository_url>
cd ocr_flask_yolo_tesseract
```

### 2. Create a Virtual Environment
```bash
# Create a virtual environment
python -m venv ocr_env

# Activate the virtual environment
# On Windows
ocr_env\Scripts\activate

# On macOS/Linux
source ocr_env/bin/activate
```

### 3. Install Dependencies
Install the required libraries from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 4. Download YOLO Weights
Download the YOLOv3 pre-trained weights from the official YOLO website:

- [YOLOv3 weights](https://pjreddie.com/media/files/yolov3.weights)

Place the `yolov3.weights` file in the root directory of the project.

---

## Usage

### 1. Start the Flask Application
Activate your virtual environment and run the application:
```bash
python run.py
```

### 2. Access the Web Interface
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

### 3. Upload a PDF
1. Upload a PDF file using the form on the main page.
2. The application will:
   - Convert the PDF into images.
   - Detect text regions in the images using YOLO.
   - Extract text from the detected regions using Tesseract.

### 4. View Extracted Text
After processing, the extracted text will be displayed on the results page. You can also download the extracted text as a `.txt` file.

---

## Directory Structure
```
ocr_flask_yolo_tesseract/
│
├── static/                 # Static files (CSS, JavaScript, etc.)
│   └── style.css           # CSS for styling
│
├── templates/              # HTML templates
│   ├── index.html          # Main HTML file for uploading PDF
│   └── results.html        # HTML file for displaying extracted text
│
├── __init__.py             # Initializes the Flask app
├── routes.py               # Application routes
├── pdf_to_images.py        # Script to convert PDF to images
├── detect_text.py          # Script to detect text using YOLO
├── extract_text.py         # Script to extract text using Tesseract
├── config.py               # Configuration file for the app
├── requirements.txt        # Project dependencies
├── yolov3.weights          # Pre-trained YOLO weights
├── README.md               # Project documentation
└── run.py                  # Main entry point for the Flask application
```

---

## Notes

### Tesseract OCR Installation
Ensure Tesseract OCR is installed on your system. Download it from the [official Tesseract GitHub page](https://github.com/tesseract-ocr/tesseract) and add it to your system's PATH. Update `extract_text.py` with the Tesseract command path if necessary:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust the path as needed
```

### YOLO Model
The default setup uses YOLOv5 for text detection. Modify `detect_text.py` if you wish to use a different model.

### File Size Limit
You can configure the maximum allowed file size in `config.py`:
```python
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit to 16 MB
```

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
