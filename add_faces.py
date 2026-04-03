# import cv2
# import pickle
# import numpy as np
# import os

# video = cv2.VideoCapture(0)
# facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# SAMPLE_COUNT = 30
# FEATURE_SIZE = 2500  # grayscale 50x50 = 2500 features

# # ================================================================
# # MUST MATCH test.py preprocess_face() exactly!
# # ================================================================
# def preprocess_face(crop_img):
#     gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
#     equalized = cv2.equalizeHist(gray)
#     resized = cv2.resize(equalized, (50, 50))
#     return resized  # 2D array, flattened later

# faces_data = []
# i = 0

# name = input("Enter Your Name: ")
# print(f"[INFO] Collecting {SAMPLE_COUNT} samples for '{name}'.")
# print("[INFO] Look at the camera from different angles and distances!")

# while True:
#     ret, frame = video.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = facedetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(60, 60))

#     for (x, y, w, h) in faces:
#         crop_img = frame[y:y+h, x:x+w, :]
#         processed = preprocess_face(crop_img)

#         if len(faces_data) < SAMPLE_COUNT and i % 5 == 0:
#             faces_data.append(processed)
#         i += 1

#         progress = len(faces_data)
#         cv2.putText(frame, f"Samples: {progress}/{SAMPLE_COUNT}", (30, 50),
#                     cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)

#         bar_width = int((progress / SAMPLE_COUNT) * 580)
#         cv2.rectangle(frame, (30, 430), (610, 460), (50, 50, 50), -1)
#         cv2.rectangle(frame, (30, 430), (30 + bar_width, 460), (50, 200, 50), -1)

#         tips = ["Look straight", "Tilt left", "Tilt right", "Move closer", "Move farther"]
#         tip = tips[(progress // 6) % len(tips)]
#         cv2.putText(frame, tip, (30, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 200), 2)

#     cv2.imshow("Collecting Faces - Press Q to quit", frame)
#     k = cv2.waitKey(1)
#     if k == ord('q') or len(faces_data) == SAMPLE_COUNT:
#         break

# video.release()
# cv2.destroyAllWindows()

# if len(faces_data) == 0:
#     print("[ERROR] No face samples collected. Exiting.")
#     exit()

# print(f"[INFO] Collected {len(faces_data)} samples for '{name}'")

# # Flatten to (N, 2500)
# faces_data = np.array(faces_data).reshape(len(faces_data), -1)
# print(f"[INFO] New data shape: {faces_data.shape}")

# # ================================================================
# # SAFETY CHECK: if existing pkl has different feature size,
# # warn user and exit cleanly instead of crashing
# # ================================================================
# names_path = 'data/names.pkl'
# faces_path = 'data/faces_data.pkl'

# if os.path.exists(faces_path):
#     with open(faces_path, 'rb') as f:
#         existing_faces = pickle.load(f)

#     if existing_faces.shape[1] != FEATURE_SIZE:
#         print("\n" + "="*60)
#         print("[ERROR] Existing faces_data.pkl has incompatible shape!")
#         print(f"        Existing: {existing_faces.shape[1]} features")
#         print(f"        New data: {FEATURE_SIZE} features")
#         print("\n[FIX] Delete old files and retrain everyone:")
#         print("      del data\\names.pkl")
#         print("      del data\\faces_data.pkl")
#         print("      Then run add_faces.py for each person again.")
#         print("="*60)
#         exit()

#     # Compatible — append
#     combined_faces = np.append(existing_faces, faces_data, axis=0)

#     with open(names_path, 'rb') as f:
#         names = pickle.load(f)
#     names = names + [name] * len(faces_data)

#     with open(faces_path, 'wb') as f:
#         pickle.dump(combined_faces, f)
#     with open(names_path, 'wb') as f:
#         pickle.dump(names, f)

#     print(f"[INFO] Appended '{name}' to existing dataset.")
#     print(f"[INFO] All people in dataset: {set(names)}")
#     print(f"[INFO] Total samples: {combined_faces.shape[0]}")

# else:
#     # Fresh start
#     names = [name] * len(faces_data)
#     with open(faces_path, 'wb') as f:
#         pickle.dump(faces_data, f)
#     with open(names_path, 'wb') as f:
#         pickle.dump(names, f)
#     print(f"[INFO] Created new dataset with '{name}'")

# print(f"\n[DONE] '{name}' saved successfully!")











# import cv2
# import pickle
# import numpy as np
# import os

# video = cv2.VideoCapture(0)
# facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# SAMPLE_COUNT = 30

# # ================================================================
# # MUST MATCH test.py preprocess_face() exactly!
# # If you change one, change both.
# # ================================================================
# def preprocess_face(crop_img):
#     gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
#     equalized = cv2.equalizeHist(gray)
#     resized = cv2.resize(equalized, (50, 50))
#     return resized  # return 2D for storage, flatten later

