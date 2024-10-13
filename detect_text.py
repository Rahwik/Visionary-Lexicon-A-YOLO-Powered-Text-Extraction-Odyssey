# detect_text.py

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
    detections = results.xyxy[0]  # Get detections (x1, y1, x2, y2, confidence, class)

    # Annotate detected text areas in the image
    for *box, conf, cls in detections:
        if conf > 0.5:  # Confidence threshold
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw rectangle
            cv2.putText(img, f'{model.names[int(cls)]}: {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the annotated image
    output_image_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_image_path, img)
    print(f'Detected and saved: {output_image_path}')