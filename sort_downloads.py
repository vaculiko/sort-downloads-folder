import os
import shutil
from datetime import datetime, timedelta

# Define the path to the directory to organize
path = os.path.join(os.path.expanduser("~"), "Downloads")

# Define the names of the folders to create and their associated file extensions
folders = {
    "3D Files": {".stl", ".obj", ".step", ".gcode", ".ipt", ".iam", ".3mf"},
    "Documents": {".doc", ".docx", ".txt", ".md", ".opml", ".tex", ".bib"},
    "Presentations": {".ppt", ".pptx", ".key", ".odp"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"},
    "Vector Graphics": {".ai", ".eps", ".svg", ".drawio", ".dxf", ".ttf"},
    "PDFs": {".pdf"},
    "Raster Graphics": {".psd", ".raw", ".cr2", ".nef", ".orf", ".sr2"},
    "Video": {
        ".avi",
        ".mp4",
        ".mov",
        ".wmv",
        ".mkv",
        ".flv",
        ".webm",
        ".mpg",
        ".mpeg",
        ".3gp",
    },
    "Audio": {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma"},
    "Code": {
        ".py",
        ".ipynb",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".cs",
        ".xml",
        ".json",
        ".yaml",
        ".yml",
        ".sql",
        ".rb",
        ".pl",
        ".sh",
        ".bat",
        ".cmd",
        ".ps1",
        ".dockerfile",
        ".fig",
        ".js",
    },
    "Web Files": {".html", ".css", ".js", ".php"},
    "Database": {".sqlite", ".db", ".sql", ".kdbx"},
    "Executable Files": {
        ".exe",
        ".msi",
        ".deb",
        ".dmg",
        ".appimage",
        ".sh",
        ".apk",
        ".xpi",
    },
    "System Files": {
        ".ini",
        ".cfg",
        ".plist",
        ".log",
        ".env",
        ".desktop",
        ".folder",
        ".flatpakref",
        ".dll",
    },
    "Compressed Files": {".zip", ".tar", ".gz", ".7z", ".rar", ".deb", ".rpm"},
    "Disk Images": {".iso", ".img", ".vmdk"},
    "Other": set(),
    "Old_Folders": set(),
    "Meta": {" "},
}

# Create the folders defined in the `folders` dictionary
for folder_name, extensions in folders.items():
    folder_path = os.path.join(path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Set the time threshold to 15 days ago
threshold_date = datetime.now() - timedelta(days=15)

# Loop over all files and directories in the path
for file in os.scandir(path):
    file_path = file.path
    file_modification_time = datetime.fromtimestamp(file.stat().st_mtime)
    
    # Skip files newer than the threshold
    if file_modification_time > threshold_date:
        continue

    # Check if the file is older than the threshold
    if file.is_file():
        # Move the file to the appropriate folder
        folder_name = None
        for name, extensions in folders.items():
            if file.name.lower().endswith(tuple(ext.lower() for ext in extensions)):
                folder_name = name
                break
        if folder_name is None:
            folder_name = "Miscellaneous"
        shutil.move(file_path, os.path.join(path, folder_name, file.name))

    # Check if the file is a directory and not in the 'folders' dictionary
    elif file.is_dir() and file.name not in folders:
        # Move the directory to the Old_Folders folder
        shutil.move(file_path, os.path.join(path, "Old_Folders", file.name))

# Move the most recently modified file in the Old_Folders directory to the Miscellaneous directory
most_recent_file = max(
    os.listdir(os.path.join(path, "Old_Folders")), key=os.path.getmtime
)
shutil.move(
    os.path.join(path, "Old_Folders", most_recent_file),
    os.path.join(path, "Miscellaneous", most_recent_file),
)

