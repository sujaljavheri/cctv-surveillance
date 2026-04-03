# from sklearn.neighbors import KNeighborsClassifier
# import cv2
# import pickle
# import numpy as np
# import os
# import csv
# import time
# from datetime import datetime
# from collections import deque, Counter
# from win32com.client import Dispatch

# def speak(str1):
#     speaker = Dispatch(("SAPI.SpVoice"))
#     speaker.Speak(str1)

# # ================================================================
# # IMPROVEMENT 1: Better face preprocessing
# # - Histogram equalization improves contrast in different lighting
# # - Matches how we save in add_faces.py (must be identical)
# # ================================================================
# def preprocess_face(crop_img):
#     # Convert to grayscale for better feature extraction
#     gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
#     # Equalize histogram to normalize lighting differences
#     equalized = cv2.equalizeHist(gray)
#     # Resize to 50x50
#     resized = cv2.resize(equalized, (50, 50))
#     return resized.flatten().reshape(1, -1)

# # ================================================================
# # IMPROVEMENT 2: Liveness using local variance (more robust)
# # ================================================================
# def liveness_score(face_img):
#     gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
#     # Use local standard deviation — better than global Laplacian
#     local_std = cv2.meanStdDev(gray)[1][0][0]
#     lap = cv2.Laplacian(gray, cv2.CV_64F).var()
#     # Combine both scores
#     combined = (local_std * 0.5) + (lap * 0.5)
#     return combined

# # ================================================================
# # IMPROVEMENT 3: IoU — track which face box matches which tracker
# # Prevents IDs jumping between faces when positions overlap
# # ================================================================
# def iou(boxA, boxB):
#     xA = max(boxA[0], boxB[0])
#     yA = max(boxA[1], boxB[1])
#     xB = min(boxA[0]+boxA[2], boxB[0]+boxB[2])
#     yB = min(boxA[1]+boxA[3], boxB[1]+boxB[3])
#     interArea = max(0, xB - xA) * max(0, yB - yA)
#     if interArea == 0:
#         return 0.0
#     boxAArea = boxA[2] * boxA[3]
#     boxBArea = boxB[2] * boxB[3]
#     return interArea / float(boxAArea + boxBArea - interArea)

# # ================================================================
# # Load model
# # ================================================================
# video = cv2.VideoCapture(0)
# facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# with open('data/names.pkl', 'rb') as w:
#     LABELS = pickle.load(w)
# with open('data/faces_data.pkl', 'rb') as f:
#     FACES = pickle.load(f)

# print('Shape of Faces matrix --> ', FACES.shape)
# print('Unique people trained:', set(LABELS))

# # ================================================================
# # IMPROVEMENT 4: Use weighted KNN with more neighbors
# # More neighbors = more stable predictions, weighted = closer
# # neighbors count more
# # ================================================================
# n_neighbors = min(7, len(set(LABELS)) * 3)  # auto scale
# knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights='distance', metric='euclidean')
# knn.fit(FACES, LABELS)

# imgBackground = cv2.imread("background.png")
# COL_NAMES = ['NAME', 'TIME']

# # ================================================================
# # IMPROVEMENT 5: Temporal voting buffer
# # Instead of trusting 1 frame, we collect predictions over the
# # last N frames per face position and vote on the most common one
# # This eliminates flickering and wrong-frame predictions
# # ================================================================
# VOTE_BUFFER_SIZE = 10       # frames to vote over
# face_vote_buffers = {}      # key = face_id, value = deque of predictions

# # ================================================================
# # THRESHOLDS — tune using debug values on screen
# # CONFIDENCE_THRESHOLD: set to ~3x your known face's Dist value
# # LIVENESS_THRESHOLD:   set to ~half your real face's Lap value
# # ================================================================
# CONFIDENCE_THRESHOLD = 3500
# LIVENESS_THRESHOLD   = 12   # combined liveness score cutoff

# attendance_list = []
# face_id_counter = 0
# tracked_faces = {}   # face_id -> last known box

# while True:
#     ret, frame = video.read()
#     if not ret:
#         break

#     # ---- IMPROVEMENT 6: Denoise frame slightly ----
#     frame_clean = cv2.GaussianBlur(frame, (3, 3), 0)

#     gray = cv2.cvtColor(frame_clean, cv2.COLOR_BGR2GRAY)
#     faces = facedetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(60, 60))

#     attendance_list = []
#     current_face_ids = []

