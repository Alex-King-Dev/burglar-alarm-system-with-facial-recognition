import os

# Camera index 0 or 1, depending on usb port
CAMERA_INDEX = 1

# Serial communication settings for Arduino connection
SERIAL_PORT = "/dev/cu.usbmodem145401"
BAUD_RATE = 9600
SERIAL_TIMEOUT = 5

# Path to the folder where saved faces images are stored
KNOWN_FACES_DIR = os.path.join(os.path.dirname(__file__), "known_faces")

# Minimum no. of faces detected in the frame to count as a valid detection
FACE_DETECTION_THRESHOLD = 1

# Consecutive frames face must appear in the frame to pass  face authentication
FACE_CONFIRM_FRAMES = 3

# Maximum no. of attempts before falling back to PIN
MAX_FACE_ATTEMPTS = 3
# Maximum no. of attempts before lockout for 30 seconds
MAX_PIN_ATTEMPTS = 3

# Lockout duration if pin is wrong (seconds)
LOCKOUT_SECONDS = 30

# Tolerance for camera
FACE_MATCH_TOLERANCE = 0.6

# startup frames to let the camera sensor warm up
CAMERA_WARMUP_FRAMES = 10

