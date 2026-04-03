# """
# alerts.py — Voice alert + SMS to Indian mobile number
# Uses Fast2SMS — free, no number purchase needed

# Setup:
#     1. Login to fast2sms.com
#     2. Click Profile icon (top right) → Dev API
#     3. Copy the API key
#     4. Paste in FAST2SMS_API_KEY below
# """

# import threading
# import time
# import urllib.request
# import urllib.parse
# import json
# from datetime import datetime

# # ================================================================
# # CONFIG
# # ================================================================
# FAST2SMS_API_KEY = "vtDsVxRcVuu4mPJarRaRtFxKqIFOksPjihkHUwolaKJKmzf3ZpgFSg1jnRjl"  # paste your key here
# ALERT_TO_NUMBER  = "8010486078"         # 10 digits, no +91

# ALERT_COOLDOWN_SECONDS = 60
# ALERT_ON               = ["sujal"]    # names that trigger alert
# VOICE_ALERTS           = True

# # ================================================================
# # INTERNAL STATE
# # ================================================================
# _last_alert_time = {}
# _alert_lock      = threading.Lock()

# # ================================================================
# # VOICE
# # ================================================================
# def _speak(text):
#     if not VOICE_ALERTS:
#         return
#     def _do():
#         try:
#             from win32com.client import Dispatch
#             Dispatch("SAPI.SpVoice").Speak(text)
#         except Exception:
#             try:
#                 import pyttsx3
#                 e = pyttsx3.init()
#                 e.say(text); e.runAndWait()
#             except Exception:
#                 print(f"[VOICE] {text}")
#     threading.Thread(target=_do, daemon=True).start()

# # ================================================================
# # SMS — Fast2SMS correct format
# # Key goes in the HEADER as "authorization"
# # Request is GET (not POST)
# # ================================================================
# def _send_sms(name, camera_id, timestamp):
#     if FAST2SMS_API_KEY == "YOUR_API_KEY_HERE":
#         print("[ALERT] Set FAST2SMS_API_KEY in alerts.py first")
#         return

#     if name == "Unknown":
#         message = f"CCTV ALERT: Unknown person detected! Camera {camera_id} | {timestamp}"
#     else:
#         message = f"CCTV ALERT: {name} detected on camera {camera_id} | {timestamp}"

#     try:
#         # Fast2SMS API — key must be in HEADER, not in body
#         params = urllib.parse.urlencode({
#             "message":  message,
#             "language": "english",
#             "route":    "v3",          # v3 works on free accounts
#             "numbers":  ALERT_TO_NUMBER,
#         })

#         url = f"https://www.fast2sms.com/dev/bulkV2?{params}"

#         req = urllib.request.Request(
#             url,
#             headers={
#                 "authorization": FAST2SMS_API_KEY,  # key in header only
#                 "Cache-Control": "no-cache",
#             }
#         )

#         with urllib.request.urlopen(req, timeout=10) as resp:
#             result = json.loads(resp.read().decode())

#         print(f"[ALERT] Fast2SMS response: {result}")

#         if result.get("return") is True:
#             print(f"[ALERT] SMS sent successfully to {ALERT_TO_NUMBER}")
#         else:
#             msgs = result.get('message', [])
#             print(f"[ALERT] SMS failed: {msgs}")

#     except urllib.error.HTTPError as e:
#         body = e.read().decode()
#         print(f"[ALERT] HTTP {e.code}: {body}")
#         if e.code == 401:
#             print("[ALERT] 401 = API key rejected")
#             print("        Check: Login fast2sms.com → Profile → Dev API → copy key fresh")
#     except Exception as e:
#         print(f"[ALERT] Error: {e}")

# # ================================================================
# # TRIGGER — called from server.py
# # ================================================================
# def trigger_alert(name, camera_id=0, force=False):
#     if name not in ALERT_ON:
#         return

#     now       = time.time()
#     alert_key = f"{name}_{camera_id}"

#     with _alert_lock:
#         last = _last_alert_time.get(alert_key, 0)
#         if not force and (now - last) < ALERT_COOLDOWN_SECONDS:
#             return
#         _last_alert_time[alert_key] = now

#     timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

#     if name == "Unknown":
#         _speak("Alert! Unknown person detected on camera.")
#     else:
#         _speak(f"Alert! {name} detected on camera.")

