# Ransomware Simulator Project - Information Security

## Overview
This project simulates a **ransomware attack** for educational and testing purposes. It encrypts target files within the current directory using AES encryption and demands a "ransom key" for decryption. The simulator demonstrates the mechanisms used by real ransomware to teach about cybersecurity threats and the importance of backups.

> **Warning**: This project is intended for educational use only. Do not use this code maliciously, as doing so violates laws and ethical standards.

---

## Features
- **Encryption**: Encrypts specific file types (`.txt`, `.md`, `.log`, `.csv`, `.docx`) using AES in CBC mode.
- **Decryption**: Restores encrypted files when the correct ransom key is provided.
- **Simulated Ransom Demand**: Displays a Bitcoin wallet address for "payment."
- **Key Management**: Securely generates and stores unique encryption keys for each file.
- **Logging**: Records all actions (encryption, decryption, errors) in a log file.
- **Interactive Interface**: Guides the user through the simulated attack and recovery process.

---

## How It Works
1. **File Discovery**: Identifies files with specified extensions in the current directory.
2. **Encryption**:
   - Encrypts files using randomly generated AES keys and IVs.
   - Removes original files after encryption.
   - Stores the keys and IVs in a secure key file.
3. **Ransom Message**: Displays a ransom demand with a Bitcoin wallet address.
4. **Decryption**:
   - Verifies the provided ransom key.
   - Decrypts files and restores them to their original state.

---

## Setup

### Prerequisites
- Python 3.6 or above
- Install required Python libraries:
  ```bash
  pip install pycryptodome tqdm colorama
  ```

---

## Usage

### Running the Simulator
1. Clone this repository and navigate to the project directory:
   ```bash
   git clone Ransomware-Simulator
   cd Ransomware-Simulator
   ```
2. Run the script:
   ```bash
   main.py
   ```

### Simulation Steps
1. The script encrypts all target files in the directory and displays a ransom message.
2. To decrypt files:
   - Enter the ransom key provided during encryption.
   - Files will be restored upon verification.

---

## Files and Logs
- **`ENCRYPTION_KEYS.secure`**: Stores encryption keys and IVs (required for decryption).
- **`ransomware_log.txt`**: Records actions for auditing and debugging.

---

## Important Notes
- **Testing Only**: Do not execute this script on sensitive or production data.
- **File Safety**: Backup your files before running the script.
- **Ethical Use**: This project is for learning purposes only. Misuse is strictly prohibited.

