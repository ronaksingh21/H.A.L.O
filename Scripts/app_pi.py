from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta
from simple_facerec import SimpleFacerec
import cv2
import requests
import os
import threading
import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client

# Initialize face recognition
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize Firebase
cred = credentials.Certificate('/home/ronak/Downloads/caca-c9b2tk-firebase-adminsdk-lijxn-038eb4cbc6.json')  # Path to Firebase credentials file
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Twilio Configuration
account_sid = '' # Replace with  Twilio SID
auth_token = ''  # Replace with  Twilio token
twilio_client = Client(account_sid, auth_token)
twilio_number = ''  # Replace with  Twilio number

# Flask app
app = Flask(__name__)

# Dictionary to track last log time for each face
last_log_time = {}

# Function to send SMS
def send_sms(phone_number, message):
    try:
        message = twilio_client.messages.create(
            body=message,
            from_=twilio_number,
            to=phone_number
        )
        print(f"Message sent to {phone_number}")
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")

# Fetch the phone number of the user directly (assuming single user)
def get_demo_phone_number():
    user_ref = db.collection('users').limit(1).stream()  # Fetch first user (assuming only one user)
    for user in user_ref:
        return user.to_dict().get('phone_number')
    return None

# Function to send logs to Heroku and SMS
def send_log_to_heroku_and_sms(name):
    log_entry = {
        "logs": [name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]  # Sending as an array of [name, timestamp]
    }
    heroku_url = "https://secret-scrubland-70107-10a3a06dbcba.herokuapp.com/update_logs"  # Correct endpoint

    try:
        # Send log to Heroku
        requests.post(heroku_url, json=log_entry)
        
        # Fetch phone number directly from Firestore (single user)
        phone_number = get_demo_phone_number()
        if phone_number:
            # Send SMS
            send_sms(phone_number, f"A person named {name} was detected at your front door.")
        else:
            print("No phone number found in Firestore.")
            
    except Exception as e:
        print(f"Failed to send log to Heroku or SMS: {e}")

# Function to handle face detection and log submission
def detect_and_log_faces():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            continue

        # Detect faces
        face_locations, face_names = sfr.detect_known_faces(frame)

        for name in face_names:
            add_log(name)

# Function to add a log entry with idempotency (no duplicate for 1 minute)
def add_log(name):
    current_time = datetime.now()

    # Check if the name was logged within the past 1 minute
    if name in last_log_time:
        time_diff = current_time - last_log_time[name]
        if time_diff < timedelta(minutes=1):
            return  # Skip logging this name if it's within 1 minute

    # Send log to Heroku and SMS
    send_log_to_heroku_and_sms(name)

    # Update last log time for the name
    last_log_time[name] = current_time

# Thread to run face detection in the background
def start_face_detection_thread():
    face_detection_thread = threading.Thread(target=detect_and_log_faces)
    face_detection_thread.start()

# Route to trigger face detection (can be used by external API calls or for debugging)
@app.route("/detect_face")
def detect_face():
    return jsonify({"status": "Face detection system is running..."})

# Route to display logs (auto-refresh every 5 seconds)
@app.route('/', methods=['POST'])
def receive_log():
    data = request.get_json()
    # Process and store the received log (name and timestamp)


if __name__ == "__main__":
    # Start the face detection thread
    start_face_detection_thread()
    
    # Start the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)

    # Release the camera when done (Flask shutdown)
    cap.release()
    cv2.destroyAllWindows()
