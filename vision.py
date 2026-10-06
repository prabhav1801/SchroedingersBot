import threading
import time
import cv2
import numpy as np

class VideoStream:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.grabbed, self.frame = self.cap.read()
        self.stopped = False
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while not self.stopped:
            if self.cap.isOpened():
                self.grabbed, self.frame = self.cap.read()
            else:
                time.sleep(0.01)

    def read(self):
        return self.grabbed, self.frame

    def release(self):
        self.stopped = False
        self.cap.release()

obj_points = np.array([
    (0.0, 0.0, 0.0), (0.0, -330.0, -65.0),
    (-225.0, 170.0, -135.0), (225.0, 170.0, -135.0),
    (-150.0, -150.0, -125.0), (150.0, -150.0, -125.0)
], dtype=np.float64)

def process_vision(frame, face_cascade):
    # TODO: fine tune focal length adjustment for wider webcams later
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    h, w, _ = frame.shape
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(40, 40))
    
    if len(faces) == 0:
        return False, None, None, 0

    x, y, fw, fh = faces[0]
    img_points = np.array([
        (x + fw * 0.5, y + fh * 0.5), (x + fw * 0.5, y + fh * 0.9),
        (x + fw * 0.3, y + fh * 0.35), (x + fw * 0.7, y + fh * 0.35),
        (x + fw * 0.35, y + fh * 0.75), (x + fw * 0.65, y + fh * 0.75)
    ], dtype=np.float64)

    focal = w
    center = (w / 2, h / 2)
    cam_matrix = np.array([[focal, 0, center[0]], [0, focal, center[1]], [0, 0, 1]], dtype=np.float64)
    
    success, rvec, tvec = cv2.solvePnP(obj_points, img_points, cam_matrix, np.zeros((4, 1)), flags=cv2.SOLVEPNP_ITERATIVE)
    if not success:
        return True, None, None, fw

    rmat, _ = cv2.Rodrigues(rvec)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    return True, angles[1], angles[0], fw