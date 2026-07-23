import random
import string
import json
import os
from cryptography.fernet import Fernet, InvalidToken

DATA_FILE = "passwords.enc"
KEY_FILE = "secret.key"


def load_key():
    """Load the encryption key, generating one on first run."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key


def load_passwords(fernet):
    """Load and decrypt saved passwords. Returns an empty dict on any failure."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "rb") as f:
            encrypted = f.read()
        if not encrypted:
            return {}
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode("utf-8"))
    except InvalidToken:
        print("Warning: could not decrypt saved data (wrong/missing key). Starting fresh.")
        return {}
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: could not read saved passwords ({e}). Starting fresh.")
        return {}


def save_passwords(passwords, fernet):
    """Encrypt and persist the passwords dict to disk."""
    try:
        data = json.dumps(passwords).encode("utf-8")
        encrypted = fernet.encrypt(data)
        with open(DATA_FILE, "wb") as f:
            f.write(encrypted)
    except OSError as e:
        print(f"Error: could not save passwords ({e}).")


def generate_password(length=12):
    """Generate a random password with letters, digits, and punctuation."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def main():
    key = load_key()
    fernet = Fernet(key)
    passwords = load_passwords(fernet)

    while True:
        print("\n1. Save a new password")
        print("2. View saved passwords")
        print("3. Generate a new password")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            site = input("Enter the site name: ").strip()
            password = input("Enter the password: ").strip()
            if not site or not password:
                print("Site name and password cannot be empty.")
                continue
            passwords[site] = password
            save_passwords(passwords, fernet)
            print(f"Password for '{site}' saved.")

        elif choice == "2":
            if not passwords:
                print("No saved passwords found.")
            else:
                for site, password in passwords.items():
                    print(f"{site}: {password}")

        elif choice == "3":
            site = input("Enter the site name: ").strip()
            if not site:
                print("Site name cannot be empty.")
                continue
            password = generate_password()
            passwords[site] = password
            save_passwords(passwords, fernet)
            print(f"Generated password for '{site}': {password}")

        elif choice == "4":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