# faces_data = []
# i = 0

# name = input("Enter Your Name: ")
# print(f"[INFO] Collecting {SAMPLE_COUNT} samples for '{name}'.")
# print("[INFO] Look at the camera from different angles and distances!")

# while True:
#     ret, frame = video.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = facedetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(60, 60))

#     for (x, y, w, h) in faces:
#         crop_img = frame[y:y+h, x:x+w, :]
#         processed = preprocess_face(crop_img)

#         if len(faces_data) < SAMPLE_COUNT and i % 5 == 0:
#             faces_data.append(processed)

#         i += 1

#         progress = len(faces_data)
#         cv2.putText(frame, f"Samples: {progress}/{SAMPLE_COUNT}", (30, 50),
#                     cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)

#         # Progress bar
#         bar_width = int((progress / SAMPLE_COUNT) * 580)
#         cv2.rectangle(frame, (30, 430), (610, 460), (50, 50, 50), -1)
#         cv2.rectangle(frame, (30, 430), (30 + bar_width, 460), (50, 200, 50), -1)

#         # Tip: nudge user to vary angle
#         tips = ["Look straight", "Tilt left", "Tilt right", "Move closer", "Move farther"]
#         tip = tips[(progress // 6) % len(tips)]
#         cv2.putText(frame, tip, (30, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 200), 2)

#     cv2.imshow("Collecting Faces - Press Q to quit", frame)
#     k = cv2.waitKey(1)

#     if k == ord('q') or len(faces_data) == SAMPLE_COUNT:
#         break

# video.release()
# cv2.destroyAllWindows()

# if len(faces_data) == 0:
#     print("[ERROR] No face samples collected. Exiting.")
#     exit()

# print(f"[INFO] Collected {len(faces_data)} samples for '{name}'")

# faces_data = np.array(faces_data).reshape(len(faces_data), -1)

# # ---- Save names ----
# if 'names.pkl' not in os.listdir('data/'):
#     names = [name] * len(faces_data)
#     with open('data/names.pkl', 'wb') as f:
#         pickle.dump(names, f)
#     print(f"[INFO] Created new names.pkl with '{name}'")
# else:
#     with open('data/names.pkl', 'rb') as f:
#         names = pickle.load(f)
#     names = names + [name] * len(faces_data)
#     with open('data/names.pkl', 'wb') as f:
#         pickle.dump(names, f)
#     print(f"[INFO] All people in dataset: {set(names)}")

# # ---- Save faces ----
# if 'faces_data.pkl' not in os.listdir('data/'):
#     with open('data/faces_data.pkl', 'wb') as f:
#         pickle.dump(faces_data, f)
#     print("[INFO] Created new faces_data.pkl")
# else:
#     with open('data/faces_data.pkl', 'rb') as f:
#         existing_faces = pickle.load(f)
#     combined = np.append(existing_faces, faces_data, axis=0)
#     with open('data/faces_data.pkl', 'wb') as f:
#         pickle.dump(combined, f)
#     print(f"[INFO] Total samples in dataset: {combined.shape[0]}")

# print(f"\n[DONE] '{name}' added successfully!")
# print("[IMPORTANT] Delete data/names.pkl and data/faces_data.pkl and retrain ALL people if accuracy is poor.")




# import cv2
# import pickle
# import numpy as np
# import os

# video = cv2.VideoCapture(0)

# # Primary detector — strict (frontal)
# facedetect_strict = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# # Relaxed detector — catches partial/angled faces
# facedetect_relaxed = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# # Optional: profile face detector for extreme side angles
# # Download from OpenCV data folder if available
# profile_path = 'data/haarcascade_profileface.xml'
# facedetect_profile = None
# if os.path.exists(profile_path):
#     facedetect_profile = cv2.CascadeClassifier(profile_path)
#     print("[INFO] Profile face detector loaded.")
# else:
#     print("[INFO] Profile detector not found — using relaxed frontal only.")

# FEATURE_SIZE = 2500  # grayscale 50x50

# def preprocess_face(crop_img):
#     """MUST match test.py exactly."""
#     gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
#     equalized = cv2.equalizeHist(gray)
#     resized = cv2.resize(equalized, (50, 50))
#     return resized  # 2D, flattened later

