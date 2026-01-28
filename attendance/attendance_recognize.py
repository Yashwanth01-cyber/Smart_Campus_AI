import cv2
import os
import csv
from datetime import datetime

# -------------------------
# Paths and Setup
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")

# Ensure CSV header exists
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time", "Confidence"])

# -------------------------
# Load model and face detector
# -------------------------
MODEL_FILE = os.path.join(BASE_DIR, "attendance", "face_model.yml")
DATASET_DIR = os.path.join(BASE_DIR, "attendance", "dataset")

model = cv2.face.LBPHFaceRecognizer_create()
model.read(MODEL_FILE)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Build label map
label_map = {}
label_id = 0
for person_name in sorted(os.listdir(DATASET_DIR)):
    person_path = os.path.join(DATASET_DIR, person_name)
    if os.path.isdir(person_path):
        label_map[label_id] = person_name
        label_id += 1

print("Label mapping:", label_map)

# -------------------------
# Live Camera Feed
# -------------------------
cam = cv2.VideoCapture(0)
marked = set()  # to avoid duplicate attendance

print("Camera started. Press 'q' to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        label, confidence = model.predict(face_img)

        name = "Unknown"
        confidence_text = f"{confidence:.1f}"

        if confidence < 80:  # lower = more confident
            name = label_map.get(label, "Unknown")
            if name not in marked:
                with open(ATTENDANCE_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        name,
                        datetime.now().strftime("%Y-%m-%d"),
                        datetime.now().strftime("%H:%M:%S"),
                        f"{confidence:.1f}"
                    ])
                marked.add(name)

        # Draw rectangle + name + confidence
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, f"{name} ({confidence_text})", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Face Recognition Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print(f"Camera closed. Attendance saved in {ATTENDANCE_FILE}")
