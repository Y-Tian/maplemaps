from firebase_admin import credentials, initialize_app, storage
import config.conf as conf
import os
import time

"""
NOTE change the variables here for source & target folders
"""
LOCAL_UPLOAD_DIR = f"{conf.LOCAL_FILE_PATH_BUILDER}/mobs/raw"
TARGET_GCS_FOLDER = "raw/mobs"

#############################

print("Starting sync...")
start_t = time.time()

cred = credentials.Certificate(conf.FIREBASE_CREDS)
initialize_app(cred, {"storageBucket": conf.FIREBASE_URL})

bucket = storage.bucket()

size_of_dir = len(os.listdir(LOCAL_UPLOAD_DIR))

process_counter = 0
directory = os.fsencode(LOCAL_UPLOAD_DIR)
for file in os.listdir(directory):
    process_counter += 1
    filename = os.fsdecode(file)
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        print(f"Uploading: {filename} - {process_counter}/{size_of_dir}")
        blob = bucket.blob(f"{TARGET_GCS_FOLDER}/{filename}")
        blob.upload_from_filename(f"{LOCAL_UPLOAD_DIR}/{filename}")
    elif os.path.isdir(f"{LOCAL_UPLOAD_DIR}/{filename}"):
        for nested_file in os.listdir(f"{LOCAL_UPLOAD_DIR}/{filename}"):
            print(f"Uploading folder: {filename}/{nested_file} - {process_counter}/{size_of_dir}")
            blob = bucket.blob(f"{TARGET_GCS_FOLDER}/{filename}/{nested_file}")
            blob.upload_from_filename(f"{LOCAL_UPLOAD_DIR}/{filename}/{nested_file}")
    else:
        print(f"Skipping file: {filename} - {process_counter}/{size_of_dir}")

print(f"Completed. Took {int(time.time() - start_t)} seconds.")
