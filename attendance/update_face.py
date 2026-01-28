import os
import cv2
import numpy as np
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_FILE = os.path.join(BASE_DIR, "face_model.yml")

# Ensure dataset folder exists
os.makedirs(DATASET_DIR, exist_ok=True)

# -------------------------
# Step 1: Enter Person Name
# -------------------------
name = input("Enter the name of the person to update/add: ").strip()
person_path = os.path.join(DATASET_DIR, name)
os.makedirs(person_path, exist_ok=True)

# -------------------------
# Step 2: Capture New Images
# -------------------------
cam = cv2.VideoCapture(0)
count = len(os.listdir(person_path))  # continue numbering
print(f"Camera started for {name}. Press 's' to save image | 'q' to quit")

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Capture Face", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        img_path = os.path.join(person_path, f"{count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"Saved {img_path}")
        count += 1

    if key == ord('q') or count >= len(os.listdir(person_path)) + 25:
        break

cam.release()
cv2.destroyAllWindows()
print(f"Image capture for {name} completed.")

# -------------------------
# Step 3: Retrain LBPH Model
# -------------------------
import cv2
faces = []
labels = []
label_map = {}
label_id = 0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

for person_name in sorted(os.listdir(DATASET_DIR)):
    person_path_i = os.path.join(DATASET_DIR, person_name)
    if os.path.isdir(person_path_i):
        label_map[label_id] = person_name
        for img_name in os.listdir(person_path_i):
            img_path = os.path.join(person_path_i, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            detected_faces = face_cascade.detectMultiScale(img, 1.3, 5)
            for (x, y, w, h) in detected_faces:
                faces.append(img[y:y+h, x:x+w])
                labels.append(label_id)
        label_id += 1

# Train and save model
model = cv2.face.LBPHFaceRecognizer_create()
model.train(faces, np.array(labels))
model.save(MODEL_FILE)
print(f"✅ Model retrained successfully with updated images for {name}")
