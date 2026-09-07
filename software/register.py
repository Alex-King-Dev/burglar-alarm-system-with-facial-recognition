import cv2
import dlib
import os
import time
from config import KNOWN_FACES_DIR, CAMERA_INDEX, CAMERA_WARMUP_FRAMES
from database import add_user, user_exists


def capture_and_register(admin_username):
    # function is only callable by an authenticated admin
    # Saves photo to known_faces/ and stores all data in database.json

    print("\n--- Register New User ---")
    print("Registering as admin:", admin_username)

    # simple input for a username
    while True:
        username = input("Enter a username for the new user: ").strip()
        if not username:
            print("Username cannot be empty")
            continue
        if user_exists(username):
            print("Username already exists, choose another")
            continue
        break

    # simple inputt for a 4-digit PIN
    while True:
        pin = input("Set a 4-digit PIN for the new user: ").strip()
        if len(pin) == 4 and pin.isdigit():
            break
        print("PIN must be exactly 4 digits")

    # Ask for a role
    while True:
        print("Select role for new user:")
        print("  1. Staff")
        print("  2. Admin")
        role_choice = input("Enter 1 or 2: ").strip()
        if role_choice == "1":
            role = "STAFF"
            break
        elif role_choice == "2":
            role = "ADMIN"
            break
        print("Please enter 1 or 2")

    # Load dlib models
    print("Loading face models...")
    detector = dlib.get_frontal_face_detector()

    # python opencv / dlib files that works alongside  our face auth system based off online material
    predictor_path = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")
    encoder_path = os.path.join(os.path.dirname(__file__), "dlib_face_recognition_resnet_model_v1.dat")

    if not os.path.exists(predictor_path):
        print("Error: shape_predictor_68_face_landmarks.dat not found in script folder")
        return False
    if not os.path.exists(encoder_path):
        print("Error: dlib_face_recognition_resnet_model_v1.dat not found in script folder")
        return False

    shape_predictor = dlib.shape_predictor(predictor_path)
    face_encoder = dlib.face_recognition_model_v1(encoder_path)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    # Open webcam
    print("Opening webcam...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: could not open webcam at index", CAMERA_INDEX)
        return False

    # Give the C270 time to fully initialise before reading frames
    print("Warming up camera...")
    time.sleep(2)
    for i in range(CAMERA_WARMUP_FRAMES):
        cap.read()

    print("Ready! Look at the camera and press S to capture, Q to cancel")

    captured_frame = None


    ### From here on downwards, code from online material found (link in my bookmarks)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: could not read frame from webcam")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        hint = "Face detected! Press S to capture" if len(faces) > 0 else "No face detected - move closer"
        cv2.putText(frame, hint, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.imshow("Register - " + username, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            if len(faces) == 0:
                print("No face in frame, try again")
                continue
            captured_frame = frame.copy()
            print("Frame captured! Computing face encoding, please wait...")
            break

        if key == ord('q'):
            print("Registration cancelled")
            cap.release()
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            return False

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    if captured_frame is None:
        print("Registration failed, no face captured")
        return False

    # Step 2: compute encoding AFTER closing webcam so nothing is frozen
    rgb = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2RGB)
    detections = detector(rgb, 1)

    if len(detections) == 0:
        print("Error: no face found in captured frame, please try again")
        return False

    shape = shape_predictor(rgb, detections[0])
    encoding = list(face_encoder.compute_face_descriptor(rgb, shape))
    print("Face encoding computed successfully")

    # Save the captured image to known_faces/
    image_filename = username + ".jpg"
    image_path = os.path.join(KNOWN_FACES_DIR, image_filename)
    cv2.imwrite(image_path, captured_frame)
    print("Face image saved to known_faces/" + image_filename)

    # Store username, PIN, encoding and role in the database
    add_user(username, pin, encoding, image_filename, role)
    print("Registration complete for user:", username, "(" + role + ")")
    return True