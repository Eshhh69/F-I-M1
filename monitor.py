import hashlib

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

import os

def scan_folder(folder_path):
    hashes = {}

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            hashes[file_name] = calculate_hash(file_path)

    return hashes

import json
import time
from datetime import datetime

folder = "monitored_folder"

with open("baseline.json", "r") as f:
    baseline = json.load(f)

print("Monitoring started...")

while True:
    current = scan_folder(folder)

    # Check for new and modified files
    for file_name, current_hash in current.items():

        if file_name not in baseline:
            alert = f"[{datetime.now()}] [ALERT] New File Created: {file_name}"
            print(alert)

            baseline[file_name] = current_hash

        elif baseline[file_name] != current_hash:
            alert = f"[{datetime.now()}] [ALERT] File Modified: {file_name}"
            print(alert)

            baseline[file_name] = current_hash

    # Check for deleted files
    for file_name in list(baseline.keys()):

        if file_name not in current:
            alert = f"[{datetime.now()}] [ALERT] File Deleted: {file_name}"
            print(alert)

            del baseline[file_name]

    # Save updated baseline
    with open("baseline.json", "w") as f:
        json.dump(baseline, f, indent=4)

    time.sleep(5)