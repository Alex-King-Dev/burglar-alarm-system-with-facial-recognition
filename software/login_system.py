from face_auth import FaceAuthenticator
from pin_auth import PINAuthenticator


class LoginSystem:
    # Orchestrates the login flow
    # Routes to staff or admin menu after successful authentication

    def __init__(self):
        self.face_auth = FaceAuthenticator()
        self.pin_auth = PINAuthenticator()

    def _get_user_choice(self):
        # Prompt user to select a login method and return their choice
        print("\n=== Burglar Alarm Login ===")
        print("Choose authentication method:")
        print("  1. Face recognition")
        print("  2. PIN")

        while True:
            choice = input("Enter 1 or 2: ").strip()
            if choice in ("1", "2"):
                return choice
            print("Please enter 1 or 2")

    def start(self):
        # Keep showing the login menu until successful auth or denial
        while True:
            choice = self._get_user_choice()

            if choice == "1":
                # Face auth with PIN fallback
                print("\n--- Face Authentication ---")
                username = self.face_auth.run()
                if not username:
                    print("Falling back to PIN authentication...")
                    username = self.pin_auth.run()
            else:
                username = self.pin_auth.run()

            if username:
                return username
            else:
                print("\nAccess denied.")
                break