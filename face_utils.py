# """
# face_utils.py — shared detection & preprocessing used by
#                 add_faces.py, test.py, and server.py

# Import:
#     from face_utils import load_detectors, detect_faces, preprocess_face
# """

# import cv2
# import numpy as np
# import os

# # ================================================================
# # CONSTANTS — change here, applies everywhere
# # ================================================================
# DNN_PROTO         = 'data/deploy.prototxt'
# DNN_MODEL         = 'data/res10_300x300_ssd_iter_140000.caffemodel'

# DNN_CONF_STRICT   = 0.80   # pass 1 — frontal, high precision
# DNN_CONF_RELAXED  = 0.42   # pass 2 — side angles, lower threshold
#                             # only used when strict finds nothing
# MIN_BOX_AREA      = 2000   # px² — ignore tiny detections
# FACE_SIZE         = 50     # training image size (50×50)
# FEATURE_SIZE      = FACE_SIZE * FACE_SIZE  # 2500


# # ================================================================
# # LOAD DETECTORS
# # Returns (net, haar, use_dnn)
# # Call once at startup and pass net/haar to detect_faces()
# # ================================================================
# def load_detectors():
#     haar = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
#     if haar.empty():
#         raise RuntimeError("[FATAL] haarcascade_frontalface_default.xml not found in data/")

#     use_dnn = False
#     net     = None

#     if os.path.exists(DNN_PROTO) and os.path.exists(DNN_MODEL):
#         if os.path.getsize(DNN_MODEL) > 5_000_000:
#             try:
#                 loaded = cv2.dnn.readNetFromCaffe(DNN_PROTO, DNN_MODEL)
#                 # Validate with a dummy forward pass
#                 dummy = np.zeros((300, 300, 3), dtype=np.uint8)
#                 blob  = cv2.dnn.blobFromImage(dummy, 1.0, (300, 300), (104.0, 177.0, 123.0))
#                 loaded.setInput(blob)
#                 loaded.forward()
#                 net     = loaded
#                 use_dnn = True
#                 print("[INFO] DNN detector loaded and verified OK")
#             except Exception as e:
#                 print(f"[WARN] DNN failed: {e} — using Haar only")
#         else:
#             print("[WARN] Caffemodel too small (corrupted) — re-run download_models.py")
#     else:
#         print("[WARN] DNN files not found — using Haar only")

#     tag = "DNN" if use_dnn else "Haar"
#     print(f"[INFO] Active detector: {tag}")
#     return net, haar, use_dnn


# # ================================================================
# # DETECT FACES
# # Returns list of (x1, y1, w, h, confidence)
# #
# # Two-pass DNN strategy:
# #   Pass 1 — strict confidence (frontal, no false positives)
# #   Pass 2 — relaxed confidence (side angles) with shape filter
# #             only runs when pass 1 finds nothing
# # ================================================================
# def detect_faces(frame, net, haar, use_dnn):
#     if use_dnn and net is not None:
#         try:
#             result = _detect_dnn(frame, net)
#             if result:
#                 return result
#         except Exception as e:
#             print(f"[WARN] DNN frame error: {e}")
#     return _detect_haar(frame, haar)


# def _detect_dnn(frame, net):
#     h, w = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(
#         cv2.resize(frame, (300, 300)), 1.0,
#         (300, 300), (104.0, 177.0, 123.0)
#     )
#     net.setInput(blob)
#     raw = net.forward()

#     def _parse(threshold):
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
#             if bw * bh < MIN_BOX_AREA:
#                 continue
#             aspect = bw / max(bh, 1)
#             if aspect < 0.25 or aspect > 3.5:   # face-like aspect ratio
#                 continue
#             boxes.append((x1, y1, bw, bh, float(conf)))
#         return boxes

#     # Pass 1 — strict
#     strict = _parse(DNN_CONF_STRICT)
#     if strict:
#         return strict

#     # Pass 2 — relaxed (catches side angles)
#     return _parse(DNN_CONF_RELAXED)