#     for (x, y, w, h) in faces:
#         crop_img = frame[y:y+h, x:x+w, :]

#         # --- Match to existing tracked face using IoU ---
#         matched_id = None
#         best_iou = 0.3  # minimum IoU to consider a match
#         for fid, fbox in tracked_faces.items():
#             score = iou((x, y, w, h), fbox)
#             if score > best_iou:
#                 best_iou = score
#                 matched_id = fid

#         if matched_id is None:
#             # New face — assign new ID
#             face_id_counter += 1
#             matched_id = face_id_counter
#             face_vote_buffers[matched_id] = deque(maxlen=VOTE_BUFFER_SIZE)

#         tracked_faces[matched_id] = (x, y, w, h)
#         current_face_ids.append(matched_id)

#         # --- Liveness check ---
#         live_score = liveness_score(crop_img)
#         is_live = live_score > LIVENESS_THRESHOLD

#         # --- KNN prediction with preprocessing ---
#         processed = preprocess_face(crop_img)
#         distances, indices = knn.kneighbors(processed)
#         raw_prediction = knn.predict(processed)[0]
#         avg_distance = np.mean(distances[0])
#         min_distance = np.min(distances[0])

#         # --- Add to vote buffer ---
#         if not is_live:
#             frame_label = "Spoof/Photo"
#         elif avg_distance > CONFIDENCE_THRESHOLD:
#             frame_label = "Unknown"
#         else:
#             frame_label = str(raw_prediction)

#         face_vote_buffers[matched_id].append(frame_label)

#         # --- IMPROVEMENT 5: Vote on final label ---
#         vote_counts = Counter(face_vote_buffers[matched_id])
#         predicted_name = vote_counts.most_common(1)[0][0]
#         vote_confidence = vote_counts.most_common(1)[0][1] / len(face_vote_buffers[matched_id])

#         # --- Color coding ---
#         if predicted_name == "Spoof/Photo":
#             box_color = (0, 165, 255)   # Orange
#         elif predicted_name == "Unknown":
#             box_color = (0, 0, 255)     # Red
#         else:
#             # Green intensity based on vote confidence
#             green = int(150 + 105 * vote_confidence)
#             box_color = (0, green, 0)

#         ts = time.time()
#         date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
#         timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
#         attendance_list.append([predicted_name, str(timestamp)])

#         # --- Draw UI ---
#         cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
#         cv2.rectangle(frame, (x, y-45), (x+w, y), box_color, -1)
#         cv2.putText(frame, predicted_name, (x+4, y-12),
#                     cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)

#         # Confidence bar inside the top banner
#         conf_bar_w = int(w * vote_confidence)
#         cv2.rectangle(frame, (x, y-5), (x+conf_bar_w, y), (255, 255, 255), -1)

#         # Debug info (remove once happy with results)
#         cv2.putText(frame, f"D:{int(avg_distance)} L:{int(live_score)}", (x, y+h+18),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
#         cv2.putText(frame, f"Vote:{int(vote_confidence*100)}% [{len(face_vote_buffers[matched_id])}f]",
#                     (x, y+h+34), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 200, 0), 1)

#     # Clean up stale face trackers (faces no longer visible)
#     stale_ids = [fid for fid in tracked_faces if fid not in current_face_ids]
#     for fid in stale_ids:
#         del tracked_faces[fid]
#         if fid in face_vote_buffers:
#             del face_vote_buffers[fid]

#     imgBackground[162:162 + 480, 55:55 + 640] = frame
#     cv2.imshow("Frame", imgBackground)
#     k = cv2.waitKey(1)

#     if k == ord('o'):
#         ts = time.time()
#         date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
#         exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
#         speak("Person detected..")
#         time.sleep(2)
#         with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
#             writer = csv.writer(csvfile)
#             if not exist:
#                 writer.writerow(COL_NAMES)
#             for entry in attendance_list:
#                 if entry[0] not in ["Unknown", "Spoof/Photo"]:
#                     writer.writerow(entry)

#     if k == ord('q'):
#         break

# video.release()
# cv2.destroyAllWindows()
























# from sklearn.neighbors import KNeighborsClassifier
# import cv2
# import pickle
# import numpy as np
# import os
# import csv
# import time
# from datetime import datetime
# from collections import deque, Counter

