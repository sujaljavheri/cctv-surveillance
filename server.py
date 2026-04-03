# import pickle
# import numpy as np
# from sklearn.neighbors import KNeighborsClassifier
# import cv2
# from flask import Flask, Response, jsonify, request
# from flask_cors import CORS
# import threading
# import os
# import time

# from face_utils import (
#     load_detectors, detect_faces, preprocess_face,
#     KNN_METRIC, KNN_WEIGHTS, get_n_neighbors
# )
# from alerts import trigger_alert, ALERT_ON
# from camera_config import (
#     CAMERAS, STREAM_WIDTH, STREAM_HEIGHT, STREAM_FPS,
#     RECONNECT_ATTEMPTS, RECONNECT_DELAY
# )

# # ================================================================
# # LOAD KNN MODEL
# # ================================================================
# with open('data/names.pkl', 'rb') as f: LABELS = pickle.load(f)
# with open('data/faces_data.pkl', 'rb') as f: FACES = pickle.load(f)

# N_NEIGHBORS = get_n_neighbors(LABELS)
# knn = KNeighborsClassifier(n_neighbors=N_NEIGHBORS, metric=KNN_METRIC, weights=KNN_WEIGHTS)
# knn.fit(FACES, LABELS)
# print(f"[INFO] KNN loaded — {len(set(LABELS))} people, {len(LABELS)} samples, k={N_NEIGHBORS}")

# num_people        = len(set(LABELS))
# UNKNOWN_THRESHOLD = 4500 if num_people == 1 else 5000
# MIN_DISTANCE_GAP  = 0    if num_people == 1 else 300

# # ================================================================
# # DETECTORS
# # ================================================================
# net, haar, USE_DNN = load_detectors()

# # ================================================================
# # FLASK
# # ================================================================
# app = Flask(__name__)
# CORS(app)

# # ================================================================
# # PREDICT
# # ================================================================
# def _predict(face_vec):
#     distances, idxs = knn.kneighbors(face_vec, n_neighbors=N_NEIGHBORS)
#     min_dist = float(np.min(distances[0]))
#     avg_dist = float(np.mean(distances[0]))
#     if min_dist > UNKNOWN_THRESHOLD:
#         return "Unknown", avg_dist
#     if num_people >= 2:
#         nbr_labels = [LABELS[i] for i in idxs[0]]
#         ld = {}
#         for lbl, d in zip(nbr_labels, distances[0]):
#             ld.setdefault(lbl, []).append(d)
#         sorted_pp = sorted({l: np.mean(v) for l,v in ld.items()}.items(), key=lambda kv: kv[1])
#         best_name = sorted_pp[0][0]
#         gap = (sorted_pp[1][1]-sorted_pp[0][1]) if len(sorted_pp)>=2 else 999
#         if gap < MIN_DISTANCE_GAP:
#             return "Unknown", avg_dist
#         return best_name, sorted_pp[0][1]
#     return knn.predict(face_vec)[0], avg_dist

# # ================================================================
# # ANNOTATE FRAME
# # ================================================================
# def annotate_frame(frame, cam_id):
#     try:
#         faces = detect_faces(frame, net, haar, USE_DNN)
#     except Exception:
#         faces = []

#     for (x1, y1, w, h, _) in faces:
#         x2, y2 = x1+w, y1+h
#         crop   = frame[y1:y2, x1:x2]
#         if crop.size == 0: continue
#         try:
#             vec        = preprocess_face(crop).flatten().reshape(1, -1)
#             name, dist = _predict(vec)
#         except Exception: continue

#         trigger_alert(name, camera_id=cam_id)

#         color = (0,255,0) if name != "Unknown" else (0,0,255)
#         cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
#         label = f"{name} ({int(dist)})"
#         (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
#         cv2.rectangle(frame, (x1, y1-lh-12), (x1+lw+6, y1), color, -1)
#         cv2.putText(frame, label, (x1+3, y1-5),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2)
#         if name in ALERT_ON:
#             cv2.putText(frame, "ALERT", (x1, y2+18),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
#     return frame

