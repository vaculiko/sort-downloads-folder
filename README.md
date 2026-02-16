![https://ailabels.org/#made-primarily-by-ai](https://github.com/micahchoo/Downloads-Folder-Sorter/blob/67de0678def24e5754947f59565ed96620e5144d/AI%20Labels%20-%20AI.svg)

# Introduction

This File and Folder Sorter is a Python program that organizes files in a specified directory into folders based on their file extensions. It is useful for individuals who have a cluttered downloads folder or other directories with a variety of file types. It sorts any type of files into their respective Folders based on date or use-case. Helps those who have a lot of files to manage. You can modify this folder classification according to your specific use case by adding or removing file extensions within each category to better suit your needs as a doctor, designer, or any other use-case. 


## Requirements

The Downloads Folder Organizer requires Python 3.5 or higher to be installed on your computer. No external dependencies are required.

## Installation

### Quick Start

1. Download the program code from the Github repository.
2. Extract the files to a directory of your choice.
3. Make the script executable (optional, Unix-like systems):
   ```bash
   chmod +x sort_downloads.py
   ```

### Development Setup

If you want to contribute or run tests:

```bash
pip install -r requirements-dev.txt
```

## Running Tests

To verify the installation and functionality:

```bash
python3 test_sort_downloads.py
```

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

**Remove empty folders after organizing:**
```bash
python3 sort_downloads.py --remove-empty-folders
```

**Combine options:**
```bash
python3 sort_downloads.py --path ~/Documents --threshold-days 60 --remove-empty-folders --dry-run --verbose
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

## Scheduling Automatic Runs (Windows Task Scheduler)

You can configure Windows Task Scheduler to run this script automatically every workday at 8:00 AM.

### Using the GUI

1. Open **Task Scheduler** (search for "Task Scheduler" in the Start menu).
2. Click **Create Basic Task** in the right-hand panel.
3. Enter a name (e.g., `Sort Downloads Folder`) and click **Next**.
4. Select **Weekly** and click **Next**.
5. Set the start time to **8:00:00 AM**, recur every **1** week, and check **Mon, Tue, Wed, Thu, Fri**. Click **Next**.
6. Select **Start a program** and click **Next**.
7. In **Program/script**, enter the path to your Python executable, for example:
   ```
   C:\Users\YourUser\AppData\Local\Programs\Python\PythonXXX\python.exe
   ```
   To find your Python path, run `where python` in a terminal.
8. In **Add arguments**, enter the script path and any desired flags, for example:
   ```
   C:\path\to\sort_downloads.py --remove-empty-folders
   ```
9. Click **Next**, review the summary, and click **Finish**.

### Using the Command Line (schtasks)

Open **Command Prompt** or **PowerShell** as Administrator and run:

```cmd
schtasks /create /tn "Sort Downloads Folder" /tr "C:\path\to\python.exe C:\path\to\sort_downloads.py --remove-empty-folders" /sc weekly /d MON,TUE,WED,THU,FRI /st 08:00
```

Replace the Python and script paths with your actual paths. To find your Python path, run `where python` in a terminal.

### Verifying the Scheduled Task

- Open Task Scheduler and look for your task under **Task Scheduler Library**.
- Right-click the task and select **Run** to test it immediately.
- Check the **Last Run Result** column to confirm it completed successfully.

### Removing the Scheduled Task

To delete the task via the command line:

```cmd
schtasks /delete /tn "Sort Downloads Folder" /f
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

## Features

- ✅ **Safe operation:** Dry-run mode to preview changes before making them
- ✅ **Smart organization:** Files are categorized by extension into logical folders
- ✅ **Configurable:** Command-line arguments for path, threshold, and verbosity
- ✅ **Age-based filtering:** Only organize files older than a specified threshold
- ✅ **Conflict handling:** Automatically renames files to avoid overwriting
- ✅ **Empty folder cleanup:** Optionally remove folders that contain no files
- ✅ **Comprehensive logging:** Track all operations and errors
- ✅ **Error resilient:** Gracefully handles permission errors and edge cases
- ✅ **Well-tested:** Includes unit tests for core functionality

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Structure

```
sort-downloads-folder/
├── sort_downloads.py          # Main script
├── test_sort_downloads.py     # Unit tests
├── README.md                  # This file
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
├── requirements.txt           # Python dependencies (none for main script)
├── requirements-dev.txt       # Development dependencies
├── config.example.json        # Example configuration file
└── .gitignore                # Git ignore rules
```




















if you made it all the way here, i'm assuming you are looking for what is in the [basement](https://github.com/micahchoo/Downloads-Folder-Sorter/wiki/Fever-Dream-of-the-Folder-Sorter)
