class Authenticator:

    def __init__(self, max_attempts):
        self.max_attempts = max_attempts
        self.authenticated_user = None

    def authenticate(self):
        raise NotImplementedError("Subclasses must implement authenticate()")

    def run(self):
        for attempt in range(1, self.max_attempts + 1):
            print("Attempt", attempt, "of", self.max_attempts)
            if self.authenticate():
                return self.authenticated_user
            if attempt < self.max_attempts:
                print("Authentication failed, retrying...")
        print("All", self.max_attempts, "attempts failed")
        return None