# def _detect_haar(frame, haar):
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


# # ================================================================
# # PREPROCESS — used for both training (add_faces) and inference
# # CRITICAL: all three scripts must use this exact function
# # ================================================================
# def preprocess_face(crop):
#     gray       = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
#     equalized  = cv2.equalizeHist(gray)
#     resized    = cv2.resize(equalized, (FACE_SIZE, FACE_SIZE))
#     normalized = resized.astype(np.float32) / 255.0
#     return normalized   # returns 2D (FACE_SIZE×FACE_SIZE) — caller flattens if needed


# # ================================================================
# # AUGMENTATION — for add_faces.py
# # Returns 7 variants of a 2D normalized face array
# # ================================================================
# def augment_face(face_2d):
#     h, w  = face_2d.shape
#     center = (w // 2, h // 2)
#     variants = [face_2d]

#     # Horizontal flip
#     variants.append(cv2.flip(face_2d, 1))

#     # Brightness shifts
#     variants.append(np.clip(face_2d + 0.10, 0, 1).astype(np.float32))
#     variants.append(np.clip(face_2d - 0.10, 0, 1).astype(np.float32))

#     # Small rotations
#     for angle in [-12, 12]:
#         M = cv2.getRotationMatrix2D(center, angle, 1.0)
#         rotated = cv2.warpAffine(face_2d, M, (w, h))
#         variants.append(rotated)

#     # Zoom in
#     scale = 0.85
#     cw, ch = int(w * scale), int(h * scale)
#     x1 = max(center[0] - cw // 2, 0)
#     y1 = max(center[1] - ch // 2, 0)
#     x2 = min(center[0] + cw // 2, w)
#     y2 = min(center[1] + ch // 2, h)
#     zoomed = cv2.resize(face_2d[y1:y2, x1:x2], (w, h))
#     variants.append(zoomed)

#     return variants  # 7 total










"""
face_utils.py — shared detection, preprocessing, and KNN config
                used by add_faces.py, test.py, and server.py
"""

import cv2
import numpy as np
import os

# ================================================================
# CONSTANTS
# ================================================================
DNN_PROTO        = 'data/deploy.prototxt'
DNN_MODEL        = 'data/res10_300x300_ssd_iter_140000.caffemodel'

DNN_CONF_STRICT  = 0.80   # pass 1 — frontal, high precision
DNN_CONF_RELAXED = 0.42   # pass 2 — side angles (only when strict finds nothing)
MIN_BOX_AREA     = 2000   # px² minimum face box size
FACE_SIZE        = 50     # 50×50 px training images
FEATURE_SIZE     = FACE_SIZE * FACE_SIZE  # 2500

# ================================================================
# KNN CONFIG — centralised so all scripts use the same settings
#
# METRIC: 'euclidean' works well for normalized pixel features
# WEIGHTS: 'distance' — closer neighbors vote more strongly
# N_NEIGHBORS: computed dynamically per-script based on dataset size
#              formula: min(15, max(7, num_people * 4), len(labels))
#              More neighbors = smoother, less noisy predictions
# ================================================================
KNN_METRIC  = 'euclidean'
KNN_WEIGHTS = 'distance'

def get_n_neighbors(labels):
    """
    Dynamically compute best k for KNN given the dataset.
    More people or more samples = higher k for stability.
    """
    n_samples = len(labels)
    n_people  = len(set(labels))
    # At least 7, scale with people count, cap at 15 or total samples
    k = min(15, max(7, n_people * 4), n_samples)
    return k

