#!/usr/bin/env python3
"""
Downloads Folder Organizer
Organizes files in a directory into folders based on their file extensions.
"""
import os
import shutil
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define the names of the folders to create and their associated file extensions
DEFAULT_FOLDERS = {
    "3D Files": {".stl", ".obj", ".step", ".gcode", ".ipt", ".iam", ".3mf"},
    "Documents": {".doc", ".docx", ".txt", ".md", ".opml", ".tex", ".bib"},
    "Presentations": {".ppt", ".pptx", ".key", ".odp"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"},
    "Vector Graphics": {".ai", ".eps", ".svg", ".drawio", ".dxf", ".ttf"},
    "PDFs": {".pdf"},
    "Raster Graphics": {".psd", ".raw", ".cr2", ".nef", ".orf", ".sr2"},
    "Video": {
        ".avi", ".mp4", ".mov", ".wmv", ".mkv", ".flv", ".webm",
        ".mpg", ".mpeg", ".3gp",
    },
    "Audio": {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma"},
    "Code": {
        ".py", ".ipynb", ".java", ".cpp", ".c", ".h", ".cs", ".xml",
        ".json", ".yaml", ".yml", ".rb", ".pl", ".bat",
        ".cmd", ".ps1", ".dockerfile", ".fig",
    },
    "Web Files": {".html", ".css", ".js", ".php"},
    "Database": {".sqlite", ".db", ".kdbx", ".sql"},
    "Executable Files": {
        ".exe", ".msi", ".deb", ".dmg", ".appimage", ".sh", ".apk", ".xpi",
    },
    "System Files": {
        ".ini", ".cfg", ".plist", ".log", ".env", ".desktop",
        ".folder", ".flatpakref", ".dll",
    },
    "Compressed Files": {".zip", ".tar", ".gz", ".7z", ".rar", ".rpm"},
    "Disk Images": {".iso", ".img", ".vmdk"},
    "Miscellaneous": set(),
    "Old_Folders": set(),
}


def create_folders(path, folders):
    """Create the folders defined in the folders dictionary.
    
    Args:
        path: The base directory path
        folders: Dictionary of folder names and their extensions
    """
    for folder_name in folders.keys():
        folder_path = os.path.join(path, folder_name)
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                logger.info(f"Created folder: {folder_name}")
        except OSError as e:
            logger.error(f"Failed to create folder {folder_name}: {e}")


def get_folder_for_file(filename, folders):
    """Determine which folder a file should be moved to based on its extension.
    
    Args:
        filename: Name of the file
        folders: Dictionary of folder names and their extensions
        
    Returns:
        The folder name or "Miscellaneous" if no match found
    """
    filename_lower = filename.lower()
    for folder_name, extensions in folders.items():
        if folder_name in ["Miscellaneous", "Old_Folders"]:
            continue
        for ext in extensions:
            if filename_lower.endswith(ext.lower()):
                return folder_name
    return "Miscellaneous"


def move_file_safely(src_path, dest_dir, filename, dry_run=False):
    """Safely move a file, handling naming conflicts.
    
    Args:
        src_path: Source file path
        dest_dir: Destination directory
        filename: Name of the file
        dry_run: If True, only log what would be done
        
    Returns:
        True if successful, False otherwise
    """
    dest_path = os.path.join(dest_dir, filename)
    
    # Handle naming conflicts
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            new_filename = f"{base}_{counter}{ext}"
            dest_path = os.path.join(dest_dir, new_filename)
            counter += 1
        filename = os.path.basename(dest_path)
    
    if dry_run:
        logger.info(f"[DRY RUN] Would move: {src_path} -> {dest_path}")
        return True
    
    try:
        shutil.move(src_path, dest_path)
        logger.info(f"Moved: {filename} -> {os.path.basename(dest_dir)}")
        return True
    except (OSError, shutil.Error) as e:
        logger.error(f"Failed to move {filename}: {e}")
        return False


def organize_files(path, threshold_days=15, dry_run=False, folders=None):
    """Organize files in the specified directory.
    
    Args:
        path: Directory to organize
        threshold_days: Only organize files older than this many days
        dry_run: If True, only preview changes without making them
        folders: Custom folder mappings (uses DEFAULT_FOLDERS if None)
    """
    if folders is None:
        folders = DEFAULT_FOLDERS
    
    # Validate path exists
    if not os.path.exists(path):
        logger.error(f"Path does not exist: {path}")
        return
    
    if not os.path.isdir(path):
        logger.error(f"Path is not a directory: {path}")
        return
    
    # Create folders
    create_folders(path, folders)
    
    # Set the time threshold
    threshold_date = datetime.now() - timedelta(days=threshold_days)
    logger.info(f"Organizing files older than {threshold_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    files_moved = 0
    dirs_moved = 0
    errors = 0
    
    # Get list of files/directories first to avoid issues with concurrent modification
    try:
        items = list(os.scandir(path))
    except OSError as e:
        logger.error(f"Failed to scan directory {path}: {e}")
        return
    
    # Loop over all files and directories in the path
    for item in items:
        try:
            # Skip if item no longer exists (could have been moved/deleted)
            if not os.path.exists(item.path):
                continue
            
            file_modification_time = datetime.fromtimestamp(item.stat().st_mtime)
            
            # Skip files newer than the threshold
            if file_modification_time > threshold_date:
                continue
            
            # Handle files
            if item.is_file():
                folder_name = get_folder_for_file(item.name, folders)
                dest_dir = os.path.join(path, folder_name)
                
                if move_file_safely(item.path, dest_dir, item.name, dry_run):
                    files_moved += 1
                else:
                    errors += 1
            
            # Handle directories (move to Old_Folders if not a category folder)
            elif item.is_dir() and item.name not in folders:
                dest_dir = os.path.join(path, "Old_Folders")
                if move_file_safely(item.path, dest_dir, item.name, dry_run):
                    dirs_moved += 1
                else:
                    errors += 1
        
        except (OSError, PermissionError) as e:
            logger.error(f"Error processing {item.name}: {e}")
            errors += 1
    
    # Handle moving most recent item from Old_Folders to Miscellaneous
    old_folders_path = os.path.join(path, "Old_Folders")
    if os.path.exists(old_folders_path):
        try:
            items_in_old = list(os.scandir(old_folders_path))
            if items_in_old:
                # Find most recently modified item
                most_recent = max(items_in_old, key=lambda x: x.stat().st_mtime)
                misc_dir = os.path.join(path, "Miscellaneous")
                if move_file_safely(most_recent.path, misc_dir, most_recent.name, dry_run):
                    logger.info(f"Moved most recent item from Old_Folders: {most_recent.name}")
        except (ValueError, OSError) as e:
            logger.warning(f"Could not process Old_Folders: {e}")
    
    # Summary
    logger.info(f"Summary: {files_moved} files moved, {dirs_moved} directories moved, {errors} errors")
    if dry_run:
        logger.info("This was a dry run - no actual changes were made")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Organize files in a directory based on their extensions"
    )
    parser.add_argument(
        "--path",
        default=os.path.join(os.path.expanduser("~"), "Downloads"),
        help="Path to the directory to organize (default: ~/Downloads)"
    )
    parser.add_argument(
        "--threshold-days",
        type=int,
        default=15,
        help="Only organize files older than this many days (default: 15)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without actually moving files"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info(f"Starting organization of: {args.path}")
    organize_files(args.path, args.threshold_days, args.dry_run)
    logger.info("Organization complete!")


if __name__ == "__main__":
    main()

