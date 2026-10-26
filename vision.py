import cv2
import os

class ObserverVision:
    def __init__(self):
        cascade_path = "haarcascade_frontalface_default.xml"
        if not os.path.exists(cascade_path):
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def check_observer(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        is_observed = len(faces) > 0
        return is_observed, faces