# ================================================================
# LOAD DETECTORS
# ================================================================
def load_detectors():
    haar = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    if haar.empty():
        raise RuntimeError("[FATAL] haarcascade_frontalface_default.xml not found in data/")

    use_dnn = False
    net     = None

    if os.path.exists(DNN_PROTO) and os.path.exists(DNN_MODEL):
        if os.path.getsize(DNN_MODEL) > 5_000_000:
            try:
                loaded = cv2.dnn.readNetFromCaffe(DNN_PROTO, DNN_MODEL)
                dummy  = np.zeros((300, 300, 3), dtype=np.uint8)
                blob   = cv2.dnn.blobFromImage(dummy, 1.0, (300, 300), (104.0, 177.0, 123.0))
                loaded.setInput(blob)
                loaded.forward()
                net     = loaded
                use_dnn = True
                print("[INFO] DNN detector loaded and verified OK")
            except Exception as e:
                print(f"[WARN] DNN failed: {e} — using Haar only")
        else:
            print("[WARN] Caffemodel too small — re-run download_models.py")
    else:
        print("[WARN] DNN files not found — using Haar only")

    print(f"[INFO] Active detector: {'DNN (two-pass)' if use_dnn else 'Haar Cascade'}")
    return net, haar, use_dnn


# ================================================================
# DETECT FACES
# Returns list of (x1, y1, w, h, confidence)
# ================================================================
def detect_faces(frame, net, haar, use_dnn):
    if use_dnn and net is not None:
        try:
            result = _detect_dnn(frame, net)
            if result:
                return result
        except Exception as e:
            print(f"[WARN] DNN frame error: {e}")
    return _detect_haar(frame, haar)


def _detect_dnn(frame, net):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0)
    )
    net.setInput(blob)
    raw = net.forward()

    def _parse(threshold):
        boxes = []
        for i in range(raw.shape[2]):
            conf = raw[0, 0, i, 2]
            if conf < threshold:
                continue
            box = raw[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = box.astype(int)
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            bw, bh = x2 - x1, y2 - y1
            if bw * bh < MIN_BOX_AREA:
                continue
            aspect = bw / max(bh, 1)
            if aspect < 0.25 or aspect > 3.5:
                continue
            boxes.append((x1, y1, bw, bh, float(conf)))
        return boxes

    strict = _parse(DNN_CONF_STRICT)
    return strict if strict else _parse(DNN_CONF_RELAXED)


def _detect_haar(frame, haar):
    gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_e = cv2.equalizeHist(gray)
    for scale, neighbors, minsize in [
        (1.1, 6, (80, 80)),
        (1.1, 4, (60, 60)),
        (1.05, 3, (50, 50)),
    ]:
        faces = haar.detectMultiScale(
            gray_e, scaleFactor=scale,
            minNeighbors=neighbors, minSize=minsize,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces) > 0:
            return [(x, y, w, h, 0.9) for (x, y, w, h) in faces]
    return []


# ================================================================
# PREPROCESSING — identical in all scripts
# ================================================================
def preprocess_face(crop):
    gray       = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    equalized  = cv2.equalizeHist(gray)
    resized    = cv2.resize(equalized, (FACE_SIZE, FACE_SIZE))
    normalized = resized.astype(np.float32) / 255.0
    return normalized   # 2D — caller does .flatten().reshape(1,-1) for KNN


# ================================================================
# AUGMENTATION
# ================================================================
def augment_face(face_2d):
    h, w   = face_2d.shape
    center = (w // 2, h // 2)
    variants = [face_2d, cv2.flip(face_2d, 1)]

    # Brightness
    variants.append(np.clip(face_2d + 0.10, 0, 1).astype(np.float32))
    variants.append(np.clip(face_2d - 0.10, 0, 1).astype(np.float32))

    # Rotations
    for angle in [-12, 12]:
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        variants.append(cv2.warpAffine(face_2d, M, (w, h)))

    # Zoom
    scale = 0.85
    cw, ch = int(w*scale), int(h*scale)
    x1 = max(center[0]-cw//2, 0); y1 = max(center[1]-ch//2, 0)
    x2 = min(center[0]+cw//2, w); y2 = min(center[1]+ch//2, h)
    variants.append(cv2.resize(face_2d[y1:y2, x1:x2], (w, h)))

    return variants  # 7 total