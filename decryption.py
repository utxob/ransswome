import os
import hashlib
import time
import pyautogui
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from tqdm import tqdm

# 🖥️ Desktop Path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# 🔑 Hardcoded Password (Same as encryption)
PASSWORD = "1234"

def derive_key(password: str) -> bytes:
    """Generate a 32-byte decryption key using SHA-256."""
    return hashlib.sha256(password.encode()).digest()

def decrypt_file(encrypted_file: str, key: bytes):
    """Decrypt a file and restore the original."""
    decrypted_file = encrypted_file.replace(".enc", "")

    try:
        with open(encrypted_file, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        with open(decrypted_file, 'wb') as f:
            f.write(plaintext)

        os.remove(encrypted_file)  # Delete the encrypted file
    except Exception as e:
        print(f"Error decrypting {encrypted_file}: {str(e)}")

def decrypt_all_files():
    """Decrypt all .enc files in the Desktop directory with a loading bar."""
    key = derive_key(PASSWORD)
    enc_files = [os.path.join(root, file) for root, _, files in os.walk(desktop_path) for file in files if file.endswith(".enc")]

    if not enc_files:
        pyautogui.alert("No encrypted files found!", "Decryption Failed")
        return

    print("YOUR file decryption Processing...")
    for file in tqdm(enc_files, desc="Decrypting", unit="file"):
        decrypt_file(file, key)
        time.sleep(0.5)  # Simulate decryption delay
    
    pyautogui.alert("All files have been decrypted successfully!", "Decryption Complete")

# 📌 Run the decryption process
decrypt_all_files()