# # ================================================================
# # NO SIGNAL FRAME
# # ================================================================
# def make_no_signal_frame(cam_id, reason="No Signal"):
#     frame    = np.zeros((STREAM_HEIGHT, STREAM_WIDTH, 3), dtype=np.uint8)
#     for i in range(0, STREAM_WIDTH,  40): cv2.line(frame, (i,0), (i,STREAM_HEIGHT), (25,25,25), 1)
#     for i in range(0, STREAM_HEIGHT, 40): cv2.line(frame, (0,i), (STREAM_WIDTH,i), (25,25,25), 1)
#     cam_name = CAMERAS.get(cam_id, {}).get("name", f"Camera {cam_id+1}")
#     cv2.putText(frame, cam_name, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (80,80,80), 1)
#     cv2.putText(frame, reason,
#                 (STREAM_WIDTH//2-90, STREAM_HEIGHT//2-10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.85, (55,55,55), 2)
#     cv2.putText(frame, "Edit camera_config.py to configure",
#                 (STREAM_WIDTH//2-140, STREAM_HEIGHT//2+25),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.45, (55,55,55), 1)
#     return frame

# # ================================================================
# # CAMERA HANDLER — supports webcam / RTSP / HTTP / video file
# # ================================================================
# class CameraHandler:
#     def __init__(self, cam_id, config):
#         self.cam_id          = cam_id
#         self.config          = config
#         self.cam_type        = config.get("type", "disabled")
#         self.source          = config.get("source")
#         self.name            = config.get("name", f"Camera {cam_id}")
#         self.raw_frame       = None
#         self.annotated_frame = None
#         self.lock            = threading.Lock()
#         self.connected       = False
#         self.status          = "Initializing"

#         if self.cam_type != "disabled":
#             threading.Thread(target=self._capture_loop, daemon=True).start()
#             threading.Thread(target=self._process_loop, daemon=True).start()
#             print(f"[CAM {cam_id}] {self.name} — type={self.cam_type} source={self.source}")
#         else:
#             self.status = "Disabled"
#             print(f"[CAM {cam_id}] {self.name} — DISABLED")

#     def _open_source(self):
#         if self.cam_type == "webcam":
#             cap = cv2.VideoCapture(self.source)
#         elif self.cam_type in ("rtsp", "http"):
#             cap = cv2.VideoCapture(self.source, cv2.CAP_FFMPEG)
#             cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#         elif self.cam_type == "video":
#             if not os.path.exists(str(self.source)):
#                 print(f"[CAM {self.cam_id}] Video not found: {self.source}")
#                 return None
#             cap = cv2.VideoCapture(self.source)
#         else:
#             return None

#         if not cap.isOpened():
#             return None

#         cap.set(cv2.CAP_PROP_FRAME_WIDTH,  STREAM_WIDTH)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
#         if self.cam_type == "webcam":
#             cap.set(cv2.CAP_PROP_FPS, STREAM_FPS)
#         return cap

#     def _capture_loop(self):
#         while True:
#             cap = self._open_source()
#             if cap is None:
#                 self.connected = False
#                 self.status    = "Cannot connect — check URL/source"
#                 print(f"[CAM {self.cam_id}] Cannot open — retry in {RECONNECT_DELAY}s")
#                 time.sleep(RECONNECT_DELAY)
#                 continue

#             self.connected = True
#             self.status    = "Live"
#             print(f"[CAM {self.cam_id}] Connected — {self.name}")

#             while True:
#                 ret, frame = cap.read()
#                 if not ret:
#                     if self.cam_type == "video":
#                         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop video
#                         continue
#                     self.connected = False
#                     self.status    = "Reconnecting..."
#                     print(f"[CAM {self.cam_id}] Lost — reconnecting in {RECONNECT_DELAY}s")
#                     break
#                 with self.lock:
#                     self.raw_frame = frame

#             cap.release()
#             time.sleep(RECONNECT_DELAY)

#     def _process_loop(self):
#         while True:
#             raw = None
#             with self.lock:
#                 if self.raw_frame is not None:
#                     raw = self.raw_frame.copy()
#             if raw is None:
#                 time.sleep(0.02); continue

#             annotated = annotate_frame(raw, self.cam_id)
#             tag = "DNN" if USE_DNN else "HAAR"
#             cv2.putText(annotated, f"{self.name} [{tag}]",
#                         (10, annotated.shape[0]-8),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.42, (120,120,120), 1)

#             with self.lock:
#                 self.annotated_frame = annotated

