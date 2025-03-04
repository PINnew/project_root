import cv2
import mediapipe as mp
from datetime import datetime
from database import save_photo
from sse_manager import add_event
import json
import os

detection_zone = {}
detection_timer = None

with open("settings.json", "r") as file:
    settings = json.load(file)
    detection_zone = settings["detection_zone"]

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


def is_inside_detection_zone(x, y):
    return (detection_zone["x"] <= x <= detection_zone["x"] + detection_zone["width"] and
            detection_zone["y"] <= y <= detection_zone["y"] + detection_zone["height"])


def detect_human(frame):
    global detection_timer
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    person_in_zone = False

    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            h, w, _ = frame.shape
            x, y = int(landmark.x * w), int(landmark.y * h)
            if is_inside_detection_zone(x, y):
                person_in_zone = True
                break

    if person_in_zone:
        if detection_timer is None:
            detection_timer = datetime.now()
        elif (datetime.now() - detection_timer).seconds >= 5:
            save_detected_human(frame)
            detection_timer = datetime.now()
    else:
        detection_timer = None


def save_detected_human(frame):
    if not os.path.exists("photos"):
        os.makedirs("photos")
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join("photos", filename)
    cv2.imwrite(filepath, frame)
    save_photo(filename)
    add_event(f"New photo: {filename}")