# # ================================================================
# # POSE STAGES — forces user to cover all angles
# # Each stage collects SAMPLES_PER_STAGE samples
# # ================================================================
# POSE_STAGES = [
#     {"label": "Look STRAIGHT at camera",     "color": (0, 200, 0)},
#     {"label": "Tilt HEAD LEFT slowly",        "color": (0, 180, 200)},
#     {"label": "Tilt HEAD RIGHT slowly",       "color": (200, 180, 0)},
#     {"label": "Look UP slightly",             "color": (200, 100, 0)},
#     {"label": "Look DOWN slightly",           "color": (100, 0, 200)},
#     {"label": "Turn FACE LEFT (side angle)",  "color": (0, 100, 255)},
#     {"label": "Turn FACE RIGHT (side angle)", "color": (255, 100, 0)},
#     {"label": "Move CLOSER to camera",        "color": (0, 200, 100)},
#     {"label": "Move FARTHER from camera",     "color": (200, 0, 100)},
#     {"label": "ANY pose (free variation)",    "color": (180, 180, 180)},
# ]
# SAMPLES_PER_STAGE = 5
# TOTAL_SAMPLES = len(POSE_STAGES) * SAMPLES_PER_STAGE  # 50

# def detect_faces_best(frame, gray):
#     """
#     Try strict detector first. If no faces found, fall back to relaxed
#     settings that work better for angled/partial faces.
#     Also tries flipped frame to catch the other profile direction.
#     """
#     # Strict detection
#     faces = facedetect_strict.detectMultiScale(
#         gray, scaleFactor=1.2, minNeighbors=6, minSize=(60, 60)
#     )
#     if len(faces) > 0:
#         return faces

#     # Relaxed detection — lower neighbors, smaller minSize
#     faces = facedetect_relaxed.detectMultiScale(
#         gray, scaleFactor=1.1, minNeighbors=3, minSize=(40, 40)
#     )
#     if len(faces) > 0:
#         return faces

#     # Profile detector (side faces)
#     if facedetect_profile is not None:
#         faces = facedetect_profile.detectMultiScale(
#             gray, scaleFactor=1.1, minNeighbors=3, minSize=(40, 40)
#         )
#         if len(faces) > 0:
#             return faces

#         # Flip frame to catch opposite side profile
#         gray_flip = cv2.flip(gray, 1)
#         frame_flip = cv2.flip(frame, 1)
#         faces_flip = facedetect_profile.detectMultiScale(
#             gray_flip, scaleFactor=1.1, minNeighbors=3, minSize=(40, 40)
#         )
#         if len(faces_flip) > 0:
#             # Un-flip coordinates back to original frame space
#             h_img, w_img = frame.shape[:2]
#             faces_unflipped = []
#             for (fx, fy, fw, fh) in faces_flip:
#                 orig_x = w_img - fx - fw
#                 faces_unflipped.append((orig_x, fy, fw, fh))
#             return np.array(faces_unflipped)

#     return []


# # ================================================================
# # MAIN COLLECTION LOOP
# # ================================================================
# faces_data = []
# stage_idx = 0
# stage_count = 0
# frame_counter = 0
# last_sample_frame = -10  # prevent collecting too fast

# name = input("Enter Your Name: ")
# print(f"\n[INFO] Collecting {TOTAL_SAMPLES} samples ({SAMPLES_PER_STAGE} per pose stage).")
# print("[INFO] Follow the on-screen instructions for each pose.\n")

# while True:
#     ret, frame = video.read()
#     if not ret:
#         print("[ERROR] Camera read failed.")
#         break

#     frame_counter += 1
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     faces = detect_faces_best(frame, gray)

#     current_stage = POSE_STAGES[stage_idx] if stage_idx < len(POSE_STAGES) else None
#     stage_color = current_stage["color"] if current_stage else (200, 200, 200)
#     stage_label = current_stage["label"] if current_stage else "Done!"

#     face_detected = False

#     for (x, y, w, h) in faces:
#         # Clamp to frame boundaries
#         x1, y1 = max(0, x), max(0, y)
#         x2, y2 = min(frame.shape[1], x + w), min(frame.shape[0], y + h)
#         crop_img = frame[y1:y2, x1:x2, :]

#         if crop_img.size == 0:
#             continue

#         face_detected = True

#         # Collect sample: every 3 frames and not too close to last sample
#         enough_gap = (frame_counter - last_sample_frame) >= 3
#         if stage_count < SAMPLES_PER_STAGE and enough_gap:
#             processed = preprocess_face(crop_img)
#             faces_data.append(processed)
#             stage_count += 1
#             last_sample_frame = frame_counter

#             # Advance stage when enough samples for this pose
#             if stage_count == SAMPLES_PER_STAGE:
#                 stage_idx += 1
#                 stage_count = 0
#                 if stage_idx < len(POSE_STAGES):
#                     print(f"[STAGE {stage_idx}] Next: {POSE_STAGES[stage_idx]['label']}")

#         cv2.rectangle(frame, (x1, y1), (x2, y2), stage_color, 2)

#     total_collected = len(faces_data)

#     # ---- Overlay UI ----
#     # Dark banner top
#     cv2.rectangle(frame, (0, 0), (frame.shape[1], 60), (30, 30, 30), -1)