# # ================================================================
# # TTS — optional
# # ================================================================
# try:
#     from win32com.client import Dispatch
#     def speak(text):
#         Dispatch("SAPI.SpVoice").Speak(text)
# except ImportError:
#     def speak(text):
#         print(f"[SPEAK] {text}")

# # ================================================================
# # FACE DETECTOR SETUP
# # ================================================================
# haar = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
# if haar.empty():
#     raise RuntimeError("[FATAL] haarcascade_frontalface_default.xml not found in data/")

# DNN_PROTO = "data/deploy.prototxt"
# DNN_MODEL = "data/res10_300x300_ssd_iter_140000.caffemodel"
# USE_DNN   = False
# net       = None

# if os.path.exists(DNN_PROTO) and os.path.exists(DNN_MODEL):
#     if os.path.getsize(DNN_MODEL) > 5_000_000:
#         try:
#             loaded = cv2.dnn.readNetFromCaffe(DNN_PROTO, DNN_MODEL)
#             dummy  = np.zeros((300, 300, 3), dtype=np.uint8)
#             blob   = cv2.dnn.blobFromImage(dummy, 1.0, (300, 300), (104.0, 177.0, 123.0))
#             loaded.setInput(blob)
#             loaded.forward()
#             net     = loaded
#             USE_DNN = True
#             print("[INFO] DNN detector loaded and verified OK")
#         except Exception as e:
#             print(f"[WARN] DNN failed: {e} — using Haar only")
#     else:
#         print("[WARN] Caffemodel too small — re-run download_models.py")
# else:
#     print("[WARN] DNN files not found — using Haar only")

# print(f"[INFO] Active detector: {'DNN' if USE_DNN else 'Haar Cascade'}")

# # ================================================================
# # TUNING
# # ----------------------------------------------------------------
# # DNN_CONF_STRICT  : used first — high precision, avoids false positives
# # DNN_CONF_RELAXED : fallback — lower threshold to catch side angles
# #                    only used when strict pass finds nothing
# #
# # UNKNOWN_THRESHOLD: KNN distance above this = "Unknown"
# # MIN_BOX_AREA     : ignore detections smaller than this (px²)
# #                    prevents tiny false-positive boxes
# # ================================================================
# DNN_CONF_STRICT   = 0.80   # pass 1: strict, frontal
# DNN_CONF_RELAXED  = 0.45   # pass 2: relaxed, catches side angles
# MIN_BOX_AREA      = 2500   # 50×50 px minimum face box
# UNKNOWN_THRESHOLD = 5000
# MIN_DISTANCE_GAP  = 300
# LIVENESS_THRESHOLD = 6
# VOTE_BUFFER       = 15


# # ================================================================
# # PREPROCESSING — must EXACTLY match add_faces.py
# # ================================================================
# def preprocess_face(crop):
#     gray       = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
#     equalized  = cv2.equalizeHist(gray)
#     resized    = cv2.resize(equalized, (50, 50))
#     normalized = resized.astype(np.float32) / 255.0
#     return normalized.flatten().reshape(1, -1)


# # ================================================================
# # TWO-PASS DNN DETECTION
# # Pass 1 — strict confidence (frontal faces, no false positives)
# # Pass 2 — relaxed confidence (side angles) BUT filters small/noisy boxes
# #           using aspect ratio + minimum area checks
# # ================================================================
# def detect_faces_dnn(frame):
#     h, w = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(
#         cv2.resize(frame, (300, 300)), 1.0,
#         (300, 300), (104.0, 177.0, 123.0)
#     )
#     net.setInput(blob)
#     raw = net.forward()

#     def parse_detections(threshold):
#         boxes = []
#         for i in range(raw.shape[2]):
#             conf = raw[0, 0, i, 2]
#             if conf < threshold:
#                 continue
#             box = raw[0, 0, i, 3:7] * np.array([w, h, w, h])
#             x1, y1, x2, y2 = box.astype(int)
#             x1, y1 = max(0, x1), max(0, y1)
#             x2, y2 = min(w, x2), min(h, y2)
#             bw, bh = x2 - x1, y2 - y1
#             # Filter: too small or extreme aspect ratio (not a face)
#             if bw * bh < MIN_BOX_AREA:
#                 continue
#             aspect = bw / max(bh, 1)
#             if aspect < 0.3 or aspect > 3.0:
#                 continue
#             boxes.append((x1, y1, bw, bh, float(conf)))
#         return boxes

#     # Pass 1: strict
#     strict = parse_detections(DNN_CONF_STRICT)
#     if strict:
#         return strict

