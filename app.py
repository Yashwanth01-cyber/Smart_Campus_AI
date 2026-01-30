from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Cameras
attendance_cam = cv2.VideoCapture(0)
food_cam = cv2.VideoCapture(0)

def attendance_stream():
    while True:
        success, frame = attendance_cam.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def food_stream():
    while True:
        success, frame = food_cam.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# Pages
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/food")
def food():
    return render_template("food.html")

@app.route("/traffic")
def traffic():
    return render_template("traffic.html")

@app.route("/bus")
def bus():
    return render_template("bus.html")

# Video feeds
@app.route("/attendance_feed")
def attendance_feed():
    return Response(attendance_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/food_feed")
def food_feed():
    return Response(food_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