#     threading.Thread(
#         target=_send_sms,
#         args=(name, camera_id, timestamp),
#         daemon=True
#     ).start()

#     print(f"[ALERT] Triggered — '{name}' camera {camera_id} at {timestamp}")


# # ================================================================
# # TEST
# # ================================================================
# if __name__ == "__main__":
#     print("=== Alert System Test ===\n")

#     if FAST2SMS_API_KEY == "YOUR_API_KEY_HERE":
#         print("[ERROR] Paste your Fast2SMS API key in alerts.py first")
#         print("        fast2sms.com → Login → Profile icon → Dev API → copy key")
#         exit()

#     key_preview = FAST2SMS_API_KEY[:8] + "*" * max(0, len(FAST2SMS_API_KEY) - 8)
#     print(f"Key     : {key_preview}  (length={len(FAST2SMS_API_KEY)})")
#     print(f"Number  : {ALERT_TO_NUMBER}")
#     print(f"Alert on: {ALERT_ON}\n")

#     print("1. Testing voice...")
#     _speak("Alert system test. Voice is working.")
#     time.sleep(2)

#     print("2. Sending test SMS now...")
#     _send_sms("Test", camera_id=0, timestamp=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
#     time.sleep(5)

#     print("\nDone — check your phone.")

















# """
# alerts.py — Voice alert + Email notification
# Uses Gmail SMTP — free, instant, no DLT/registration needed
# Works on any phone that has email (Gmail app etc.)

# Setup (one time only):
#     1. Go to myaccount.google.com → Security
#     2. Enable 2-Step Verification (required for app passwords)
#     3. Go to myaccount.google.com/apppasswords
#     4. Select app: Mail, Select device: Windows Computer
#     5. Click Generate → copy the 16-character password
#     6. Paste it in GMAIL_APP_PASSWORD below
#        (use your normal Gmail address in GMAIL_FROM)
# """

# import threading
# import time
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime

# # ================================================================
# # CONFIG — fill these 3 fields
# # ================================================================
# GMAIL_FROM        = "sujaljavheri333@gmail.com"      # your Gmail address
# GMAIL_APP_PASSWORD = "bott votw fvyv tmrs"      # 16-char app password (with spaces)
# ALERT_TO_EMAIL    = "kharadkar9876@gmail.com"      # where to send alerts (can be same)

# # To get alert on phone — just use your Gmail on your phone
# # Or use your carrier email gateway:
# #   Airtel  : 10digitnumber@airtelmail.in  → SMS on phone
# #   Jio     : 10digitnumber@jiomail.in     → not supported
# #   BSNL    : 10digitnumber@bsnl.in        → SMS on phone
# # Example: ALERT_TO_EMAIL = "8010486078@airtelmail.in"

# ALERT_COOLDOWN_SECONDS = 10
# ALERT_ON               = ["sujal"]   # names that trigger alert
# VOICE_ALERTS           = True

# # ================================================================
# # INTERNAL STATE
# # ================================================================
# _last_alert_time = {}
# _alert_lock      = threading.Lock()

# # ================================================================
# # VOICE — Windows SAPI, no install needed
# # ================================================================
# def _speak(text):
#     if not VOICE_ALERTS:
#         return
#     def _do():
#         try:
#             from win32com.client import Dispatch
#             Dispatch("SAPI.SpVoice").Speak(text)
#         except Exception:
#             try:
#                 import pyttsx3
#                 e = pyttsx3.init()
#                 e.say(text); e.runAndWait()
#             except Exception:
#                 print(f"[VOICE] {text}")
#     threading.Thread(target=_do, daemon=True).start()

# # ================================================================
# # EMAIL via Gmail SMTP
# # ================================================================
# def _send_email(name, camera_id, timestamp):
#     if GMAIL_FROM == "your_email@gmail.com":
#         print("[ALERT] Fill in GMAIL_FROM and GMAIL_APP_PASSWORD in alerts.py")
#         return

#     if name == "Unknown":
#         subject = "🚨 CCTV ALERT — Unknown Person Detected"
#         body    = (f"ALERT: An unknown person was detected on your CCTV.\n\n"
#                    f"Camera  : {camera_id}\n"
#                    f"Time    : {timestamp}\n\n"
#                    f"Please check your camera feed immediately.\n"
#                    f"Open: http://localhost:5174")
#     else:
#         subject = f"✅ CCTV ALERT — {name} Detected"
#         body    = (f"ALERT: {name} was detected on your CCTV.\n\n"
#                    f"Camera  : {camera_id}\n"
#                    f"Time    : {timestamp}\n\n"
#                    f"Open: http://localhost:5174")

