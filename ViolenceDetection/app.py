import os
import time
import cv2
import pandas as pd
import numpy as np
import xgboost as xgb
import cvzone
import smtplib
from email.message import EmailMessage
from ultralytics import YOLO
from flask import Flask, request, render_template, Response
from flask import send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# =================== Email Settings =================== #
SENDER_EMAIL = "tensortitans2612@gmail.com"
SENDER_PASSWORD = "hjcy lblh gwhv jmzk"  # Use app-specific passwords in production
DEFAULT_RECEIVERS = [
    "siddhantpatil1543@gmail.com",
    "shantanua.panse@gmail.com"
]

def send_emergency_email(suspicious_frame=None):
    """
    Send an emergency email alert with an optional image attachment.
    """
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(DEFAULT_RECEIVERS)
    msg["Subject"] = "Emergency Incident !! Suspicious Activity !!"
    msg.set_content("A suspicious activity has been detected. Please check the attached image for details.")

    if suspicious_frame is not None:
        ret, buffer = cv2.imencode('.jpg', suspicious_frame)
        if ret:
            img_data = buffer.tobytes()
            msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename="suspicious.jpg")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Emergency Email sent successfully to:", ", ".join(DEFAULT_RECEIVERS))
    except Exception as e:
        print("❌ Failed to send email:", e)

# =================== Detection Function =================== #
def detect_shoplifting(video_path, output_path):
    # Load YOLOv8 model (adjust model path as needed)
    model_yolo = YOLO('yolo11s-pose.pt')
    # Load the trained XGBoost model (adjust model path as needed)
    model = xgb.Booster()
    model.load_model('trained_model.json')

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return False

    # Get properties from the input video to create the output writer
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    count = 0
    email_sent = False

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        count += 1
        # Process every 3rd frame for detection (adjust as needed)
        if count % 3 != 0:
            out.write(frame)
            continue

        # Run YOLO detection
        results = model_yolo(frame, verbose=False)
        annotated_frame = results[0].plot(boxes=False)

        # Convert the annotated frame from RGB to BGR (OpenCV uses BGR)
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
        # Force proper 8-bit data type
        annotated_frame = np.uint8(annotated_frame)

        suspicious_detected = False

        for r in results:
            bound_box = r.boxes.xyxy  # Bounding box coordinates
            conf = r.boxes.conf.tolist()  # Confidence levels
            keypoints = r.keypoints.xyn.tolist()  # Keypoints for human pose

            for index, box in enumerate(bound_box):
                if conf[index] > 0.55:
                    x1, y1, x2, y2 = box.tolist()

                    # Prepare data for the XGBoost prediction
                    data = {}
                    for j in range(len(keypoints[index])):
                        data[f'x{j}'] = keypoints[index][j][0]
                        data[f'y{j}'] = keypoints[index][j][1]
                    df = pd.DataFrame(data, index=[0])
                    dmatrix = xgb.DMatrix(df)

                    # Predict using the XGBoost model
                    sus = model.predict(dmatrix)
                    binary_predictions = (sus > 0.5).astype(int)

                    if binary_predictions == 0:
                        suspicious_detected = True
                        cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                        cvzone.putTextRect(annotated_frame, "Suspicious", (int(x1), int(y1)), scale=1, thickness=1)
                    else:
                        cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cvzone.putTextRect(annotated_frame, "Normal", (int(x1), int(y1) + 50), scale=1, thickness=1)

        if suspicious_detected:
            alert_message = "Emergency Alert!! Suspicious Activity detected !!!"
            cvzone.putTextRect(annotated_frame, alert_message, (50, 50), scale=2, thickness=2, colorR=(0, 0, 255))
            if not email_sent:
                send_emergency_email(frame)
                email_sent = True

        # Resize annotated frame to the original dimensions and write to output
        annotated_frame = cv2.resize(annotated_frame, (width, height))
        out.write(annotated_frame)

    cap.release()
    out.release()
    return True

# =================== Flask Routes =================== #
@app.route('/', methods=['GET', 'POST'])
def index():
    processed_video = None
    cache_buster = None
    if request.method == 'POST':
        if 'video' not in request.files:
            return "No video file uploaded", 400
        file = request.files['video']
        if file.filename == '':
            return "No file selected", 400

        # Save the uploaded video
        input_video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_video_path)

        # Process the video and save the annotated output
        output_video_filename = "processed_" + file.filename
        output_video_path = os.path.join(app.config['PROCESSED_FOLDER'], output_video_filename)
        if detect_shoplifting(input_video_path, output_video_path):
            processed_video = output_video_filename
            cache_buster = int(time.time())

    return render_template('index.html', processed_video=processed_video, cache_buster=cache_buster)

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.04)
    cap.release()

@app.route('/video_feed/<filename>')
def video_feed(filename):
    video_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    return Response(generate_frames(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/download/<filename>')
def download_video(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5003)