#     # Pose instruction
#     status_text = stage_label if face_detected else "NO FACE — adjust position"
#     text_color = stage_color if face_detected else (0, 50, 255)
#     cv2.putText(frame, status_text, (10, 42),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 2)

#     # Sample counter top-right
#     counter_str = f"{total_collected}/{TOTAL_SAMPLES}"
#     cv2.putText(frame, counter_str, (frame.shape[1] - 160, 42),
#                 cv2.FONT_HERSHEY_COMPLEX, 0.9, (50, 255, 100), 2)

#     # Stage progress dots
#     dot_x = 10
#     for si in range(len(POSE_STAGES)):
#         dot_color = (0, 200, 0) if si < stage_idx else ((100, 200, 255) if si == stage_idx else (80, 80, 80))
#         cv2.circle(frame, (dot_x + si * 22, frame.shape[0] - 20), 8, dot_color, -1)

#     # Overall progress bar
#     bar_fill = int((total_collected / TOTAL_SAMPLES) * (frame.shape[1] - 20))
#     cv2.rectangle(frame, (10, frame.shape[0] - 40), (frame.shape[1] - 10, frame.shape[0] - 10), (50, 50, 50), -1)
#     cv2.rectangle(frame, (10, frame.shape[0] - 40), (10 + bar_fill, frame.shape[0] - 10), (50, 200, 50), -1)

#     # Stage sub-progress bar (lighter color)
#     sub_fill = int((stage_count / SAMPLES_PER_STAGE) * (frame.shape[1] - 20))
#     cv2.rectangle(frame, (10, frame.shape[0] - 48), (10 + sub_fill, frame.shape[0] - 42), stage_color, -1)

#     cv2.imshow("Collecting Faces - Press Q to quit", frame)
#     k = cv2.waitKey(1)

#     if k == ord('q'):
#         print("[INFO] Quit early.")
#         break
#     if total_collected >= TOTAL_SAMPLES:
#         print(f"[INFO] All {TOTAL_SAMPLES} samples collected!")
#         break

# video.release()
# cv2.destroyAllWindows()

# # ================================================================
# # Save data
# # ================================================================
# if len(faces_data) == 0:
#     print("[ERROR] No face samples collected. Exiting.")
#     exit()

# print(f"[INFO] Collected {len(faces_data)} samples for '{name}'")

# faces_data = np.array(faces_data).reshape(len(faces_data), -1)
# print(f"[INFO] Data shape: {faces_data.shape}")

# names_path = 'data/names.pkl'
# faces_path = 'data/faces_data.pkl'

# if os.path.exists(faces_path):
#     with open(faces_path, 'rb') as f:
#         existing_faces = pickle.load(f)

#     if existing_faces.shape[1] != FEATURE_SIZE:
#         print("\n" + "="*60)
#         print("[ERROR] Existing faces_data.pkl has incompatible shape!")
#         print(f"        Existing: {existing_faces.shape[1]} features")
#         print(f"        New data : {FEATURE_SIZE} features")
#         print("\n[FIX] Delete old files and retrain everyone:")
#         print("      del data\\names.pkl")
#         print("      del data\\faces_data.pkl")
#         print("="*60)
#         exit()

#     combined_faces = np.append(existing_faces, faces_data, axis=0)

#     with open(names_path, 'rb') as f:
#         names = pickle.load(f)
#     names = names + [name] * len(faces_data)

#     with open(faces_path, 'wb') as f:
#         pickle.dump(combined_faces, f)
#     with open(names_path, 'wb') as f:
#         pickle.dump(names, f)

#     print(f"[INFO] Appended '{name}' to existing dataset.")
#     print(f"[INFO] All people: {set(names)}")
#     print(f"[INFO] Total samples: {combined_faces.shape[0]}")

# else:
#     names = [name] * len(faces_data)
#     with open(faces_path, 'wb') as f:
#         pickle.dump(faces_data, f)
#     with open(names_path, 'wb') as f:
#         pickle.dump(names, f)
#     print(f"[INFO] Created new dataset with '{name}'")

# print(f"\n[DONE] '{name}' saved successfully!")
# print(f"[TIP]  Delete data/*.pkl and re-run this script if recognition is poor.")









# import cv2
# import pickle
# import numpy as np
# import os

# video = cv2.VideoCapture(0)
# video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# # ================================================================
# # LOAD DNN FACE DETECTOR (same as server.py)
# # ================================================================
# DNN_PROTO  = 'data/deploy.prototxt'
# DNN_MODEL  = 'data/res10_300x300_ssd_iter_140000.caffemodel'
# USE_DNN    = os.path.exists(DNN_PROTO) and os.path.exists(DNN_MODEL)

# if USE_DNN:
#     net = cv2.dnn.readNetFromCaffe(DNN_PROTO, DNN_MODEL)
#     print("[INFO] DNN face detector loaded")
# else:
#     haar = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
#     print("[WARN] DNN not found — falling back to Haar Cascade")

