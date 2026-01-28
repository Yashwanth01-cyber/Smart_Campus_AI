import cv2
import os
import csv
from datetime import datetime
import numpy as np

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

FOOD_WASTE_FILE = os.path.join(DATA_DIR, "food_waste.csv")

if not os.path.exists(FOOD_WASTE_FILE):
    with open(FOOD_WASTE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DateTime", "Wastage %", "Notes"])

# -------------------------
# Camera setup
# -------------------------
cam = cv2.VideoCapture(0)
print("Camera started. Place the plate in front of the camera. Press 'q' to quit.")

last_logged_wastage = None  # To track last logged reading
threshold = 5  # Minimum % change to log again

while True:
    ret, frame = cam.read()
    if not ret:
        break

    height, width, _ = frame.shape
    # Define center plate area
    plate_area = frame[height//2-100:height//2+100, width//2-100:width//2+100]

    # Convert to gray and threshold
    gray = cv2.cvtColor(plate_area, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    # Estimate wastage by counting white pixels
    white_pixels = np.sum(thresh == 255)
    total_pixels = thresh.size
    wastage_percent = int((white_pixels / total_pixels) * 100)

    # Draw rectangle + label
    cv2.rectangle(frame, (width//2-100, height//2-100), (width//2+100, height//2+100), (0,255,0), 2)
    cv2.putText(frame, f"Wastage: {wastage_percent}%", (width//2-100, height//2-120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    # Log to CSV only if significant change
    if last_logged_wastage is None or abs(wastage_percent - last_logged_wastage) >= threshold:
        with open(FOOD_WASTE_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                wastage_percent,
                "Live detection"
            ])
        last_logged_wastage = wastage_percent  # Update last logged value

    cv2.imshow("Food Waste Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print(f"Camera closed. Wastage data saved in {FOOD_WASTE_FILE}")
