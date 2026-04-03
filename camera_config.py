# """
# camera_config.py — Configure all 4 camera sources here
#                    Supports webcam, IP camera, RTSP, HTTP stream, video file

# HOW TO FIND YOUR CAMERA URL:
# ─────────────────────────────
# IP Camera (most CCTV brands):
#     Hikvision : rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101
#     Dahua     : rtsp://admin:password@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
#     Generic   : rtsp://username:password@ip_address:554/stream1

# Mobile as IP Camera (free apps):
#     DroidCam  : http://192.168.1.x:4747/video   (install DroidCam on Android)
#     IP Webcam : http://192.168.1.x:8080/video   (install IP Webcam on Android)
#     EpocCam   : works on iPhone

# YouTube Live / Twitch (streamlink required):
#     pip install streamlink
#     Then use source type "streamlink"

# Local webcam:
#     Use integer index: 0 = default, 1 = second webcam

# Video file (for demo):
#     Use file path: "videos/demo.mp4"
# """

# # ================================================================
# # CAMERA SOURCES
# # Edit this dict to configure your cameras
# #
# # source types:
# #   "webcam"     — local USB webcam (source = index number)
# #   "rtsp"       — IP camera RTSP stream
# #   "http"       — HTTP MJPEG stream (IP Webcam app etc.)
# #   "video"      — local video file (for demo)
# #   "screen"     — screen capture region (x, y, w, h)
# #   "disabled"   — slot unused, shows "No Signal"
# # ================================================================

# CAMERAS = {
#     0: {
#         "name":   "Camera 1 — Main Entrance",
#         "type":   "webcam",
#         "source": 0,            # webcam index
#     },
#     1: {
#         "name":   "Camera 2 — Parking Area",
#         "type":   "rtmp",
#         "source": "rtmp://localhost/live/stream1",
#         # To use IP camera, change to:
#         # "type":   "rtsp",
#         # "source": "rtsp://admin:password@192.168.1.64:554/stream1",
#         #
#         # To use phone as camera (IP Webcam app):
#         # "type":   "http",
#         # "source": "http://192.168.1.5:8080/video",
#     },
#     2: {
#         "name":   "Camera 3 — Side Gate",
#         "type":   "disabled",
#         "source": None,
#         # Demo video example:
#         # "type":   "video",
#         # "source": "videos/demo.mp4",
#     },
#     3: {
#         "name":   "Camera 4 — Back Exit",
#         "type":   "disabled",
#         "source": None,
#     },
# }

# # ================================================================
# # STREAM SETTINGS
# # ================================================================
# STREAM_WIDTH  = 640
# STREAM_HEIGHT = 480
# STREAM_FPS    = 30

# # Reconnect attempts if stream drops (IP cameras can disconnect)
# RECONNECT_ATTEMPTS = 5
# RECONNECT_DELAY    = 3   # seconds between attempts
















"""
camera_config.py — Configure all 4 camera sources here

Source types:
    webcam   — local USB webcam        source = 0, 1, 2...
    rtmp     — OBS / local RTMP stream source = "rtmp://localhost/live/stream1"
    rtsp     — IP camera RTSP stream   source = "rtsp://user:pass@ip:554/stream"
    http     — IP Webcam Android app   source = "http://192.168.x.x:8080/video"
    video    — local video file        source = "videos/demo.mp4"
    disabled — slot unused
"""

CAMERAS = {
    0: {
        "name":   "Camera 1 — Main Entrance",
        "type":   "webcam",
        "source": 0,
    },
    1: {
        "name":   "Camera 2 — OBS Live Stream",
        "type":   "rtmp",                          # ← must be "rtmp" not "rtsp"
        "source": "rtmp://localhost/live/stream1",  # matches OBS stream key
    },
    2: {
        "name":   "Camera 3 — Side Gate",
        "type":   "disabled",
        "source": None,
        # IP camera example:
        # "type":   "rtsp",
        # "source": "rtsp://admin:password@192.168.1.64:554/stream1",
        #
        # Android phone camera (IP Webcam app):
        # "type":   "http",
        # "source": "http://192.168.1.5:8080/video",
    },
    3: {
        "name":   "Camera 4 — Back Exit",
        "type":   "disabled",
        "source": None,
        # Demo video:
        # "type":   "video",
        # "source": "videos/demo.mp4",
    },
}

STREAM_WIDTH       = 640
STREAM_HEIGHT      = 480
STREAM_FPS         = 30
RECONNECT_ATTEMPTS = 5
RECONNECT_DELAY    = 3