#     try:
#         msg = MIMEMultipart()
#         msg['From']    = GMAIL_FROM
#         msg['To']      = ALERT_TO_EMAIL
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         # Gmail SMTP — port 587 with TLS
#         with smtplib.SMTP('smtp.gmail.com', 587, timeout=15) as server:
#             server.starttls()
#             server.login(GMAIL_FROM, GMAIL_APP_PASSWORD)
#             server.sendmail(GMAIL_FROM, ALERT_TO_EMAIL, msg.as_string())

#         print(f"[ALERT] Email sent to {ALERT_TO_EMAIL} — '{name}' on camera {camera_id}")

#     except smtplib.SMTPAuthenticationError:
#         print("[ALERT] Gmail auth failed — check GMAIL_APP_PASSWORD")
#         print("        Make sure you used an App Password, not your Gmail login password")
#         print("        Get it: myaccount.google.com/apppasswords")
#     except Exception as e:
#         print(f"[ALERT] Email error: {e}")

# # ================================================================
# # TRIGGER — called from server.py
# # ================================================================
# def trigger_alert(name, camera_id=0, force=False):
#     if name not in ALERT_ON:
#         return

#     now       = time.time()
#     alert_key = f"{name}_{camera_id}"

#     with _alert_lock:
#         last = _last_alert_time.get(alert_key, 0)
#         if not force and (now - last) < ALERT_COOLDOWN_SECONDS:
#             return
#         _last_alert_time[alert_key] = now

#     timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

#     if name == "Unknown":
#         _speak("Alert! Unknown person detected on camera.")
#     else:
#         _speak(f"Alert! {name} detected on camera.")

#     threading.Thread(
#         target=_send_email,
#         args=(name, camera_id, timestamp),
#         daemon=True
#     ).start()

#     print(f"[ALERT] Triggered — '{name}' camera {camera_id} at {timestamp}")


# # ================================================================
# # TEST — python alerts.py
# # ================================================================
# if __name__ == "__main__":
#     print("=== Alert System Test ===\n")
#     print(f"From    : {GMAIL_FROM}")
#     print(f"To      : {ALERT_TO_EMAIL}")
#     print(f"Alert on: {ALERT_ON}\n")

#     if GMAIL_FROM == "your_email@gmail.com":
#         print("[ERROR] Fill in GMAIL_FROM and GMAIL_APP_PASSWORD first")
#         print()
#         print("Steps:")
#         print("  1. myaccount.google.com → Security → 2-Step Verification → Enable")
#         print("  2. myaccount.google.com/apppasswords")
#         print("  3. App = Mail, Device = Windows → Generate")
#         print("  4. Paste the 16-char password in GMAIL_APP_PASSWORD")
#         exit()

#     print("1. Testing voice...")
#     _speak("Alert system test. Voice is working.")
#     time.sleep(2)

#     print("2. Sending test email...")
#     _send_email("TestPerson", camera_id=0,
#                 timestamp=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
#     time.sleep(3)

#     print("\nDone — check your email inbox (and spam folder).")


















# """
# alerts.py — Voice alert + Email notification
# Uses Gmail SMTP — free, instant, no DLT/registration needed

# Setup (one time only):
#     1. Go to myaccount.google.com → Security
#     2. Enable 2-Step Verification (required for app passwords)
#     3. Go to myaccount.google.com/apppasswords
#     4. Select app: Mail, Select device: Windows Computer
#     5. Click Generate → copy the 16-character password
#     6. Paste it in GMAIL_APP_PASSWORD below
# """

# import threading
# import time
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime

# # ================================================================
# # CONFIG — fill these 3 fields
# # ================================================================
# GMAIL_FROM         = "sujaljavheri333@gmail.com"
# GMAIL_APP_PASSWORD = "bott votw fvyv tmrs"       # 16-char app password
# ALERT_TO_EMAIL     = "sujaljavheri333@gmail.com"

