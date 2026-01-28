import cv2
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)

name = input("Enter person name: ").strip()
person_path = os.path.join(DATASET_DIR, name)
os.makedirs(person_path, exist_ok=True)

cam = cv2.VideoCapture(0)
count = 0

print("Camera started")
print("Press 's' to save image | 'q' to quit")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    cv2.imshow("Face Capture", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        img_path = os.path.join(person_path, f"{count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"Saved {img_path}")
        count += 1

    if key == ord('q') or count >= 25:
        break

cam.release()
cv2.destroyAllWindows()