#     def get_frame(self):
#         with self.lock:
#             if self.annotated_frame is not None:
#                 return self.annotated_frame.copy()
#         return make_no_signal_frame(self.cam_id,
#                self.status if not self.connected else "No Signal")

# # ================================================================
# # INIT ALL CAMERAS
# # ================================================================
# cameras = {cam_id: CameraHandler(cam_id, cfg) for cam_id, cfg in CAMERAS.items()}

# # ================================================================
# # FRAME GENERATOR
# # ================================================================
# def generate_frames(cam_id):
#     handler = cameras.get(cam_id)
#     while True:
#         frame = handler.get_frame() if handler else make_no_signal_frame(cam_id, "Not Configured")
#         ret, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
#         if not ret: continue
#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')

# # ================================================================
# # ROUTES
# # ================================================================
# @app.route('/video_feed/<int:cam_id>')
# def video_feed(cam_id):
#     return Response(generate_frames(cam_id),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/cameras')
# def camera_list():
#     return jsonify([{
#         "id":     cam_id,
#         "name":   h.name,
#         "type":   h.cam_type,
#         "active": h.connected or h.cam_type == "video",
#         "status": h.status,
#         "url":    f"http://localhost:5000/video_feed/{cam_id}"
#     } for cam_id, h in cameras.items()])

# @app.route('/camera_status')
# def camera_status():
#     return jsonify({
#         cam_id: {"connected": h.connected, "status": h.status, "type": h.cam_type}
#         for cam_id, h in cameras.items()
#     })

# @app.route('/upload_faces', methods=['POST'])
# def upload_faces():
#     name = request.form.get('name')
#     if not name: return {"error": "Name required"}, 400
#     files = request.files.getlist('images')
#     if len(files) < 3: return {"error": "Upload at least 3 images"}, 400
#     faces_data = []
#     for file in files:
#         npimg = np.frombuffer(file.read(), np.uint8)
#         img   = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#         if img is None: continue
#         for (x1, y1, w, h, _) in detect_faces(img, net, haar, USE_DNN):
#             crop = img[y1:y1+h, x1:x1+w]
#             if crop.size > 0: faces_data.append(preprocess_face(crop).flatten())
#     if not faces_data: return {"error": "No face detected"}, 400
#     faces_data = np.array(faces_data)
#     names_path, faces_path = 'data/names.pkl', 'data/faces_data.pkl'
#     if os.path.exists(faces_path):
#         with open(faces_path,'rb') as f: ef = pickle.load(f)
#         with open(names_path, 'rb') as f: en = pickle.load(f)
#         combined_faces = np.append(ef, faces_data, axis=0)
#         combined_names = en + [name]*len(faces_data)
#     else:
#         combined_faces, combined_names = faces_data, [name]*len(faces_data)
#     with open(faces_path,'wb') as f: pickle.dump(combined_faces, f)
#     with open(names_path, 'wb') as f: pickle.dump(combined_names, f)
#     global knn, N_NEIGHBORS
#     N_NEIGHBORS = get_n_neighbors(combined_names)
#     knn = KNeighborsClassifier(n_neighbors=N_NEIGHBORS, metric=KNN_METRIC, weights=KNN_WEIGHTS)
#     knn.fit(combined_faces, combined_names)
#     return {"message": f"{name} trained with {len(faces_data)} samples"}

# @app.route('/')
# def index():
#     active = sum(1 for h in cameras.values() if h.connected)
#     return f"CCTV | {active}/{len(cameras)} live | {'DNN' if USE_DNN else 'Haar'} | k={N_NEIGHBORS}"

# if __name__ == '__main__':
#     print(f"\n[INFO] {len(cameras)} camera slots | edit camera_config.py to configure")
#     print("[INFO] http://localhost:5000\n")
#     app.run(host='0.0.0.0', port=5000, threaded=True)








# #new2


# import pickle
# import numpy as np
# from sklearn.neighbors import KNeighborsClassifier
# import cv2
# from flask import Flask, Response, jsonify, request
# from flask_cors import CORS
# import threading
# import os
# import time

# from face_utils import (
#     load_detectors, detect_faces, preprocess_face,
#     KNN_METRIC, KNN_WEIGHTS, get_n_neighbors, FEATURE_SIZE
# )
# from alerts import trigger_alert, ALERT_ON

