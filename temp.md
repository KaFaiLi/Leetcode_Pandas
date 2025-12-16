import base64
import csv
import gzip
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

# Constants from encryption.py
ENCRYPTED_PREFIX = "$enc:"
FLAG_COMPRESSED = 0x01

def decrypt_field(encrypted_str: str, key_bytes: bytes) -> Any:
    """
    Decrypts a field following the AzureMiddleware encryption format:
    $enc:BASE64([flags:1][nonce:12][ciphertext:N])
    """
    if not isinstance(encrypted_str, str) or not encrypted_str.startswith(ENCRYPTED_PREFIX):
        return encrypted_str

    try:
        # Remove prefix and decode base64
        b64_data = encrypted_str[len(ENCRYPTED_PREFIX):]
        data = base64.b64decode(b64_data)
        
        if len(data) < 13: # 1 byte flags + 12 bytes nonce
            return "<Invalid Blob>"

        # Extract components
        flags = data[0]
        nonce = data[1:13]
        ciphertext = data[13:]
        
        # Decrypt using AES-GCM
        aesgcm = AESGCM(key_bytes)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Decompress if the compression flag is set
        if flags & FLAG_COMPRESSED:
            plaintext = gzip.decompress(plaintext)
            
        # Parse JSON
        return json.loads(plaintext.decode("utf-8"))
        
    except Exception as e:
        return f"<Decryption Failed: {e}>"

def process_log_file(file_path: Path, key_bytes: bytes) -> List[Dict[str, Any]]:
    rows = []
    print(f"Processing {file_path}...")
    
    try:
        # Log files are plain text JSONL (not gzipped themselves)
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    entry = json.loads(line)
                    
                    # Decrypt request (key is 'request_encrypted')
                    req_enc = entry.get("request_encrypted")
                    request_body = decrypt_field(req_enc, key_bytes) if req_enc else None
                    
                    # Decrypt response (key is 'response_encrypted')
                    res_enc = entry.get("response_encrypted")
                    response_body = decrypt_field(res_enc, key_bytes) if res_enc else None

                    # Flatten for CSV
                    row = {
                        "timestamp": entry.get("timestamp"),
                        "user": entry.get("user"),
                        "endpoint": entry.get("endpoint"),
                        "method": entry.get("method"),
                        "deployment": entry.get("deployment"),
                        "cost_eur": entry.get("cost_eur"),
                        "status_code": entry.get("status_code"),
                        "duration_ms": entry.get("duration_ms"),
                        "error": entry.get("error"),
                        
                        # Store decrypted bodies as JSON strings
                        "request_body": json.dumps(request_body, ensure_ascii=False) if request_body else "",
                        "response_body": json.dumps(response_body, ensure_ascii=False) if response_body else "",
                    }
                    rows.append(row)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line in {file_path}")
                    
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
                
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
