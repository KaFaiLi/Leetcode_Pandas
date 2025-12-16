import base64
import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ================= CONFIGURATION =================
# 1. Paste your Base64 encoded 32-byte encryption key here (from config.yaml)
ENCRYPTION_KEY = "YOUR_BASE64_KEY_HERE"

# 2. Path to a specific .jsonl file or a directory containing logs
INPUT_PATH = "logs/"

# 3. Output CSV file path
OUTPUT_FILE = "decrypted_logs.csv"
# =================================================

def decrypt_data(encrypted_data: str, key_bytes: bytes) -> Any:
    """
    Decrypts a base64 encoded string using AES-GCM.
    Expects the format: nonce (12 bytes) + ciphertext + tag (16 bytes)
    """
    if not encrypted_data:
        return None

    try:
        # Decode the base64 container
        data = base64.b64decode(encrypted_data)
        
        # AES-GCM standard nonce size is 12 bytes
        nonce = data[:12]
        ciphertext = data[12:]
        
        aesgcm = AESGCM(key_bytes)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Parse the JSON content back to a python object
        return json.loads(plaintext.decode("utf-8"))
    except Exception as e:
        # Return the error string so it's visible in the CSV
        return f"<Decryption Failed: {e}>"

def process_log_file(file_path: Path, key_bytes: bytes) -> List[Dict[str, Any]]:
    rows = []
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                entry = json.loads(line)
                
                # Decrypt specific fields if they exist
                if entry.get("request_body"):
                    entry["request_body"] = decrypt_data(entry["request_body"], key_bytes)
                
                if entry.get("response_body"):
                    entry["response_body"] = decrypt_data(entry["response_body"], key_bytes)

                # Flatten for CSV
                row = {
                    "timestamp": entry.get("timestamp"),
                    "request_id": entry.get("request_id"),
                    "username": entry.get("username"),
                    "model": entry.get("model"),
                    "total_tokens": entry.get("total_tokens"),
                    "cost_eur": entry.get("cost_eur"),
                    "status_code": entry.get("status_code"),
                    # Dump JSON bodies to string so they fit in one CSV cell
                    "request_body": json.dumps(entry.get("request_body"), ensure_ascii=False),
                    "response_body": json.dumps(entry.get("response_body"), ensure_ascii=False),
                }
                rows.append(row)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line in {file_path}")
                
    return rows

def main():
    # Validate and decode key
    try:
        key_bytes = base64.b64decode(ENCRYPTION_KEY)
        if len(key_bytes) != 32:
            raise ValueError(f"Key must be 32 bytes, got {len(key_bytes)}")
    except Exception as e:
        print(f"Invalid encryption key configuration: {e}")
        return

    input_path = Path(INPUT_PATH)
    all_rows = []

    # Process single file or directory
    if input_path.is_file():
        all_rows.extend(process_log_file(input_path, key_bytes))
    elif input_path.is_dir():
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith(".jsonl"):
                    all_rows.extend(process_log_file(Path(root) / file, key_bytes))
    else:
        print(f"Input path not found: {input_path}")
        return

    if not all_rows:
        print("No logs found or processed.")
        return

    # Determine CSV headers dynamically based on the first row
    fieldnames = list(all_rows[0].keys())
    
    # Ensure timestamp is first if present
    if "timestamp" in fieldnames:
        fieldnames.remove("timestamp")
        fieldnames.insert(0, "timestamp")

    # Write to CSV
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"Successfully exported {len(all_rows)} log entries to {OUTPUT_FILE}")
    except IOError as e:
        print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    main()