# # ================================================================
# # LOAD KNN MODEL
# # ================================================================
# with open('data/names.pkl', 'rb') as f: LABELS = pickle.load(f)
# with open('data/faces_data.pkl', 'rb') as f: FACES = pickle.load(f)

# N_NEIGHBORS = get_n_neighbors(LABELS)   # dynamic k from face_utils
# knn = KNeighborsClassifier(
#     n_neighbors=N_NEIGHBORS,
#     metric=KNN_METRIC,
#     weights=KNN_WEIGHTS
# )
# knn.fit(FACES, LABELS)
# print(f"[INFO] KNN loaded — {len(set(LABELS))} people, {len(LABELS)} samples, k={N_NEIGHBORS}")

# num_people        = len(set(LABELS))
# UNKNOWN_THRESHOLD = 4500 if num_people == 1 else 5000
# MIN_DISTANCE_GAP  = 0    if num_people == 1 else 300

# # ================================================================
# # DETECTORS
# # ================================================================
# net, haar, USE_DNN = load_detectors()

# # ================================================================
# # FLASK
# # ================================================================
# app = Flask(__name__)
# CORS(app)

# # ================================================================
# # CAMERA — capture + process threads
# # ================================================================
# class Camera:
#     def __init__(self, source=0):
#         self.cap = cv2.VideoCapture(source)
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#         self.cap.set(cv2.CAP_PROP_FPS, 30)
#         self.raw_frame       = None
#         self.annotated_frame = None
#         self.lock            = threading.Lock()
#         self._cam_id         = source   # used for alerts
#         threading.Thread(target=self._capture, daemon=True).start()
#         threading.Thread(target=self._process, daemon=True).start()
#         print("[INFO] Camera started")

#     def _capture(self):
#         while True:
#             ret, frame = self.cap.read()
#             if ret:
#                 with self.lock: self.raw_frame = frame

#     def _process(self):
#         while True:
#             raw = None
#             with self.lock:
#                 if self.raw_frame is not None: raw = self.raw_frame.copy()
#             if raw is None: time.sleep(0.01); continue

#             try: faces = detect_faces(raw, net, haar, USE_DNN)
#             except Exception as e: print(f"[WARN] {e}"); faces = []

#             for (x1, y1, w, h, _) in faces:
#                 x2, y2 = x1+w, y1+h
#                 crop   = raw[y1:y2, x1:x2]
#                 if crop.size == 0: continue
#                 try:
#                     vec        = preprocess_face(crop).flatten().reshape(1, -1)
#                     name, dist = _predict(vec)
#                 except Exception: continue

#                 # ---- TRIGGER ALERT ----
#                 trigger_alert(name, camera_id=self._cam_id)

#                 # Draw box
#                 color = (0,255,0) if name != "Unknown" else (0,0,255)
#                 cv2.rectangle(raw, (x1,y1), (x2,y2), color, 2)
#                 label = f"{name} ({int(dist)})"
#                 (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
#                 cv2.rectangle(raw, (x1, y1-lh-12), (x1+lw+6, y1), color, -1)
#                 cv2.putText(raw, label, (x1+3, y1-5),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2)

#                 # Alert indicator on frame
#                 if name in ALERT_ON:
#                     cv2.putText(raw, "! ALERT", (x1, y2+18),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,255), 2)

#             with self.lock: self.annotated_frame = raw

#     def get_frame(self):
#         with self.lock:
#             return self.annotated_frame.copy() if self.annotated_frame is not None else None

# camera = Camera(0)

# # ================================================================
# # PREDICT — uses improved thresholds
# # ================================================================
# def _predict(face_vec):
#     distances, idxs = knn.kneighbors(face_vec, n_neighbors=N_NEIGHBORS)
#     min_dist = float(np.min(distances[0]))
#     avg_dist = float(np.mean(distances[0]))

#     if min_dist > UNKNOWN_THRESHOLD:
#         return "Unknown", avg_dist

#     if num_people >= 2:
#         nbr_labels = [LABELS[i] for i in idxs[0]]
#         ld = {}
#         for lbl, d in zip(nbr_labels, distances[0]):
#             ld.setdefault(lbl, []).append(d)
#         sorted_pp = sorted({l: np.mean(v) for l,v in ld.items()}.items(), key=lambda kv: kv[1])
#         best_name = sorted_pp[0][0]
#         gap = (sorted_pp[1][1] - sorted_pp[0][1]) if len(sorted_pp) >= 2 else 999
#         if gap < MIN_DISTANCE_GAP:
#             return "Unknown", avg_dist
#         return best_name, sorted_pp[0][1]

