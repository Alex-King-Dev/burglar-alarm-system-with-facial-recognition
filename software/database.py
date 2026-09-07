import json
import os

# Path to the JSON file that stores all registered users
DB_FILE = os.path.join(os.path.dirname(__file__), "database.json")


def _load():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)


def _save(data):
    # Write the full database dict back to disk as JSON
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_user(username, pin, encoding, image_filename, role):
    data = _load()
    data[username] = {
        "pin": pin,
        "encoding": encoding,
        "image": image_filename,
        "role": role.upper()
    }
    _save(data)
    print("User registered:", username, "as", role.upper())


def get_user(username):
    # Return the data dict for a given username, or None if not found
    data = _load()
    return data.get(username, None)


def get_all_users():
    # Return the full database dict of all registered users
    return _load()


def user_exists(username):
    # Return True if the username is already registered
    data = _load()
    return username in data


def check_pin(username, pin):
    # Return True if the given PIN matches the stored PIN for that user
    user = get_user(username)
    if user is None:
        print("User not found:", username)
        return False
    return user["pin"] == pin


def get_role(username):
    # Return the role of a given user (STAFF or ADMIN), or None if not found
    user = get_user(username)
    if user is None:
        return None
    return user.get("role", "STAFF")


def change_pin(username, new_pin):
    # Update the PIN for an existing user
    data = _load()
    if username not in data:
        print("User not found:", username)
        return False
    data[username]["pin"] = new_pin
    _save(data)
    print("PIN updated for:", username)
    return True


def delete_user(username):
    # Remove a user from the database entirely
    data = _load()
    if username not in data:
        print("User not found:", username)
        return False
    del data[username]
    _save(data)
    print("User deleted:", username)
    return True
