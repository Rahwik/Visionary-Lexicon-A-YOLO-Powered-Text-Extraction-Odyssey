import os
from flask import render_template, request, redirect, url_for, flash, send_file
from pdf_to_images import pdf_to_images
from detect_text import detect_text
from extract_text import extract_text

# Define the main routes here, but don't create the app instance.
def register_routes(app):
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