#     return knn.predict(face_vec)[0], avg_dist

# # ================================================================
# # FRAME GENERATOR
# # ================================================================
# def generate_frames(cam_id):
#     tag = "DNN" if USE_DNN else "HAAR"
#     while True:
#         frame = camera.get_frame()
#         if frame is None: time.sleep(0.01); continue
#         display = frame.copy()
#         cv2.putText(display, f"Feed {cam_id} [{tag}]",
#                     (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
#         ret, buf = cv2.imencode('.jpg', display, [cv2.IMWRITE_JPEG_QUALITY, 80])
#         if not ret: continue
#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')

# # ================================================================
# # ROUTES
# # ================================================================
# @app.route('/video_feed/<int:cam_id>')
# def video_feed(cam_id):
#     return Response(generate_frames(cam_id),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/upload_faces', methods=['POST'])
# def upload_faces():
#     name = request.form.get('name')
#     if not name: return {"error": "Name required"}, 400
#     files = request.files.getlist('images')
#     if len(files) < 3: return {"error": "Upload at least 3 images"}, 400

#     faces_data = []
#     for file in files:
#         npimg = np.frombuffer(file.read(), np.uint8)
#         img   = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#         if img is None: continue
#         for (x1, y1, w, h, _) in detect_faces(img, net, haar, USE_DNN):
#             crop = img[y1:y1+h, x1:x1+w]
#             if crop.size > 0:
#                 faces_data.append(preprocess_face(crop).flatten())

#     if not faces_data: return {"error": "No face detected"}, 400

#     faces_data = np.array(faces_data)
#     names_path, faces_path = 'data/names.pkl', 'data/faces_data.pkl'
#     if os.path.exists(faces_path):
#         with open(faces_path,'rb') as f: ef = pickle.load(f)
#         with open(names_path, 'rb') as f: en = pickle.load(f)
#         combined_faces = np.append(ef, faces_data, axis=0)
#         combined_names = en + [name]*len(faces_data)
#     else:
#         combined_faces, combined_names = faces_data, [name]*len(faces_data)

#     with open(faces_path,'wb') as f: pickle.dump(combined_faces, f)
#     with open(names_path, 'wb') as f: pickle.dump(combined_names, f)

#     global knn, N_NEIGHBORS
#     N_NEIGHBORS = get_n_neighbors(combined_names)
#     knn = KNeighborsClassifier(n_neighbors=N_NEIGHBORS, metric=KNN_METRIC, weights=KNN_WEIGHTS)
#     knn.fit(combined_faces, combined_names)
#     return {"message": f"{name} trained with {len(faces_data)} samples"}

# @app.route('/cameras')
# def camera_list():
#     return jsonify([{"id":i,"active":True,"url":f"http://localhost:5000/video_feed/{i}"} for i in range(4)])

# @app.route('/alert_config')
# def alert_config():
#     """Shows current alert configuration"""
#     from alerts import ALERT_ON, ALERT_COOLDOWN_SECONDS, USE_WHATSAPP, _twilio_available
#     return jsonify({
#         "alert_on":        ALERT_ON,
#         "cooldown_sec":    ALERT_COOLDOWN_SECONDS,
#         "sms_enabled":     _twilio_available,
#         "whatsapp":        USE_WHATSAPP,
#         "voice_enabled":   True,
#     })

# @app.route('/')
# def index():
#     return f"CCTV | {'DNN' if USE_DNN else 'Haar'} | k={N_NEIGHBORS} | alerts active"

# if __name__ == '__main__':
#     print("[INFO] Starting server at http://localhost:5000")
#     app.run(host='0.0.0.0', port=5000, threaded=True)






















#new3

import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import cv2
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import threading
import os
import time

from face_utils import (
    load_detectors, detect_faces, preprocess_face,
    KNN_METRIC, KNN_WEIGHTS, get_n_neighbors
)
from alerts import trigger_alert, ALERT_ON
from camera_config import (
    CAMERAS, STREAM_WIDTH, STREAM_HEIGHT, STREAM_FPS,
    RECONNECT_ATTEMPTS, RECONNECT_DELAY
)

