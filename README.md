![https://ailabels.org/#made-primarily-by-ai](https://github.com/micahchoo/Downloads-Folder-Sorter/blob/67de0678def24e5754947f59565ed96620e5144d/AI%20Labels%20-%20AI.svg)

# Introduction

This File and Folder Sorter is a Python program that organizes files in a specified directory into folders based on their file extensions. It is useful for individuals who have a cluttered downloads folder or other directories with a variety of file types. It sorts any type of files into their respective Folders based on date or use-case. Helps those who have a lot of files to manage. You can modify this folder classification according to your specific use case by adding or removing file extensions within each category to better suit your needs as a doctor, designer, or any other use-case. 


## Requirements

The Downloads Folder Organizer requires Python 3.5 or higher to be installed on your computer.

## Installation

   - Download the program code from the Github repository.
   - Extract the files to a directory of your choice.

## Usage

### Basic Usage

Run the script with default settings (organizes ~/Downloads, files older than 15 days):

```bash
python3 sort_downloads.py
```

### Advanced Usage

**Preview changes without making them (dry-run mode):**
```bash
python3 sort_downloads.py --dry-run
```

**Organize a custom directory:**
```bash
python3 sort_downloads.py --path /path/to/your/directory
```

**Change the age threshold (e.g., only files older than 30 days):**
```bash
python3 sort_downloads.py --threshold-days 30
```

**Enable verbose logging:**
```bash
python3 sort_downloads.py --verbose
```

**Combine options:**
```bash
python3 sort_downloads.py --path ~/Documents --threshold-days 60 --dry-run --verbose
```

### Important Notes

- **Always use dry-run mode first** to preview changes before actually moving files
- The script only processes files older than the threshold (default: 15 days)
- Files are automatically renamed if naming conflicts occur
- All operations are logged for easy troubleshooting 

# Customization

1. **File Categories:** To customize file categories, edit the `DEFAULT_FOLDERS` dictionary in `sort_downloads.py` to add or remove folders and their associated file extensions.

2. **Time Threshold:** Use the `--threshold-days` command-line argument to change how old files must be before organizing:
```bash
python3 sort_downloads.py --threshold-days 30
```

3. **Custom Directory:** Use the `--path` argument to organize a different directory:
```bash
python3 sort_downloads.py --path /path/to/your/folder
```


# Troubleshooting

If you encounter any issues with the program, please check the following:

  - Make sure that you have Python 3.5 or higher installed on your computer.
  - Make sure you have the correct permissions to read/write in the target directory.
  - Use the `--dry-run` flag first to preview what will happen.
  - Check the log output for specific error messages.
  - Path directory may look different on different OSs - the script handles this automatically.
  - Make sure the directory you're organizing exists and is accessible.

### Common Issues

**Permission Errors:** Make sure you have read/write permissions for the directory you're organizing.

**No Files Moving:** Check that files are older than the threshold (default: 15 days). Use `--threshold-days 0` to process all files.

**Files Going to Wrong Folders:** The script uses the first matching category. You can customize the `DEFAULT_FOLDERS` dictionary in the script.




















if you made it all the way here, i'm assuming you are looking for what is in the [basement](https://github.com/micahchoo/Downloads-Folder-Sorter/wiki/Fever-Dream-of-the-Folder-Sorter)