#     # Pass 2: relaxed (only when nothing found in strict)
#     relaxed = parse_detections(DNN_CONF_RELAXED)
#     return relaxed


# # ================================================================
# # HAAR DETECTION — multi-scale
# # ================================================================
# def detect_faces_haar(frame):
#     gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray_e = cv2.equalizeHist(gray)
#     for scale, neighbors, minsize in [
#         (1.1, 6, (80, 80)),
#         (1.1, 4, (60, 60)),
#         (1.05, 3, (50, 50)),
#     ]:
#         faces = haar.detectMultiScale(
#             gray_e, scaleFactor=scale,
#             minNeighbors=neighbors, minSize=minsize,
#             flags=cv2.CASCADE_SCALE_IMAGE
#         )
#         if len(faces) > 0:
#             return [(x, y, w, h, 0.9) for (x, y, w, h) in faces]
#     return []


# def detect_faces(frame):
#     if USE_DNN and net is not None:
#         try:
#             result = detect_faces_dnn(frame)
#             if result:
#                 return result
#         except Exception as e:
#             print(f"[WARN] DNN error: {e}")
#     return detect_faces_haar(frame)


# # ================================================================
# # LIVENESS
# # ================================================================
# def liveness_score(face_img):
#     gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
#     std  = cv2.meanStdDev(gray)[1][0][0]
#     lap  = cv2.Laplacian(gray, cv2.CV_64F).var()
#     return std * 0.5 + lap * 0.5


# # ================================================================
# # IoU — face tracker
# # ================================================================
# def iou(a, b):
#     xA    = max(a[0], b[0])
#     yA    = max(a[1], b[1])
#     xB    = min(a[0]+a[2], b[0]+b[2])
#     yB    = min(a[1]+a[3], b[1]+b[3])
#     inter = max(0, xB-xA) * max(0, yB-yA)
#     if inter == 0:
#         return 0.0
#     return inter / float(a[2]*a[3] + b[2]*b[3] - inter)


# # ================================================================
# # LOAD DATA & TRAIN KNN
# # ================================================================
# video = cv2.VideoCapture(0)
# video.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
# video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# with open('data/names.pkl', 'rb') as f:
#     LABELS = pickle.load(f)
# with open('data/faces_data.pkl', 'rb') as f:
#     FACES = pickle.load(f)

# unique_people = list(set(LABELS))
# num_people    = len(unique_people)
# print(f"[INFO] Faces shape  : {FACES.shape}")
# print(f"[INFO] People       : {unique_people}")
# print(f"[INFO] Total samples: {len(LABELS)}")

# if num_people == 1:
#     UNKNOWN_THRESHOLD = 4500
#     MIN_DISTANCE_GAP  = 0
#     print("[INFO] Single-person mode — strict threshold")
# else:
#     UNKNOWN_THRESHOLD = 5000
#     MIN_DISTANCE_GAP  = 300
#     print(f"[INFO] Multi-person mode — gap={MIN_DISTANCE_GAP}")

# n_neighbors = min(max(5, num_people * 3), len(LABELS))
# knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights='distance', metric='euclidean')
# knn.fit(FACES, LABELS)
# print(f"[INFO] KNN ready — k={n_neighbors}")

# # ================================================================
# # STATE
# # ================================================================
# COL_NAMES         = ['NAME', 'TIME']
# face_vote_buffers = {}
# face_id_counter   = 0
# tracked_faces     = {}
# attendance_list   = []
# show_debug        = True

# imgBackground = cv2.imread("background.png") if os.path.exists("background.png") else None

# print(f"\n[READY] Press 'o' = attendance  |  'd' = debug  |  'q' = quit")
# print(f"[READY] Detection: strict={DNN_CONF_STRICT}, relaxed={DNN_CONF_RELAXED}\n")

# # ================================================================
# # MAIN LOOP
# # ================================================================
# while True:
#     ret, frame = video.read()
#     if not ret:
#         break

#     faces           = detect_faces(frame)
#     attendance_list = []
#     current_ids     = []

#     for (x, y, w, h, det_conf) in faces:
#         x,  y  = max(0, x),  max(0, y)
#         x2, y2 = min(frame.shape[1], x+w), min(frame.shape[0], y+h)
#         w,  h  = x2-x, y2-y
#         crop   = frame[y:y2, x:x2]
#         if crop.size == 0:
#             continue