# ================================================================
# LOAD KNN MODEL
# ================================================================
with open('data/names.pkl', 'rb') as f: LABELS = pickle.load(f)
with open('data/faces_data.pkl', 'rb') as f: FACES = pickle.load(f)

N_NEIGHBORS = get_n_neighbors(LABELS)
knn = KNeighborsClassifier(n_neighbors=N_NEIGHBORS, metric=KNN_METRIC, weights=KNN_WEIGHTS)
knn.fit(FACES, LABELS)
print(f"[INFO] KNN loaded — {len(set(LABELS))} people, {len(LABELS)} samples, k={N_NEIGHBORS}")

num_people        = len(set(LABELS))
UNKNOWN_THRESHOLD = 4500 if num_people == 1 else 5000
MIN_DISTANCE_GAP  = 0    if num_people == 1 else 300

# ================================================================
# DETECTORS
# ================================================================
net, haar, USE_DNN = load_detectors()

# ================================================================
# FLASK
# ================================================================
app = Flask(__name__)
CORS(app)

# ================================================================
# PREDICT
# ================================================================
def _predict(face_vec):
    distances, idxs = knn.kneighbors(face_vec, n_neighbors=N_NEIGHBORS)
    min_dist = float(np.min(distances[0]))
    avg_dist = float(np.mean(distances[0]))
    if min_dist > UNKNOWN_THRESHOLD:
        return "Unknown", avg_dist
    if num_people >= 2:
        nbr_labels = [LABELS[i] for i in idxs[0]]
        ld = {}
        for lbl, d in zip(nbr_labels, distances[0]):
            ld.setdefault(lbl, []).append(d)
        sorted_pp = sorted(
            {l: np.mean(v) for l, v in ld.items()}.items(),
            key=lambda kv: kv[1]
        )
        best_name = sorted_pp[0][0]
        gap = (sorted_pp[1][1] - sorted_pp[0][1]) if len(sorted_pp) >= 2 else 999
        if gap < MIN_DISTANCE_GAP:
            return "Unknown", avg_dist
        return best_name, sorted_pp[0][1]
    return knn.predict(face_vec)[0], avg_dist

