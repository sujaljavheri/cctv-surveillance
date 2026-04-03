"""
Run this script ONCE to download the DNN face detector model files.
Usage:  python download_models.py
"""
import urllib.request
import os
import sys

os.makedirs('data', exist_ok=True)

FILES = {
    'data/deploy.prototxt': (
        'https://raw.githubusercontent.com/opencv/opencv/master/'
        'samples/dnn/face_detector/deploy.prototxt'
    ),
    'data/res10_300x300_ssd_iter_140000.caffemodel': (
        'https://github.com/opencv/opencv_3rdparty/raw/'
        'dnn_samples_face_detector_20170830/'
        'res10_300x300_ssd_iter_140000.caffemodel'
    ),
}

# Minimum expected sizes in bytes
MIN_SIZES = {
    'data/deploy.prototxt': 1_000,          # ~3 KB
    'data/res10_300x300_ssd_iter_140000.caffemodel': 10_000_000,  # ~10 MB
}

def download(path, url):
    print(f"\n[DOWN] {path}")
    print(f"       from: {url}")

    def progress(count, block_size, total_size):
        if total_size > 0:
            pct = min(count * block_size * 100 // total_size, 100)
            bar = '#' * (pct // 5) + '-' * (20 - pct // 5)
            sys.stdout.write(f"\r       [{bar}] {pct}%")
            sys.stdout.flush()

    urllib.request.urlretrieve(url, path, reporthook=progress)
    print()

for path, url in FILES.items():
    if os.path.exists(path):
        size = os.path.getsize(path)
        if size >= MIN_SIZES[path]:
            print(f"[SKIP] {path} already exists and looks valid ({size:,} bytes)")
            continue
        else:
            print(f"[WARN] {path} exists but is too small ({size:,} bytes) — re-downloading")

    try:
        download(path, url)
        size = os.path.getsize(path)
        print(f"[OK]   {path} — {size:,} bytes")
        if size < MIN_SIZES[path]:
            print(f"[WARN] File seems too small! Expected >= {MIN_SIZES[path]:,} bytes.")
            print(f"       The download may have been truncated. Try again or download manually.")
    except Exception as e:
        print(f"[ERR]  Failed to download {path}: {e}")
        print(f"       Please download manually from:\n       {url}")

# Verify both files load correctly with OpenCV
print("\n[TEST] Verifying model files load correctly with OpenCV...")
try:
    import cv2
    net = cv2.dnn.readNetFromCaffe(
        'data/deploy.prototxt',
        'data/res10_300x300_ssd_iter_140000.caffemodel'
    )
    import numpy as np
    dummy = np.zeros((300, 300, 3), dtype=np.uint8)
    blob = cv2.dnn.blobFromImage(dummy, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    out = net.forward()
    print(f"[OK]   Model loaded and ran a test forward pass successfully!")
    print(f"       Output shape: {out.shape}")
    print("\n✅ All good — you can now run server.py")
except Exception as e:
    print(f"[ERR]  Model verification failed: {e}")
    print("       The .caffemodel file may still be corrupted.")
    print("       Try deleting data/res10_300x300_ssd_iter_140000.caffemodel and re-running.")
