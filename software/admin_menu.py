import sys
import select
from database import get_all_users, delete_user, change_pin, user_exists
from register import capture_and_register

class AdminMenu:
    # Menu for admins

    # admin menu initialisation
    def __init__(self, username, bridge):
        self.username = username
        self.bridge = bridge #Main attribute which connects to arduino

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

    def _view_sensors(self):
        sensors = self.bridge.get_sensors()
        if sensors:
            print("\n--- Sensor Status ---")
            for sensor_id, state in sensors.items():
                print(sensor_id, ":", "TRIGGERED" if state else "OK")
        else:
            print("Could not retrieve sensor status")

    def _view_actuators(self):
        actuators = self.bridge.get_actuators()
        if actuators:
            print("\n--- Actuator Status ---")
            for actuator_id, state in actuators.items():
                print(actuator_id, ":", "ON" if state else "OFF")
        else:
            print("Could not retrieve actuator status")

    # add user to the database
    def _add_user(self):
        capture_and_register(self.username)

    # delete user from database
    def _delete_user(self):
        print("\n--- Delete User ---")
        users = get_all_users()
        if not users:
            print("No users registered")
            return
        print("Registered users:")

        for username in users:
            print(" -", username, "(" + users[username]["role"] + ")")
        while True:
            target = input("Enter username to delete (or Q to cancel): ").strip()

            if target.lower() == "q":
                print("Cancelled")
                return

            # stop from deleting own account
            if target == self.username:
                print("You cannot delete your own account")
                continue

            # if name not in lisst
            if not user_exists(target):
                print("Username not found:", target)
                continue
            break

        confirm = input("Are you sure you want to delete " + target + "? (yes/no): ").strip().lower()
        if confirm == "yes":
            delete_user(target)
        else:
            print("Deletion cancelled")

    def _change_pin(self):
        print("\n--- Change User PIN ---")
        users = get_all_users()
        if not users:
            print("No users registered")
            return
        print("Registered users:")
        for username in users:
            print(" -", username, "(" + users[username]["role"] + ")")
        while True:
            target = input("Enter username to change PIN (or Q to cancel): ").strip()
            if target.lower() == "q":
                print("Cancelled")
                return
            if not user_exists(target):
                print("Username not found:", target)
                continue
            break
        while True:
            new_pin = input("Enter new 4-digit PIN: ").strip()
            if len(new_pin) == 4 and new_pin.isdigit():
                break
            print("PIN must be exactly 4 digits")
        change_pin(target, new_pin)

    def _list_users(self):
        print("\n--- Registered Users ---")
        users = get_all_users()
        if not users:
            print("No users registered")
            return
        for username, data in users.items():
            print(" -", username, "(" + data["role"] + ")")

    def _print_menu(self):
        print("\n--- Admin Menu ---")
        self._display_status()
        print("  1. Arm alarm")
        print("  2. Disarm alarm")
        print("  3. View sensor status")
        print("  4. View actuator status")
        print("  5. Add new user")
        print("  6. Delete user")
        print("  7. Change user PIN")
        print("  8. List all users")
        print("  9. Logout")
        print("Enter choice: ", end="", flush=True)

    def _get_choice(self):
        # Returns choice string if available, None if alarm triggered
        while True:
            # Check for alarm trigger first in case of an interrupt
            if self.bridge.alarm_event.is_set():
                return None

            # I researched a way to get a user input that doesnt freeze the system (isnt stuck waiting,
            # so it can detect alarm trigger whilst waiting for menu input):
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            if ready:
                return sys.stdin.readline().strip()

    def run(self):
        print("\nWelcome,", self.username, "(ADMIN)")

        while True:
            self._print_menu()
            choice = self._get_choice()

            # reprints menu if alarm triggered mid menu
            if choice is None:
                self.bridge.alarm_event.clear()
                continue

            if choice == "1":
                self._arm()
            elif choice == "2":
                self._disarm()
            elif choice == "3":
                self._view_sensors()
            elif choice == "4":
                self._view_actuators()
            elif choice == "5":
                self._add_user()
            elif choice == "6":
                self._delete_user()
            elif choice == "7":
                self._change_pin()
            elif choice == "8":
                self._list_users()
            elif choice == "9":
                print("Logging out:", self.username)
                break
            else:
                print("Invalid choice, please try again")