# ================================================================
# ANNOTATE FRAME
# ================================================================
def annotate_frame(frame, cam_id):
    try:
        faces = detect_faces(frame, net, haar, USE_DNN)
    except Exception:
        faces = []

    for (x1, y1, w, h, _) in faces:
        x2, y2 = x1 + w, y1 + h
        crop   = frame[y1:y2, x1:x2]
        if crop.size == 0: continue
        try:
            vec        = preprocess_face(crop).flatten().reshape(1, -1)
            name, dist = _predict(vec)
        except Exception: continue

        trigger_alert(name, camera_id=cam_id)

        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{name} ({int(dist)})"
        (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
        cv2.rectangle(frame, (x1, y1 - lh - 12), (x1 + lw + 6, y1), color, -1)
        cv2.putText(frame, label, (x1 + 3, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        if name in ALERT_ON:
            cv2.putText(frame, "ALERT", (x1, y2 + 18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return frame

# ================================================================
# NO SIGNAL FRAME
# ================================================================
def make_no_signal_frame(cam_id, reason="No Signal"):
    frame = np.zeros((STREAM_HEIGHT, STREAM_WIDTH, 3), dtype=np.uint8)
    for i in range(0, STREAM_WIDTH,  40):
        cv2.line(frame, (i, 0), (i, STREAM_HEIGHT), (25, 25, 25), 1)
    for i in range(0, STREAM_HEIGHT, 40):
        cv2.line(frame, (0, i), (STREAM_WIDTH, i), (25, 25, 25), 1)
    cam_name = CAMERAS.get(cam_id, {}).get("name", f"Camera {cam_id + 1}")
    cv2.putText(frame, cam_name, (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (80, 80, 80), 1)
    cv2.putText(frame, reason,
                (STREAM_WIDTH // 2 - 120, STREAM_HEIGHT // 2 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (55, 55, 55), 2)
    if "OBS" in reason or "RTMP" in reason or "stream" in reason.lower():
        cv2.putText(frame, "Start OBS → Settings → Stream → Start Streaming",
                    (STREAM_WIDTH // 2 - 190, STREAM_HEIGHT // 2 + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (55, 55, 55), 1)
    return frame

# ================================================================
# OPEN CAPTURE
# KEY FIX: No test read for RTMP — stream must already be open
#          when cap.read() is called in the loop.
#          For RTMP, just check isOpened() and trust the loop.
# ================================================================
def open_capture(cam_type, source):
    try:
        if cam_type == "webcam":
            # Try default backend first (avoids MSMF errors on some systems)
            cap = cv2.VideoCapture(source)
            if not cap.isOpened():
                # Fallback to DSHOW
                cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH,  STREAM_WIDTH)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
                cap.set(cv2.CAP_PROP_FPS, STREAM_FPS)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                # Test read for webcam only
                ret, frame = cap.read()
                if ret and frame is not None:
                    return cap
            cap.release()
            return None

        elif cam_type == "rtmp":
            # Set FFMPEG options for low-latency RTMP BEFORE opening
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
                "fflags=nobuffer;"
                "flags=low_delay;"
                "probesize=32;"
                "analyzeduration=0;"
                "reorder_queue_size=0"
            )
            cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            # DO NOT test read for RTMP here — it blocks if stream just started
            # The capture loop handles failed reads gracefully
            if cap.isOpened():
                print(f"[RTMP] Stream opened: {source}")
                return cap
            cap.release()
            return None

        elif cam_type == "rtsp":
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
                "rtsp_transport=tcp;"
                "fflags=nobuffer;"
                "flags=low_delay"
            )
            cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if not cap.isOpened():
                return None
            ret, frame = cap.read()
            if ret and frame is not None:
                return cap
            cap.release()
            return None

        elif cam_type == "http":
            cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
            if not cap.isOpened():
                return None
            ret, frame = cap.read()
            if ret and frame is not None:
                return cap
            cap.release()
            return None

        elif cam_type == "video":
            if not os.path.exists(str(source)):
                print(f"[ERROR] Video file not found: {source}")
                return None
            cap = cv2.VideoCapture(source)
            return cap if cap.isOpened() else None

    except Exception as e:
        print(f"[ERROR] open_capture({cam_type}): {e}")
        return None

# ================================================================
# CAMERA HANDLER
# ================================================================
class CameraHandler:
    def __init__(self, cam_id, config):
        self.cam_id          = cam_id
        self.cam_type        = config.get("type", "disabled")
        self.source          = config.get("source")
        self.name            = config.get("name", f"Camera {cam_id}")
        self.raw_frame       = None
        self.annotated_frame = None
        self.lock            = threading.Lock()
        self.connected       = False
        self.status          = "Waiting..."

        if self.cam_type != "disabled":
            threading.Thread(target=self._capture_loop, daemon=True).start()
            threading.Thread(target=self._process_loop, daemon=True).start()
            print(f"[CAM {cam_id}] {self.name} | {self.cam_type} | {self.source}")
        else:
            self.status = "Disabled"
            print(f"[CAM {cam_id}] {self.name} — DISABLED")

    def _capture_loop(self):
        fail_count = 0
        while True:
            if self.cam_type == "rtmp":
                self.status = "Waiting for OBS stream..."
            else:
                self.status = f"Connecting... (attempt {fail_count + 1})"

            cap = open_capture(self.cam_type, self.source)

            if cap is None:
                fail_count += 1
                self.connected = False
                wait = 5 if self.cam_type == "rtmp" else RECONNECT_DELAY
                time.sleep(wait)
                continue

            # Connected
            self.connected = True
            self.status    = "Live"
            fail_count     = 0
            print(f"[CAM {self.cam_id}] ✅ Live — {self.name}")

            consecutive_fails = 0
            while True:
                ret, frame = cap.read()

                if not ret or frame is None:
                    consecutive_fails += 1
                    # For RTMP: allow a few failed reads before giving up
                    # (stream may stutter briefly)
                    if self.cam_type in ("rtmp", "rtsp") and consecutive_fails < 10:
                        time.sleep(0.1)
                        continue
                    # Video file: loop
                    if self.cam_type == "video":
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        consecutive_fails = 0
                        continue
                    # Give up and reconnect
                    self.connected = False
                    self.status    = "Stream lost — reconnecting..."
                    print(f"[CAM {self.cam_id}] Stream lost")
                    break

                consecutive_fails = 0
                with self.lock:
                    self.raw_frame = frame

            cap.release()
            time.sleep(RECONNECT_DELAY)

    def _process_loop(self):
        while True:
            raw = None
            with self.lock:
                if self.raw_frame is not None:
                    raw = self.raw_frame.copy()
            if raw is None:
                time.sleep(0.02)
                continue

            annotated = annotate_frame(raw, self.cam_id)
            tag = "DNN" if USE_DNN else "HAAR"
            cv2.putText(annotated, f"{self.name} [{tag}]",
                        (10, annotated.shape[0] - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (120, 120, 120), 1)
            with self.lock:
                self.annotated_frame = annotated

    def get_frame(self):
        with self.lock:
            if self.annotated_frame is not None:
                return self.annotated_frame.copy()
        return make_no_signal_frame(self.cam_id, self.status)

# ================================================================
# INIT CAMERAS
# ================================================================
cameras = {
    cam_id: CameraHandler(cam_id, cfg)
    for cam_id, cfg in CAMERAS.items()
}

# ================================================================
# FRAME GENERATOR
# ================================================================
def generate_frames(cam_id):
    handler = cameras.get(cam_id)
    while True:
        frame = (handler.get_frame() if handler
                 else make_no_signal_frame(cam_id, "Not Configured"))
        ret, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not ret: continue
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' +
               buf.tobytes() + b'\r\n')

# ================================================================
# ROUTES
# ================================================================
@app.route('/video_feed/<int:cam_id>')
def video_feed(cam_id):
    return Response(generate_frames(cam_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cameras')
def camera_list():
    return jsonify([{
        "id":     cam_id,
        "name":   h.name,
        "type":   h.cam_type,
        "active": h.connected or h.cam_type == "video",
        "status": h.status,
        "url":    f"http://localhost:5000/video_feed/{cam_id}"
    } for cam_id, h in cameras.items()])

@app.route('/camera_status')
def camera_status():
    return jsonify({
        cam_id: {
            "connected": h.connected,
            "status":    h.status,
            "type":      h.cam_type,
            "name":      h.name,
        }
        for cam_id, h in cameras.items()
    })

@app.route('/upload_faces', methods=['POST'])
def upload_faces():
    name = request.form.get('name')
    if not name: return {"error": "Name required"}, 400
    files = request.files.getlist('images')
    if len(files) < 3: return {"error": "Upload at least 3 images"}, 400

    faces_data = []
    for file in files:
        npimg = np.frombuffer(file.read(), np.uint8)
        img   = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if img is None: continue
        for (x1, y1, w, h, _) in detect_faces(img, net, haar, USE_DNN):
            crop = img[y1:y1 + h, x1:x1 + w]
            if crop.size > 0:
                faces_data.append(preprocess_face(crop).flatten())

    if not faces_data: return {"error": "No face detected"}, 400

    faces_data = np.array(faces_data)
    names_path, faces_path = 'data/names.pkl', 'data/faces_data.pkl'
    if os.path.exists(faces_path):
        with open(faces_path, 'rb') as f: ef = pickle.load(f)
        with open(names_path,  'rb') as f: en = pickle.load(f)
        combined_faces = np.append(ef, faces_data, axis=0)
        combined_names = en + [name] * len(faces_data)
    else:
        combined_faces = faces_data
        combined_names = [name] * len(faces_data)

    with open(faces_path, 'wb') as f: pickle.dump(combined_faces, f)
    with open(names_path,  'wb') as f: pickle.dump(combined_names, f)

    global knn, N_NEIGHBORS
    N_NEIGHBORS = get_n_neighbors(combined_names)
    knn = KNeighborsClassifier(
        n_neighbors=N_NEIGHBORS, metric=KNN_METRIC, weights=KNN_WEIGHTS
    )
    knn.fit(combined_faces, combined_names)
    return {"message": f"{name} trained with {len(faces_data)} samples"}

@app.route('/')
def index():
    active = sum(1 for h in cameras.values() if h.connected)
    return (f"CCTV | {active}/{len(cameras)} live | "
            f"{'DNN' if USE_DNN else 'Haar'} | k={N_NEIGHBORS}")

if __name__ == '__main__':
    print(f"\n[INFO] {len(cameras)} camera slots configured")
    print("[INFO] RTMP: start node rtmp_server.js first, then OBS, then this")
    print("[INFO] http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, threaded=True)