import time
from authenticator import Authenticator
from config import MAX_PIN_ATTEMPTS, LOCKOUT_SECONDS
from database import check_pin, user_exists


class PINAuthenticator(Authenticator):
    # Authenticates the user using a username and 4-digit PIN
    # Returns the authenticated username on success so the menu can be routed correctly

    def __init__(self):
        super().__init__(max_attempts=MAX_PIN_ATTEMPTS)
        self.authenticated_user = None

    def _get_credentials(self):
        # Prompt for username first, reject immediately if not registered
        while True:
            username = input("Enter username: ").strip()
            if not user_exists(username):
                print("Username not found:", username)
                continue
            break

        pin = input("Enter 4-digit PIN: ").strip()
        return username, pin

    def authenticate(self):
        # Ask for credentials and validate against the database
        # Returns True and stores username if correct, False otherwise
        username, pin = self._get_credentials()

        if len(pin) != 4 or not pin.isdigit():
            print("Invalid input: PIN must be exactly 4 digits")
            return False

        if check_pin(username, pin):
            print("PIN authentication successful! Welcome,", username)
            self.authenticated_user = username
            return True

        print("Incorrect PIN")
        return False

    def run(self):
        # Override run() to add lockout behaviour after all attempts fail
        # Returns authenticated username on success, None on failure
        print("\n--- PIN Authentication ---")
        self.authenticated_user = None

        for attempt in range(1, self.max_attempts + 1):
            print("PIN attempt", attempt, "of", self.max_attempts)
            if self.authenticate():
                return self.authenticated_user
            if attempt < self.max_attempts:
                remaining = self.max_attempts - attempt
                print("Wrong credentials.", remaining, "attempt(s) remaining")

        # All attempts exhausted, begin lockout
        print("\nToo many failed PIN attempts!")
        print("Locked out for", LOCKOUT_SECONDS, "seconds...")

        for remaining in range(LOCKOUT_SECONDS, 0, -1):
            print("Unlocking in", remaining, "seconds...", end='\r')
            time.sleep(1)

        print("\nLockout over. You have been logged out.")
        return None