# DNN_CONFIDENCE = 0.55
# FEATURE_SIZE   = 2500   # 50x50

# # ================================================================
# # POSE STAGES
# # ================================================================
# SAMPLES_PER_STAGE = 6
# POSE_STAGES = [
#     {"label": "Look STRAIGHT at camera",      "color": (0, 220, 0)},
#     {"label": "Tilt HEAD LEFT slowly",         "color": (0, 180, 200)},
#     {"label": "Tilt HEAD RIGHT slowly",        "color": (200, 180, 0)},
#     {"label": "Look UP slightly",              "color": (200, 100, 0)},
#     {"label": "Look DOWN slightly",            "color": (100, 0, 200)},
#     {"label": "Turn FACE LEFT (side angle)",   "color": (0, 100, 255)},
#     {"label": "Turn FACE RIGHT (side angle)",  "color": (255, 100, 0)},
#     {"label": "Move CLOSER to camera",         "color": (0, 200, 100)},
#     {"label": "Move FARTHER from camera",      "color": (200, 0, 100)},
#     {"label": "ANY pose — free variation",     "color": (180, 180, 180)},
# ]
# TOTAL_SAMPLES = len(POSE_STAGES) * SAMPLES_PER_STAGE  # 60 base


# # ================================================================
# # PREPROCESSING — must exactly match server.py
# # ================================================================
# def preprocess_face(crop_img):
#     gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
#     equalized = cv2.equalizeHist(gray)
#     resized = cv2.resize(equalized, (50, 50))
#     normalized = resized.astype(np.float32) / 255.0
#     return normalized  # 2D float, flattened during save


# # ================================================================
# # DATA AUGMENTATION
# # Generates 7 variants per captured sample (~420 total from 60)
# # ================================================================
# def augment_face(face_2d):
#     variants = [face_2d]

#     # Horizontal flip — simulates opposite head turn
#     variants.append(cv2.flip(face_2d, 1))

#     # Brightness shifts — simulates lighting changes
#     variants.append(np.clip(face_2d + 0.10, 0, 1))
#     variants.append(np.clip(face_2d - 0.10, 0, 1))

#     # Small rotations — simulates head tilt
#     h, w = face_2d.shape
#     center = (w // 2, h // 2)
#     for angle in [-10, 10]:
#         M = cv2.getRotationMatrix2D(center, angle, 1.0)
#         rotated = cv2.warpAffine(face_2d, M, (w, h))
#         variants.append(rotated)

#     # Slight zoom in
#     scale = 0.85
#     cx, cy = w // 2, h // 2
#     cw, ch = int(w * scale), int(h * scale)
#     x1 = max(cx - cw // 2, 0)
#     y1 = max(cy - ch // 2, 0)
#     x2 = min(cx + cw // 2, w)
#     y2 = min(cy + ch // 2, h)
#     zoomed = cv2.resize(face_2d[y1:y2, x1:x2], (w, h))
#     variants.append(zoomed)

#     return variants  # 7 variants


# # ================================================================
# # DETECTION — DNN or Haar fallback (same logic as server.py)
# # ================================================================
# def detect_faces(frame):
#     if USE_DNN:
#         h, w = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(
#             cv2.resize(frame, (300, 300)), 1.0,
#             (300, 300), (104.0, 177.0, 123.0)
#         )
#         net.setInput(blob)
#         dets = net.forward()

#         faces = []
#         for i in range(dets.shape[2]):
#             conf = dets[0, 0, i, 2]
#             if conf < DNN_CONFIDENCE:
#                 continue
#             box = dets[0, 0, i, 3:7] * np.array([w, h, w, h])
#             x1, y1, x2, y2 = box.astype(int)
#             x1, y1 = max(0, x1), max(0, y1)
#             x2, y2 = min(w, x2), min(h, y2)
#             if (x2 - x1) < 40 or (y2 - y1) < 40:
#                 continue
#             faces.append((x1, y1, x2, y2))
#         return faces

#     else:
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         gray_eq = cv2.equalizeHist(gray)
#         configs = [(1.1, 6, (80, 80)), (1.1, 4, (60, 60)), (1.05, 3, (50, 50))]
#         for scale, neighbors, minsize in configs:
#             fs = haar.detectMultiScale(gray_eq, scale, neighbors, minSize=minsize)
#             if len(fs) > 0:
#                 return [(x, y, x + w, y + h) for (x, y, w, h) in fs]
#         return []


# # ================================================================
# # MAIN COLLECTION LOOP
# # ================================================================
# name = input("Enter Your Name: ")
# print(f"\n[INFO] Collecting {TOTAL_SAMPLES} samples across {len(POSE_STAGES)} poses.")
# print(f"[INFO] Each sample augmented to 7x → ~{TOTAL_SAMPLES * 7} effective training samples.\n")

