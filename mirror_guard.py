import os
import time
import hashlib
import threading
import datetime

# 👁️ Watch these files
WATCHED_FILES = [
    "mirror_ui.py",
    "mirror_guard.py",
    "mirror_toolkit.py",
    "mirror_layer_two.py",
    "mirror_system.py"
]

# 🧠 Store last known hashes
file_hashes = {}

# 🧮 Hashing function
def hash_file(filepath):
    try:
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            return file_hash
    except Exception as e:
        return f"ERROR: {str(e)}"

# 📊 Get info for UI panel
def get_file_info():
    status = []
    for file in WATCHED_FILES:
        try:
            last_mod = os.path.getmtime(file)
            last_mod_str = datetime.datetime.fromtimestamp(last_mod).strftime('%Y-%m-%d %H:%M:%S')
            file_hash = hash_file(file)
            status.append({
                "file": file,
                "last_modified": last_mod_str,
                "hash": file_hash
            })
        except Exception as e:
            status.append({
                "file": file,
                "error": str(e)
            })
    return status

# 🚨 Background watcher
def watch(interval=5):
    print("🛡️ mirror_guard activated...")
    global file_hashes

    # Initialize hashes
    for file in WATCHED_FILES:
        file_hashes[file] = hash_file(file)

    while True:
        for file in WATCHED_FILES:
            new_hash = hash_file(file)
            if new_hash != file_hashes.get(file):
                print(f"⚠️ File changed: {file}")
                print(f"  Old: {file_hashes.get(file)}")
                print(f"  New: {new_hash}")
                file_hashes[file] = new_hash
        time.sleep(interval)

if __name__ == "__main__":
    watch()
