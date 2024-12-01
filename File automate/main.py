import os
import shutil
import time

SIZE_LIMIT_MB = 500  # Maximum size per folder in MB
SIZE_LIMIT_BYTES = SIZE_LIMIT_MB * 1024 * 1024
LARGE_FILE_SIZE = 50 * 1024 * 1024
RETENTION_DAYS = 30  # Days after which files will be archived

# To calculate folder size
def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

# Folders exceeding size limits
def handle_exceeding_folder(folder_path):
    # Create Archive folder if not exists
    archive_folder = os.path.join(folder_path, "Archive")
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    current_time = time.time()

    # Archive files older than RETENTION_DAYS
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file != "Archive":
            if current_time - os.path.getmtime(file_path) > RETENTION_DAYS * 86400:
                print(f"Archiving file: {file}")
                shutil.move(file_path, os.path.join(archive_folder, file))

    # Delete large files
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and os.path.getsize(file_path) > LARGE_FILE_SIZE:
            print(f"Deleting large file: {file}")
            os.remove(file_path)

# Check disk usage of folders
def check_disk_usage(path):
    folder_names = ["Excel", "Music", "Image", "Docs", "Text"]

    for folder in folder_names:
        folder_path = os.path.join(path, folder)
        if os.path.exists(folder_path):
            folder_size = get_folder_size(folder_path)
            if folder_size > SIZE_LIMIT_BYTES:
                print(f"Warning: Folder '{folder}' exceeds the size limit of {SIZE_LIMIT_MB} MB.")
                handle_exceeding_folder(folder_path)

# Organize files into categorized folders
def organize_files():
    path = r"M:/Python24/File automate/Usage/"
    file_name = os.listdir(path)

    folder_names = ["Excel", "Music", "Image", "Docs", "Text"]

    # Check disk usage before organizing
    check_disk_usage(path)

    # Create folders if they don't exist
    for folder in folder_names:
        folder_path = os.path.join(path, folder)
        if not os.path.exists(folder_path):
            print(f"Creating folder: {folder_path}")
            os.makedirs(folder_path)

    # Move files into respective folders
    for file in file_name:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            if file.endswith(".ods") or file.endswith(".xlsx"):
                shutil.move(file_path, os.path.join(path, "Excel", file))
            elif file.endswith(".mp3"):
                shutil.move(file_path, os.path.join(path, "Music", file))
            elif file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                shutil.move(file_path, os.path.join(path, "Image", file))
            elif file.endswith(".docx") or file.endswith(".pdf"):
                shutil.move(file_path, os.path.join(path, "Docs", file))
            elif file.endswith(".txt"):
                shutil.move(file_path, os.path.join(path, "Text", file))

# Main function to run the organizer periodically
if __name__ == "__main__":
    try:
        while True:
            organize_files()
            print("Files organized successfully. Waiting for the next cycle...")
            time.sleep(86400)  # Wait for 24 hours
    except KeyboardInterrupt:
        print("File organizer stopped by user.")