# # ================================================================
# # CAMERA NAMES — shown in email subject & body
# # ================================================================
# CAMERA_NAMES = {
#     0: "Camera 1 — Main Entrance",
#     1: "Camera 2 — Parking Area",
#     2: "Camera 3 — wagholi_phata Gate",
#     3: "Camera 4 — sumit_home",
# }

# # ================================================================
# # ALERT SETTINGS
# # ================================================================
# ALERT_COOLDOWN_SECONDS = 10   # minimum gap between emails for same person+camera
#                                 # increased from 10s — avoids email spam
# ALERT_ON               = ["sujal"]   # names that trigger alert. Add more: ["sujal", "john"]
# VOICE_ALERTS           = True

# # Dashboard URL shown in the email
# DASHBOARD_URL = "http://localhost:5174"

# # ================================================================
# # INTERNAL STATE
# # ================================================================
# _last_alert_time = {}   # key = "name_camid"
# _alert_lock      = threading.Lock()

# # ================================================================
# # VOICE — Windows SAPI, no install needed
# # ================================================================
# def _speak(text):
#     if not VOICE_ALERTS:
#         return
#     def _do():
#         try:
#             from win32com.client import Dispatch
#             Dispatch("SAPI.SpVoice").Speak(text)
#         except Exception:
#             try:
#                 import pyttsx3
#                 e = pyttsx3.init()
#                 e.say(text); e.runAndWait()
#             except Exception:
#                 print(f"[VOICE] {text}")
#     threading.Thread(target=_do, daemon=True).start()

# # ================================================================
# # EMAIL via Gmail SMTP
# # ================================================================
# def _send_email(name, camera_id, timestamp, date_str):
#     if GMAIL_FROM == "sujaljavheri333@gmail.com":
#         print("[ALERT] Fill in GMAIL_FROM and GMAIL_APP_PASSWORD in alerts.py")
#         return

#     cam_name = CAMERA_NAMES.get(camera_id, f"Camera {camera_id}")

#     # ---- Subject ----
#     if name == "Unknown":
#         subject = f"🚨 CCTV ALERT — Unknown Person | {cam_name} | {timestamp}"
#     else:
#         subject = f"✅ CCTV ALERT — {name} Detected | {cam_name} | {timestamp}"

#     # ---- Body ----
#     separator = "─" * 48

#     if name == "Unknown":
#         body = f"""
# CCTV FACE RECOGNITION SYSTEM — ALERT
# {separator}

#   STATUS   : ⚠️  UNKNOWN PERSON DETECTED
#   CAMERA   : {cam_name}
#   DATE     : {date_str}
#   TIME     : {timestamp}

# {separator}

# An unrecognized face was detected by your CCTV system.

# Please check your camera feed immediately:
#   → {DASHBOARD_URL}

# {separator}
# GH Raisoni College · CSE-AI · FYP 2025–26
# This is an automated alert from your CCTV system.
# """
#     else:
#         body = f"""
# CCTV FACE RECOGNITION SYSTEM — ALERT
# {separator}

#   STATUS   : ✅  PERSON DETECTED
#   NAME     : {name}
#   CAMERA   : {cam_name}
#   DATE     : {date_str}
#   TIME     : {timestamp}

# {separator}

# {name} was identified by your CCTV face recognition system.

# View live feed:
#   → {DASHBOARD_URL}

# {separator}
# GH Raisoni College · CSE-AI · FYP 2025–26
# This is an automated alert from your CCTV system.
# """

#     try:
#         msg = MIMEMultipart()
#         msg['From']    = GMAIL_FROM
#         msg['To']      = ALERT_TO_EMAIL
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         with smtplib.SMTP('smtp.gmail.com', 587, timeout=15) as server:
#             server.starttls()
#             server.login(GMAIL_FROM, GMAIL_APP_PASSWORD)
#             server.sendmail(GMAIL_FROM, ALERT_TO_EMAIL, msg.as_string())

#         print(f"[ALERT] ✅ Email sent → {ALERT_TO_EMAIL}")
#         print(f"         Person  : {name}")
#         print(f"         Camera  : {cam_name}")
#         print(f"         Time    : {timestamp}")

#     except smtplib.SMTPAuthenticationError:
#         print("[ALERT] ❌ Gmail auth failed — check GMAIL_APP_PASSWORD")
#         print("           Get app password: myaccount.google.com/apppasswords")
#     except Exception as e:
#         print(f"[ALERT] ❌ Email error: {e}")