# faces_data = []
# stage_idx   = 0
# stage_count = 0
# frame_counter = 0
# last_sample_frame = -10

# while True:
#     ret, frame = video.read()
#     if not ret:
#         print("[ERROR] Camera read failed.")
#         break

#     frame_counter += 1
#     faces = detect_faces(frame)

#     current_stage = POSE_STAGES[stage_idx] if stage_idx < len(POSE_STAGES) else None
#     stage_color   = current_stage["color"] if current_stage else (200, 200, 200)
#     stage_label   = current_stage["label"] if current_stage else "All done!"

#     face_detected = False

#     for (x1, y1, x2, y2) in faces:
#         crop_img = frame[y1:y2, x1:x2]
#         if crop_img.size == 0:
#             continue

#         face_detected = True
#         enough_gap = (frame_counter - last_sample_frame) >= 4

#         if stage_idx < len(POSE_STAGES) and stage_count < SAMPLES_PER_STAGE and enough_gap:
#             processed = preprocess_face(crop_img)
#             faces_data.append(processed)
#             stage_count += 1
#             last_sample_frame = frame_counter

#             if stage_count == SAMPLES_PER_STAGE:
#                 stage_idx += 1
#                 stage_count = 0
#                 if stage_idx < len(POSE_STAGES):
#                     print(f"[STAGE {stage_idx + 1}/{len(POSE_STAGES)}] → {POSE_STAGES[stage_idx]['label']}")

#         cv2.rectangle(frame, (x1, y1), (x2, y2), stage_color, 2)

#     total_collected = len(faces_data)

#     # ---- UI overlay ----
#     cv2.rectangle(frame, (0, 0), (frame.shape[1], 62), (25, 25, 25), -1)

#     status_text = stage_label if face_detected else "NO FACE DETECTED — adjust position"
#     text_color  = stage_color if face_detected else (0, 60, 255)
#     cv2.putText(frame, status_text, (10, 44),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.72, text_color, 2)

#     counter_str = f"{total_collected}/{TOTAL_SAMPLES}"
#     cv2.putText(frame, counter_str, (frame.shape[1] - 170, 44),
#                 cv2.FONT_HERSHEY_COMPLEX, 0.95, (60, 255, 120), 2)

#     # Stage progress dots
#     for si in range(len(POSE_STAGES)):
#         if si < stage_idx:
#             dot_color = (0, 200, 0)
#         elif si == stage_idx:
#             dot_color = (100, 200, 255)
#         else:
#             dot_color = (70, 70, 70)
#         cv2.circle(frame, (10 + si * 22, frame.shape[0] - 18), 7, dot_color, -1)

#     # Overall progress bar
#     bar_fill = int((total_collected / TOTAL_SAMPLES) * (frame.shape[1] - 20))
#     cv2.rectangle(frame, (10, frame.shape[0] - 42), (frame.shape[1] - 10, frame.shape[0] - 10), (50, 50, 50), -1)
#     cv2.rectangle(frame, (10, frame.shape[0] - 42), (10 + bar_fill, frame.shape[0] - 10), (50, 200, 50), -1)

#     # Stage sub-progress bar
#     sub_fill = int((stage_count / SAMPLES_PER_STAGE) * (frame.shape[1] - 20))
#     cv2.rectangle(frame, (10, frame.shape[0] - 50), (10 + sub_fill, frame.shape[0] - 44), stage_color, -1)

#     detector_tag = "DNN" if USE_DNN else "HAAR"
#     cv2.putText(frame, detector_tag, (frame.shape[1] - 70, frame.shape[0] - 55),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 0), 1)

#     cv2.imshow("Collecting Faces — Press Q to quit", frame)
#     k = cv2.waitKey(1)

#     if k == ord('q'):
#         print("[INFO] Quit early.")
#         break
#     if total_collected >= TOTAL_SAMPLES:
#         print(f"\n[INFO] All {TOTAL_SAMPLES} base samples collected!")
#         break

# video.release()
# cv2.destroyAllWindows()

# if len(faces_data) == 0:
#     print("[ERROR] No face samples collected. Exiting.")
#     exit()

# # ================================================================
# # AUGMENTATION
# # ================================================================
# print(f"[INFO] Augmenting {len(faces_data)} samples...")
# augmented = []
# for face in faces_data:
#     augmented.extend(augment_face(face))

# augmented = np.array(augmented).reshape(len(augmented), -1)
# print(f"[INFO] Final dataset shape after augmentation: {augmented.shape}")

# names_path = 'data/names.pkl'
# faces_path = 'data/faces_data.pkl'

# if os.path.exists(faces_path):
#     with open(faces_path, 'rb') as f:
#         existing_faces = pickle.load(f)

