import cv2
from ultralytics import YOLO
import requests
import time
import threading

MAC_IP = "YOUR_MAC_IP"
MAC_PORT = 5001
CONFIDENCE = 0.5

model = YOLO('PATH_TO_YOUR_MODEL/best.pt')


latest_frame = None
lock = threading.Lock()

def read_frames():
    global latest_frame
    cap = cv2.VideoCapture('rtsp://USERNAME:PASSWORD@CAMERA_IP:554/stream2', cv2.CAP_FFMPEG)
    while True:
        ret, frame = cap.read()
        if ret:
            with lock:
                latest_frame = frame

t = threading.Thread(target=read_frames, daemon=True)
t.start()

print("Monitoring... Waiting for detection.")
time.sleep(3)

while True:
    with lock:
        frame = latest_frame
    if frame is None:
        time.sleep(0.1)
        continue

    results = model(frame, conf=CONFIDENCE, verbose=False)
    for r in results:
        if r.boxes:
            confidence = float(r.boxes[0].conf)
            print(f"DETECTED! Confidence: {confidence:.0%}")
            annotated = results[0].plot()
            cv2.imwrite('/home/pi/detected_token.jpg', annotated)
            print("Photo saved!")
            try:
                requests.post(f"http://{MAC_IP}:{MAC_PORT}/shit_detected", timeout=5)
                print("Signal sent!")
            except Exception as e:
                print(f"Error: {e}")
            exit()
    time.sleep(0.5)