# # ================================================================
# # TRIGGER — called from server.py on every detection
# # Cooldown prevents email spam for continuous detections
# # ================================================================
# def trigger_alert(name, camera_id=0, force=False):
#     if name not in ALERT_ON:
#         return

#     now       = time.time()
#     alert_key = f"{name}_{camera_id}"

#     with _alert_lock:
#         last = _last_alert_time.get(alert_key, 0)
#         if not force and (now - last) < ALERT_COOLDOWN_SECONDS:
#             remaining = int(ALERT_COOLDOWN_SECONDS - (now - last))
#             # Uncomment below line to see cooldown countdown in terminal:
#             # print(f"[ALERT] Cooldown — next alert for '{name}' in {remaining}s")
#             return
#         _last_alert_time[alert_key] = now

#     now_dt    = datetime.now()
#     timestamp = now_dt.strftime("%H:%M:%S")
#     date_str  = now_dt.strftime("%d %B %Y")   # e.g. "27 March 2026"

#     # Voice alert (non-blocking)
#     cam_name = CAMERA_NAMES.get(camera_id, f"Camera {camera_id}")
#     if name == "Unknown":
#         _speak(f"Alert! Unknown person detected on {cam_name}.")
#     else:
#         _speak(f"Alert! {name} detected on {cam_name}.")

#     # Email (non-blocking thread so it doesn't slow the video stream)
#     threading.Thread(
#         target=_send_email,
#         args=(name, camera_id, timestamp, date_str),
#         daemon=True
#     ).start()

#     print(f"[ALERT] Triggered — '{name}' on {cam_name} at {timestamp}")


# # ================================================================
# # TEST — run: python alerts.py
# # ================================================================
# if __name__ == "__main__":
#     print("=== Alert System Test ===\n")
#     print(f"From      : {GMAIL_FROM}")
#     print(f"To        : {ALERT_TO_EMAIL}")
#     print(f"Alert on  : {ALERT_ON}")
#     print(f"Cooldown  : {ALERT_COOLDOWN_SECONDS}s\n")

#     if GMAIL_FROM == "sujaljavheri333@gmail.com":
#         print("[ERROR] Fill in GMAIL_FROM and GMAIL_APP_PASSWORD first")
#         exit()

#     print("1. Testing voice...")
#     _speak("Alert system test. Voice is working.")
#     time.sleep(2)

#     print("2. Sending test email for known person (camera 0)...")
#     trigger_alert("sujal", camera_id=0, force=True)
#     time.sleep(4)

#     print("3. Sending test email for unknown person (camera 2)...")
#     # Temporarily add Unknown to ALERT_ON for this test
#     ALERT_ON.append("Unknown")
#     trigger_alert("Unknown", camera_id=2, force=True)
#     time.sleep(4)

#     print("\nDone — check your email inbox (and spam folder).")
#     print("The email subject and body should now show the camera name and exact time.")








#neww2

"""
alerts.py — Voice alert + Email notification
Uses Gmail SMTP — free, instant, no DLT/registration needed
"""

import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ================================================================
# CONFIG
# ================================================================
GMAIL_FROM         = "sujaljavheri333@gmail.com"
GMAIL_APP_PASSWORD = "bott votw fvyv tmrs"
ALERT_TO_EMAIL     = "sujaljavheri333@gmail.com"

CAMERA_NAMES = {
    0: "Camera 1 — Main Entrance",
    1: "Camera 2 — Parking Area",
    2: "Camera 3 — Wagholi Phata Gate",
    3: "Camera 4 — Sumit Home",
}

ALERT_COOLDOWN_SECONDS = 30
ALERT_ON               = ["sujal" ,"soham"]   # names that trigger alert
VOICE_ALERTS           = True
DASHBOARD_URL          = "http://localhost:5174"

# ================================================================
# INTERNAL STATE
# ================================================================
_last_alert_time = {}
_alert_lock      = threading.Lock()

# ================================================================
# VOICE
# ================================================================
def _speak(text):
    if not VOICE_ALERTS:
        return
    def _do():
        try:
            from win32com.client import Dispatch
            Dispatch("SAPI.SpVoice").Speak(text)
        except Exception:
            try:
                import pyttsx3
                e = pyttsx3.init()
                e.say(text); e.runAndWait()
            except Exception:
                print(f"[VOICE] {text}")
    threading.Thread(target=_do, daemon=True).start()

