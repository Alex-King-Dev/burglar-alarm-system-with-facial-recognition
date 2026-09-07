from serial_bridge import SerialBridge

class StaffMenu:
    # Menu for staff users, a much more simpler version of admin menu

    def __init__(self, username, bridge):
        self.username = username
        self.bridge = bridge

    def _display_status(self):
        status = self.bridge.get_status()
        if status:
            print("Alarm status:", status)
        else:
            print("Could not retrieve alarm status")

    def _arm(self):
        self.bridge.arm()

    def _disarm(self):
        self.bridge.disarm()

    def _print_menu(self):
        print("\n--- Staff Menu ---")
        self._display_status()
        print("  1. Arm alarm")
        print("  2. Disarm alarm")
        print("  3. Logout")

    def run(self):
        print("\nWelcome,", self.username, "(STAFF)")

        while True:
            self._print_menu()
            choice = input("Enter choice: ").strip()

            # Clear alarm event after input
            self.bridge.alarm_event.clear()

            if choice == "1":
                self._arm()
            elif choice == "2":
                self._disarm()
            elif choice == "3":
                print("Logging out:", self.username)
                break
            else:
                print("Invalid choice, please try again")