#     if existing_faces.shape[1] != FEATURE_SIZE:
#         print("\n" + "="*60)
#         print("[ERROR] Existing faces_data.pkl has incompatible shape!")
#         print(f"        Existing: {existing_faces.shape[1]} features | New: {FEATURE_SIZE}")
#         print("[FIX]   Delete data/names.pkl and data/faces_data.pkl, then re-run for all people.")
#         print("="*60)
#         exit()

#     combined_faces = np.append(existing_faces, augmented, axis=0)
#     with open(names_path, 'rb') as f:
#         existing_names = pickle.load(f)
#     combined_names = existing_names + [name] * len(augmented)

#     with open(faces_path, 'wb') as f:
#         pickle.dump(combined_faces, f)
#     with open(names_path, 'wb') as f:
#         pickle.dump(combined_names, f)

#     print(f"[INFO] Appended '{name}' — all people: {set(combined_names)}")
#     print(f"[INFO] Total samples: {combined_faces.shape[0]}")

# else:
#     combined_names = [name] * len(augmented)
#     with open(faces_path, 'wb') as f:
#         pickle.dump(augmented, f)
#     with open(names_path, 'wb') as f:
#         pickle.dump(combined_names, f)
#     print(f"[INFO] Created new dataset with '{name}' — {len(augmented)} samples")

# print(f"\n[DONE] '{name}' saved successfully!")
# print("[TIP]  Delete data/*.pkl and re-run for all people if accuracy is poor.")















import cv2
import pickle
import numpy as np
import os

from face_utils import (
    load_detectors, detect_faces, preprocess_face,
    augment_face, FEATURE_SIZE
)

# ================================================================
# CAMERA
# ================================================================
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

net, haar, USE_DNN = load_detectors()

# ================================================================
# POSE STAGES
# More stages at extreme angles = better side-angle recognition
# ================================================================
SAMPLES_PER_STAGE = 6
POSE_STAGES = [
    {"label": "Look STRAIGHT at camera",       "color": (0, 220, 0)},
    {"label": "Tilt HEAD LEFT slowly",          "color": (0, 180, 200)},
    {"label": "Tilt HEAD RIGHT slowly",         "color": (200, 180, 0)},
    {"label": "Look UP slightly",               "color": (200, 100, 0)},
    {"label": "Look DOWN slightly",             "color": (100, 0, 200)},
    {"label": "Turn FACE LEFT — 45°",           "color": (0, 100, 255)},
    {"label": "Turn FACE LEFT — 60° (extreme)", "color": (0, 60, 255)},
    {"label": "Turn FACE RIGHT — 45°",          "color": (255, 100, 0)},
    {"label": "Turn FACE RIGHT — 60° (extreme)","color": (255, 60, 0)},
    {"label": "Move CLOSER to camera",          "color": (0, 200, 100)},
    {"label": "Move FARTHER from camera",       "color": (200, 0, 100)},
    {"label": "ANY pose — free variation",      "color": (180, 180, 180)},
]
TOTAL_SAMPLES = len(POSE_STAGES) * SAMPLES_PER_STAGE  # 72 base → ~504 after augmentation

# ================================================================
# COLLECTION LOOP
# ================================================================
name = input("Enter Your Name: ")
print(f"\n[INFO] Collecting {TOTAL_SAMPLES} samples across {len(POSE_STAGES)} poses.")
print(f"[INFO] Each sample augmented 7× → ~{TOTAL_SAMPLES * 7} effective training samples.")
print(f"[INFO] Detector: {'DNN (two-pass)' if USE_DNN else 'Haar'}\n")

faces_data        = []
stage_idx         = 0
stage_count       = 0
frame_counter     = 0
last_sample_frame = -10

