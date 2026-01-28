from flask import Flask, render_template, Response, jsonify

# -------------------- IMPORT CAMERA MODULES --------------------
from attendance.camera import gen_frames
from food_waste.camera import gen_food_frames

app = Flask(__name__)

# -------------------- BASIC PAGES --------------------

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

# -------------------- LIVE CAMERA FEEDS --------------------

@app.route("/video_feed")
def video_feed():
    return Response(
        gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/food_feed")
def food_feed():
    return Response(
        gen_food_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# -------------------- REAL-TIME STATUS API --------------------

@app.route("/status")
def status():
    # Dummy values for now (replace with real AI output later)
    return jsonify({
        "attendance_system": "Running",
        "faces_detected": 2,
        "food_waste_status": "Monitoring",
        "food_waste_detected": False,
        "traffic_status": "Normal",
        "bus_status": "On Route"
    })

# -------------------- MAIN --------------------

if __name__ == "__main__":
    app.run(debug=True)
