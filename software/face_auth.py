import cv2
import dlib
import time
import os
import numpy as np
from authenticator import Authenticator
from config import MAX_FACE_ATTEMPTS, FACE_DETECTION_THRESHOLD, FACE_CONFIRM_FRAMES, FACE_MATCH_TOLERANCE, CAMERA_INDEX, CAMERA_WARMUP_FRAMES
from database import get_all_users


class FaceAuthenticator(Authenticator):
    # Authenticates the user by comparing their live face encoding
    # against all the registered face encodings stored in our database

    # Returns the authenticated username on success so the menu can be routed correctly

    def __init__(self):
        super().__init__(max_attempts=MAX_FACE_ATTEMPTS)
        self.authenticated_user = None
        self.face_cascade = self._load_cascade()
        self.detector = dlib.get_frontal_face_detector()
        self.shape_predictor = self._load_shape_predictor()
        self.face_encoder = self._load_face_encoder()

    def _load_cascade(self):
        # Load the Haar cascade XML for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        cascade = cv2.CascadeClassifier(cascade_path)
        if cascade.empty():
            print("Error: could not load face cascade classifier")
            return None
        return cascade

    def _load_shape_predictor(self):
        # Load the dlib 68-point shape predictor model
        path = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")
        if not os.path.exists(path):
            print("Error: shape_predictor_68_face_landmarks.dat not found")
            return None
        return dlib.shape_predictor(path)

    def _load_face_encoder(self):
        # Load the dlib face recognition ResNet model
        path = os.path.join(os.path.dirname(__file__), "dlib_face_recognition_resnet_model_v1.dat")
        if not os.path.exists(path):
            print("Error: dlib_face_recognition_resnet_model_v1.dat not found")
            return None
        return dlib.face_recognition_model_v1(path)

    def _get_encoding(self, frame):
        # Compute a 128-d face encoding from a frame, or return None if no face found
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = self.detector(rgb, 1)
        if len(detections) == 0:
            return None
        shape = self.shape_predictor(rgb, detections[0])
        encoding = self.face_encoder.compute_face_descriptor(rgb, shape)
        return list(encoding)

    def _match_encoding(self, encoding):
        # Compare encoding against all registered users
        # Returns the matched username or None
        users = get_all_users()
        if not users:
            print("No registered users found")
            return None
        for username, data in users.items():
            stored = data.get("encoding")
            if stored is None:
                continue
            distance = float(np.linalg.norm(np.array(encoding) - np.array(stored)))
            if distance < FACE_MATCH_TOLERANCE:
                return username
        return None

    def authenticate(self):
        # Scan webcam for a recognised face
        # Returns True and stores username if recognised, False after max fails
        print("Starting face authentication... Press Q to cancel")

        if None in (self.face_cascade, self.shape_predictor, self.face_encoder):
            print("Error: face auth models not loaded correctly")
            return False

        cap = cv2.VideoCapture(CAMERA_INDEX)

        # Give the C270 time to fully initialise before reading frames
        time.sleep(2)
        for _ in range(CAMERA_WARMUP_FRAMES):
            cap.read()

        if not cap.isOpened():
            print("Error: could not open webcam")
            return False

        confirmed_frames = 0
        fail_count = 0
        pending_match = None
        result = False

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: could not read frame from webcam")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if len(faces) >= FACE_DETECTION_THRESHOLD:
                encoding = self._get_encoding(frame)
                if encoding:
                    match = self._match_encoding(encoding)
                    if match:
                        # Recognised face, keep building confirmed frame count
                        pending_match = match
                        confirmed_frames += 1
                    else:
                        if confirmed_frames > 0:
                            # Was mid count, reset without penalising
                            confirmed_frames = 0
                            pending_match = None
                            print("Face interrupted, resetting...")
                        else:
                            # Clean unrecognised face, count as a fail
                            confirmed_frames = 0
                            pending_match = None
                            fail_count += 1
                            print("Unrecognised face. Attempt", fail_count, "of", MAX_FACE_ATTEMPTS)
                            if fail_count >= MAX_FACE_ATTEMPTS:
                                print("Face authentication failed after", MAX_FACE_ATTEMPTS, "attempts")
                                break
                else:
                    if confirmed_frames > 0:
                        confirmed_frames = 0
                        pending_match = None
                        print("Face interrupted, resetting...")
            else:
                # No face in frame, reset count if mid progress
                if confirmed_frames > 0:
                    confirmed_frames = 0
                    pending_match = None
                    print("Face left frame, resetting count...")

            if pending_match:
                status = "Recognised: " + pending_match + " (" + str(confirmed_frames) + "/" + str(FACE_CONFIRM_FRAMES) + ")"
            elif fail_count > 0:
                status = "Unrecognised. Fails: " + str(fail_count) + "/" + str(MAX_FACE_ATTEMPTS)
            else:
                status = "Scanning for known face..."
            cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Face Authentication", frame)

            if confirmed_frames >= FACE_CONFIRM_FRAMES:
                print("Face authentication successful! Welcome,", pending_match)
                self.authenticated_user = pending_match
                result = True
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Face authentication cancelled")
                break

        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        return result

    def run(self):
        # Override run() to return username on success, or None on failure
        print("\n--- Face Authentication ---")
        self.authenticated_user = None

        for attempt in range(1, self.max_attempts + 1):
            print("Face attempt", attempt, "of", self.max_attempts)
            if self.authenticate():
                return self.authenticated_user
            if attempt < self.max_attempts:
                print("Face auth failed, retrying...")

        print("Face authentication failed after", self.max_attempts, "attempts")
        return None