while True:
    ret, frame = video.read()
    if not ret:
        print("[ERROR] Camera read failed.")
        break

    frame_counter += 1

    # Use same detection as server/test — TWO-PASS DNN
    faces = detect_faces(frame, net, haar, USE_DNN)

    current_stage = POSE_STAGES[stage_idx] if stage_idx < len(POSE_STAGES) else None
    stage_color   = current_stage["color"] if current_stage else (200, 200, 200)
    stage_label   = current_stage["label"] if current_stage else "All done!"
    face_detected = False

    for (x1, y1, w, h, det_conf) in faces:
        x2, y2   = x1 + w, y1 + h
        crop_img = frame[y1:y2, x1:x2]
        if crop_img.size == 0:
            continue

        face_detected = True
        enough_gap    = (frame_counter - last_sample_frame) >= 4

        if stage_idx < len(POSE_STAGES) and stage_count < SAMPLES_PER_STAGE and enough_gap:
            processed = preprocess_face(crop_img)   # returns 2D float
            faces_data.append(processed)
            stage_count += 1
            last_sample_frame = frame_counter

            if stage_count == SAMPLES_PER_STAGE:
                stage_idx  += 1
                stage_count = 0
                if stage_idx < len(POSE_STAGES):
                    print(f"  [STAGE {stage_idx + 1}/{len(POSE_STAGES)}] → {POSE_STAGES[stage_idx]['label']}")

        cv2.rectangle(frame, (x1, y1), (x2, y2), stage_color, 2)
        # Show detection confidence so you know if relaxed pass fired
        cv2.putText(frame, f"{det_conf:.2f}", (x1, y2 + 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 255, 255), 1)

    total_collected = len(faces_data)

    # ---- UI overlay ----
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 62), (25, 25, 25), -1)

    status_text = stage_label if face_detected else "NO FACE — adjust position or move closer"
    text_color  = stage_color if face_detected else (0, 60, 255)
    cv2.putText(frame, status_text, (10, 44),
                cv2.FONT_HERSHEY_SIMPLEX, 0.70, text_color, 2)

    cv2.putText(frame, f"{total_collected}/{TOTAL_SAMPLES}",
                (frame.shape[1] - 170, 44),
                cv2.FONT_HERSHEY_COMPLEX, 0.95, (60, 255, 120), 2)

    # Stage progress dots
    for si in range(len(POSE_STAGES)):
        dot_color = (0,200,0) if si < stage_idx else ((100,200,255) if si == stage_idx else (70,70,70))
        cv2.circle(frame, (10 + si * 20, frame.shape[0] - 18), 6, dot_color, -1)

    # Overall progress bar
    bar_fill = int((total_collected / TOTAL_SAMPLES) * (frame.shape[1] - 20))
    cv2.rectangle(frame, (10, frame.shape[0]-42), (frame.shape[1]-10, frame.shape[0]-10), (50,50,50), -1)
    cv2.rectangle(frame, (10, frame.shape[0]-42), (10+bar_fill, frame.shape[0]-10), (50,200,50), -1)

    # Stage sub-bar
    sub_fill = int((stage_count / SAMPLES_PER_STAGE) * (frame.shape[1] - 20))
    cv2.rectangle(frame, (10, frame.shape[0]-50), (10+sub_fill, frame.shape[0]-44), stage_color, -1)

    cv2.putText(frame, f"{'DNN' if USE_DNN else 'HAAR'}",
                (frame.shape[1]-70, frame.shape[0]-55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,0), 1)

    cv2.imshow("Collecting Faces — Press Q to quit", frame)
    k = cv2.waitKey(1)

    if k == ord('q'):
        print("[INFO] Quit early.")
        break
    if total_collected >= TOTAL_SAMPLES:
        print(f"\n[INFO] All {TOTAL_SAMPLES} samples collected!")
        break

video.release()
cv2.destroyAllWindows()

if len(faces_data) == 0:
    print("[ERROR] No face samples collected. Exiting.")
    exit()

# ================================================================
# AUGMENTATION
# ================================================================
print(f"\n[INFO] Augmenting {len(faces_data)} base samples...")
augmented = []
for face in faces_data:
    augmented.extend(augment_face(face))

augmented = np.array(augmented).reshape(len(augmented), -1)
print(f"[INFO] Final dataset: {augmented.shape}  ({augmented.shape[0]} samples × {augmented.shape[1]} features)")

names_path = 'data/names.pkl'
faces_path = 'data/faces_data.pkl'

if os.path.exists(faces_path):
    with open(faces_path, 'rb') as f:
        existing_faces = pickle.load(f)

    if existing_faces.shape[1] != FEATURE_SIZE:
        print(f"\n[ERROR] Shape mismatch! Existing={existing_faces.shape[1]}, New={FEATURE_SIZE}")
        print("[FIX]   Delete data/names.pkl and data/faces_data.pkl, re-run for ALL people.")
        exit()

    combined_faces = np.append(existing_faces, augmented, axis=0)
    with open(names_path, 'rb') as f:
        existing_names = pickle.load(f)
    combined_names = existing_names + [name] * len(augmented)

    with open(faces_path, 'wb') as f: pickle.dump(combined_faces, f)
    with open(names_path, 'wb') as f: pickle.dump(combined_names, f)

    print(f"[INFO] Appended '{name}' — dataset: {combined_faces.shape[0]} total samples")
    print(f"[INFO] People in dataset: {set(combined_names)}")
else:
    combined_names = [name] * len(augmented)
    with open(faces_path, 'wb') as f: pickle.dump(augmented, f)
    with open(names_path, 'wb') as f: pickle.dump(combined_names, f)
    print(f"[INFO] New dataset: '{name}' — {len(augmented)} samples")

print(f"\n[DONE] '{name}' saved!")
print("[NOTE] Delete data/*.pkl and re-run for all people if recognition is poor.")