#         # Track face
#         matched_id = None
#         best_score = 0.25
#         for fid, fbox in tracked_faces.items():
#             s = iou((x, y, w, h), fbox)
#             if s > best_score:
#                 best_score, matched_id = s, fid
#         if matched_id is None:
#             face_id_counter += 1
#             matched_id = face_id_counter
#             face_vote_buffers[matched_id] = deque(maxlen=VOTE_BUFFER)
#         tracked_faces[matched_id] = (x, y, w, h)
#         current_ids.append(matched_id)

#         # Liveness
#         live_score = liveness_score(crop)
#         is_live    = live_score > LIVENESS_THRESHOLD

#         # KNN
#         processed       = preprocess_face(crop)
#         distances, idxs = knn.kneighbors(processed, n_neighbors=n_neighbors)
#         min_dist        = float(np.min(distances[0]))
#         raw_pred        = knn.predict(processed)[0]

#         # Identity decision
#         if not is_live:
#             frame_label = "Spoof/Photo"
#         elif min_dist > UNKNOWN_THRESHOLD:
#             frame_label = "Unknown"
#         elif num_people >= 2:
#             neighbour_labels = [LABELS[i] for i in idxs[0]]
#             label_dists = {}
#             for lbl, dist in zip(neighbour_labels, distances[0]):
#                 label_dists.setdefault(lbl, []).append(dist)
#             avg_pp      = {lbl: np.mean(d) for lbl, d in label_dists.items()}
#             sorted_pp   = sorted(avg_pp.items(), key=lambda kv: kv[1])
#             best_name   = sorted_pp[0][0]
#             if len(sorted_pp) >= 2:
#                 gap = sorted_pp[1][1] - sorted_pp[0][1]
#                 frame_label = best_name if gap >= MIN_DISTANCE_GAP else "Unknown"
#             else:
#                 frame_label = best_name
#         else:
#             frame_label = str(raw_pred)

#         # Vote buffer
#         face_vote_buffers[matched_id].append(frame_label)
#         counts         = Counter(face_vote_buffers[matched_id])
#         predicted_name = counts.most_common(1)[0][0]
#         vote_conf      = counts.most_common(1)[0][1] / len(face_vote_buffers[matched_id])

#         # Colour
#         if predicted_name == "Spoof/Photo":
#             color = (0, 165, 255)
#         elif predicted_name == "Unknown":
#             color = (0, 0, 255)
#         else:
#             color = (0, int(150 + 105 * vote_conf), 0)

#         attendance_list.append([predicted_name, datetime.now().strftime("%H:%M:%S")])

#         # Draw
#         cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
#         banner_y = max(y - 40, 0)
#         cv2.rectangle(frame, (x, banner_y), (x+w, y), color, -1)
#         cv2.putText(frame, predicted_name, (x+4, y-8),
#                     cv2.FONT_HERSHEY_COMPLEX, 0.72, (255, 255, 255), 1)
#         cv2.rectangle(frame, (x, y-4), (x + int(w*vote_conf), y), (255,255,255), -1)

#         if show_debug:
#             # Shows: Distance | Liveness | Det-confidence | Vote%
#             cv2.putText(frame, f"D:{int(min_dist)} L:{int(live_score)} DC:{det_conf:.2f}",
#                         (x, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0,255,255), 1)
#             cv2.putText(frame, f"V:{int(vote_conf*100)}% [{len(face_vote_buffers[matched_id])}f]",
#                         (x, y+h+28), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255,200,0), 1)

#     # Cleanup stale trackers
#     for fid in [f for f in list(tracked_faces) if f not in current_ids]:
#         del tracked_faces[fid]
#         face_vote_buffers.pop(fid, None)

#     # Overlay detector mode
#     tag = "DNN" if USE_DNN else "HAAR"
#     cv2.putText(frame, f"[{tag}] strict={DNN_CONF_STRICT} relaxed={DNN_CONF_RELAXED}",
#                 (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (180,180,0), 1)

#     if imgBackground is not None:
#         try:
#             imgBackground[162:162+480, 55:55+640] = frame
#             cv2.imshow("Face Recognition", imgBackground)
#         except Exception:
#             cv2.imshow("Face Recognition", frame)
#     else:
#         cv2.imshow("Face Recognition", frame)

#     k = cv2.waitKey(1)

#     if k == ord('d'):
#         show_debug = not show_debug

