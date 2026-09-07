from login_system import LoginSystem
from serial_bridge import SerialBridge
from staff_menu import StaffMenu
from admin_menu import AdminMenu
from database import get_role

def main():
    # Create and connect the serial bridge to the Arduino
    bridge = SerialBridge()
    if not bridge.connect():
        print("Could not connect to Arduino, alarm control will not work")
        print("Continuing in local mode...")

    # Create login system and run the auth
    login = LoginSystem()

    while True:
        # Run login and get the authenticated username
        username = login.start()

        if not username:
            print("Login failed, exiting")
            bridge.disconnect()
            break

        # Look up the user's role and route to the correct menu
        role = get_role(username)

        if role == "ADMIN":
            menu = AdminMenu(username, bridge)
        else:
            menu = StaffMenu(username, bridge)

        # After logout loop back to the login menu screen
        menu.run()
        print("\nReturning to login screen...")


if __name__ == "__main__":
    main()