# ================================================================
# EMAIL
# ================================================================
def _send_email(name, camera_id, timestamp, date_str):
    cam_name  = CAMERA_NAMES.get(camera_id, f"Camera {camera_id}")
    separator = "─" * 48

    if name == "Unknown":
        subject = f"🚨 CCTV ALERT — Unknown Person | {cam_name} | {timestamp}"
        body = f"""
CCTV FACE RECOGNITION SYSTEM — ALERT
{separator}

  STATUS   : ⚠️  UNKNOWN PERSON DETECTED
  CAMERA   : {cam_name}
  DATE     : {date_str}
  TIME     : {timestamp}

{separator}

An unrecognized face was detected by your CCTV system.

Please check your camera feed immediately:
  → {DASHBOARD_URL}

{separator}
GH Raisoni College · CSE-AI · FYP 2025-26
This is an automated alert from your CCTV system.
"""
    else:
        subject = f"✅ CCTV ALERT — {name} Detected | {cam_name} | {timestamp}"
        body = f"""
CCTV FACE RECOGNITION SYSTEM — ALERT
{separator}

  STATUS   : ✅  PERSON DETECTED
  NAME     : {name}
  CAMERA   : {cam_name}
  DATE     : {date_str}
  TIME     : {timestamp}

{separator}

{name} was identified by your CCTV face recognition system.

View live feed:
  → {DASHBOARD_URL}

{separator}
GH Raisoni College · CSE-AI · FYP 2025-26
This is an automated alert from your CCTV system.
"""

    try:
        msg            = MIMEMultipart()
        msg['From']    = GMAIL_FROM
        msg['To']      = ALERT_TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587, timeout=15) as server:
            server.starttls()
            server.login(GMAIL_FROM, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_FROM, ALERT_TO_EMAIL, msg.as_string())

        print(f"[ALERT] ✅ Email sent → {ALERT_TO_EMAIL}")
        print(f"         Person : {name}")
        print(f"         Camera : {cam_name}")
        print(f"         Time   : {timestamp}")

    except smtplib.SMTPAuthenticationError:
        print("[ALERT] ❌ Gmail auth failed — check GMAIL_APP_PASSWORD")
        print("           myaccount.google.com/apppasswords")
    except Exception as e:
        print(f"[ALERT] ❌ Email error: {e}")

# ================================================================
# TRIGGER — called from server.py on every detection
# ================================================================
def trigger_alert(name, camera_id=0, force=False):
    if name not in ALERT_ON:
        return

    now       = time.time()
    alert_key = f"{name}_{camera_id}"

    with _alert_lock:
        last = _last_alert_time.get(alert_key, 0)
        if not force and (now - last) < ALERT_COOLDOWN_SECONDS:
            return
        _last_alert_time[alert_key] = now

    now_dt    = datetime.now()
    timestamp = now_dt.strftime("%H:%M:%S")
    date_str  = now_dt.strftime("%d %B %Y")

    cam_name = CAMERA_NAMES.get(camera_id, f"Camera {camera_id}")
    if name == "Unknown":
        _speak(f"Alert! Unknown person detected on {cam_name}.")
    else:
        _speak(f"Alert! {name} detected on {cam_name}.")

    threading.Thread(
        target=_send_email,
        args=(name, camera_id, timestamp, date_str),
        daemon=True
    ).start()

    print(f"[ALERT] Triggered — '{name}' on {cam_name} at {timestamp}")


# ================================================================
# TEST — python alerts.py
# ================================================================
if __name__ == "__main__":
    print("=== Alert System Test ===\n")
    print(f"From     : {GMAIL_FROM}")
    print(f"To       : {ALERT_TO_EMAIL}")
    print(f"Alert on : {ALERT_ON}")
    print(f"Cooldown : {ALERT_COOLDOWN_SECONDS}s\n")

    print("1. Testing voice...")
    _speak("Alert system test. Voice is working.")
    time.sleep(2)

    print("2. Sending test email — known person (camera 0)...")
    trigger_alert("sujal", camera_id=0, force=True)
    time.sleep(4)

    print("3. Sending test email — unknown person (camera 2)...")
    trigger_alert("Unknown", camera_id=2, force=True)
    time.sleep(4)

    print("\nDone — check inbox and spam folder.")