#     if k == ord('o'):
#         date  = datetime.now().strftime("%d-%m-%Y")
#         fpath = f"Attendance/Attendance_{date}.csv"
#         os.makedirs("Attendance", exist_ok=True)
#         exists = os.path.isfile(fpath)
#         speak("Attendance marked")
#         with open(fpath, "+a", newline='') as f:
#             writer = csv.writer(f)
#             if not exists:
#                 writer.writerow(COL_NAMES)
#             for entry in attendance_list:
#                 if entry[0] not in ["Unknown", "Spoof/Photo"]:
#                     writer.writerow(entry)
#         saved = [e[0] for e in attendance_list if e[0] not in ["Unknown", "Spoof/Photo"]]
#         print(f"[INFO] Attendance saved: {saved}")

#     if k == ord('q'):
#         break

# video.release()
# cv2.destroyAllWindows()


























# //new

from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
from datetime import datetime
from collections import deque, Counter
import time

from face_utils import load_detectors, detect_faces, preprocess_face

# ================================================================
# TTS — optional
# ================================================================
try:
    from win32com.client import Dispatch
    def speak(text): Dispatch("SAPI.SpVoice").Speak(text)
except ImportError:
    def speak(text): print(f"[SPEAK] {text}")

# ================================================================
# DETECTORS
# ================================================================
net, haar, USE_DNN = load_detectors()

# ================================================================
# TUNING
# ================================================================
UNKNOWN_THRESHOLD  = 5000   # KNN distance — above = "Unknown"
MIN_DISTANCE_GAP   = 300    # gap between best & 2nd person avg dist
LIVENESS_THRESHOLD = 6      # below = photo/spoof
VOTE_BUFFER        = 15     # frames to average prediction over

# ================================================================
# LOAD DATA & TRAIN KNN
# ================================================================
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

with open('data/names.pkl', 'rb') as f: LABELS = pickle.load(f)
with open('data/faces_data.pkl', 'rb') as f: FACES = pickle.load(f)

unique_people = list(set(LABELS))
num_people    = len(unique_people)
print(f"[INFO] Faces shape  : {FACES.shape}")
print(f"[INFO] People       : {unique_people}")
print(f"[INFO] Total samples: {len(LABELS)}")

if num_people == 1:
    UNKNOWN_THRESHOLD = 4500
    MIN_DISTANCE_GAP  = 0
    print("[INFO] Single-person mode")
else:
    print(f"[INFO] Multi-person mode — gap={MIN_DISTANCE_GAP}")

n_neighbors = min(max(5, num_people * 3), len(LABELS))
knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights='distance', metric='euclidean')
knn.fit(FACES, LABELS)
print(f"[INFO] KNN ready — k={n_neighbors}")

# ================================================================
# HELPERS
# ================================================================
def liveness_score(face_img):
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    return cv2.meanStdDev(gray)[1][0][0] * 0.5 + cv2.Laplacian(gray, cv2.CV_64F).var() * 0.5

def iou(a, b):
    xA = max(a[0], b[0]); yA = max(a[1], b[1])
    xB = min(a[0]+a[2], b[0]+b[2]); yB = min(a[1]+a[3], b[1]+b[3])
    inter = max(0, xB-xA) * max(0, yB-yA)
    return 0.0 if inter == 0 else inter / float(a[2]*a[3] + b[2]*b[3] - inter)

# ================================================================
# STATE
# ================================================================
face_vote_buffers = {}
face_id_counter   = 0
tracked_faces     = {}
attendance_list   = []
show_debug        = True
imgBackground     = cv2.imread("background.png") if os.path.exists("background.png") else None

print(f"\n[READY] 'o'=attendance  'd'=debug  'q'=quit")

