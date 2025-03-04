import cv2
import threading
from human_detector import detect_human
from time import sleep

camera_thread = None
camera_running = False


def camera_loop():
    global camera_running
    cap = cv2.VideoCapture(0)
    while camera_running:
        ret, frame = cap.read()
        if ret:
            detect_human(frame)
        sleep(0.1)
    cap.release()


def start_camera():
    global camera_thread, camera_running
    if camera_running:
        return
    camera_running = True
    camera_thread = threading.Thread(target=camera_loop, daemon=True)
    camera_thread.start()


def stop_camera():
    global camera_running
    camera_running = False


def is_camera_running():
    return camera_running