# ================================================================
# MAIN LOOP
# ================================================================
while True:
    ret, frame = video.read()
    if not ret: break

    faces           = detect_faces(frame, net, haar, USE_DNN)
    attendance_list = []
    current_ids     = []

    for (x, y, w, h, det_conf) in faces:
        x,  y  = max(0, x), max(0, y)
        x2, y2 = min(frame.shape[1], x+w), min(frame.shape[0], y+h)
        w,  h  = x2-x, y2-y
        crop   = frame[y:y2, x:x2]
        if crop.size == 0: continue

        # Track face across frames
        matched_id = None
        best_score = 0.25
        for fid, fbox in tracked_faces.items():
            s = iou((x, y, w, h), fbox)
            if s > best_score: best_score, matched_id = s, fid
        if matched_id is None:
            face_id_counter += 1
            matched_id = face_id_counter
            face_vote_buffers[matched_id] = deque(maxlen=VOTE_BUFFER)
        tracked_faces[matched_id] = (x, y, w, h)
        current_ids.append(matched_id)

        # Liveness
        live_score = liveness_score(crop)
        is_live    = live_score > LIVENESS_THRESHOLD

        # KNN — preprocess_face returns 2D, flatten for knn
        processed       = preprocess_face(crop).flatten().reshape(1, -1)
        distances, idxs = knn.kneighbors(processed, n_neighbors=n_neighbors)
        min_dist        = float(np.min(distances[0]))
        raw_pred        = knn.predict(processed)[0]

        # Identity decision
        if not is_live:
            frame_label = "Spoof/Photo"
        elif min_dist > UNKNOWN_THRESHOLD:
            frame_label = "Unknown"
        elif num_people >= 2:
            nbr_labels = [LABELS[i] for i in idxs[0]]
            ld = {}
            for lbl, d in zip(nbr_labels, distances[0]):
                ld.setdefault(lbl, []).append(d)
            sorted_pp = sorted({l: np.mean(v) for l,v in ld.items()}.items(), key=lambda kv: kv[1])
            best_name = sorted_pp[0][0]
            gap = (sorted_pp[1][1] - sorted_pp[0][1]) if len(sorted_pp) >= 2 else 999
            frame_label = best_name if gap >= MIN_DISTANCE_GAP else "Unknown"
        else:
            frame_label = str(raw_pred)

        # Temporal vote
        face_vote_buffers[matched_id].append(frame_label)
        counts         = Counter(face_vote_buffers[matched_id])
        predicted_name = counts.most_common(1)[0][0]
        vote_conf      = counts.most_common(1)[0][1] / len(face_vote_buffers[matched_id])

        # Color
        color = (0,165,255) if predicted_name=="Spoof/Photo" else \
                (0,0,255)   if predicted_name=="Unknown"     else \
                (0, int(150+105*vote_conf), 0)

        attendance_list.append([predicted_name, datetime.now().strftime("%H:%M:%S")])

        # Draw
        cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
        banner_y = max(y-40, 0)
        cv2.rectangle(frame, (x, banner_y), (x+w, y), color, -1)
        cv2.putText(frame, predicted_name, (x+4, y-8),
                    cv2.FONT_HERSHEY_COMPLEX, 0.72, (255,255,255), 1)
        cv2.rectangle(frame, (x, y-4), (x+int(w*vote_conf), y), (255,255,255), -1)

        if show_debug:
            cv2.putText(frame, f"D:{int(min_dist)} L:{int(live_score)} DC:{det_conf:.2f}",
                        (x, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0,255,255), 1)
            cv2.putText(frame, f"V:{int(vote_conf*100)}% [{len(face_vote_buffers[matched_id])}f]",
                        (x, y+h+28), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255,200,0), 1)

    # Cleanup stale trackers
    for fid in [f for f in list(tracked_faces) if f not in current_ids]:
        del tracked_faces[fid]; face_vote_buffers.pop(fid, None)

    tag = "DNN" if USE_DNN else "HAAR"
    cv2.putText(frame, f"[{tag}]", (10, frame.shape[0]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180,180,0), 1)

    if imgBackground is not None:
        try:
            imgBackground[162:162+480, 55:55+640] = frame
            cv2.imshow("Face Recognition", imgBackground)
        except Exception:
            cv2.imshow("Face Recognition", frame)
    else:
        cv2.imshow("Face Recognition", frame)

    k = cv2.waitKey(1)
    if k == ord('d'): show_debug = not show_debug
    if k == ord('o'):
        date  = datetime.now().strftime("%d-%m-%Y")
        fpath = f"Attendance/Attendance_{date}.csv"
        os.makedirs("Attendance", exist_ok=True)
        exists = os.path.isfile(fpath)
        speak("Attendance marked")
        with open(fpath, "+a", newline='') as f:
            writer = csv.writer(f)
            if not exists: writer.writerow(['NAME','TIME'])
            for e in attendance_list:
                if e[0] not in ["Unknown","Spoof/Photo"]: writer.writerow(e)
        print(f"[INFO] Saved: {[e[0] for e in attendance_list if e[0] not in ['Unknown','Spoof/Photo']]}")
    if k == ord('q'): break

video.release()
cv2.destroyAllWindows()
