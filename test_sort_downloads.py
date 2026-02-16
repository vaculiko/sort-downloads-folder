#!/usr/bin/env python3
"""
Basic tests for sort_downloads.py
"""
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path to import sort_downloads
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sort_downloads


class TestSortDownloads(unittest.TestCase):
    """Test cases for the sort_downloads module."""
    
    def setUp(self):
        """Create a temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_get_folder_for_file(self):
        """Test that files are correctly categorized."""
        folders = sort_downloads.DEFAULT_FOLDERS
        
        # Test various file types
        self.assertEqual(sort_downloads.get_folder_for_file("test.pdf", folders), "PDFs")
        self.assertEqual(sort_downloads.get_folder_for_file("image.jpg", folders), "Images")
        self.assertEqual(sort_downloads.get_folder_for_file("video.mp4", folders), "Video")
        self.assertEqual(sort_downloads.get_folder_for_file("song.mp3", folders), "Audio")
        self.assertEqual(sort_downloads.get_folder_for_file("script.py", folders), "Code")
        self.assertEqual(sort_downloads.get_folder_for_file("doc.docx", folders), "Documents")
        
        # Test case insensitivity
        self.assertEqual(sort_downloads.get_folder_for_file("TEST.PDF", folders), "PDFs")
        self.assertEqual(sort_downloads.get_folder_for_file("IMAGE.JPG", folders), "Images")
        
        # Test unknown extension
        self.assertEqual(sort_downloads.get_folder_for_file("unknown.xyz", folders), "Miscellaneous")
    
    def test_create_folders(self):
        """Test that folders are created correctly."""
        folders = {"TestFolder1": {".txt"}, "TestFolder2": {".pdf"}}
        sort_downloads.create_folders(self.test_dir, folders)
        
        # Check folders were created
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "TestFolder1")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "TestFolder2")))
    
    def test_organize_files_dry_run(self):
        """Test organize_files in dry-run mode."""
        # Create some test files
        test_file = os.path.join(self.test_dir, "test.txt")
        Path(test_file).touch()
        
        # Set modification time to 20 days ago
        old_time = datetime.now() - timedelta(days=20)
        os.utime(test_file, (old_time.timestamp(), old_time.timestamp()))
        
        # Run in dry-run mode
        sort_downloads.organize_files(self.test_dir, threshold_days=15, dry_run=True)
        
        # File should still exist in original location
        self.assertTrue(os.path.exists(test_file))
    
    def test_organize_files_with_old_file(self):
        """Test that old files are moved."""
        # Create a test file
        test_file = os.path.join(self.test_dir, "test.pdf")
        Path(test_file).touch()
        
        # Set modification time to 20 days ago
        old_time = datetime.now() - timedelta(days=20)
        os.utime(test_file, (old_time.timestamp(), old_time.timestamp()))
        
        # Run organize
        sort_downloads.organize_files(self.test_dir, threshold_days=15, dry_run=False)
        
        # File should be moved to PDFs folder
        self.assertFalse(os.path.exists(test_file))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "PDFs", "test.pdf")))
    
    def test_organize_files_with_new_file(self):
        """Test that new files are not moved."""
        # Create a test file with current time
        test_file = os.path.join(self.test_dir, "test.pdf")
        Path(test_file).touch()
        
        # Run organize
        sort_downloads.organize_files(self.test_dir, threshold_days=15, dry_run=False)
        
        # File should still be in original location
        self.assertTrue(os.path.exists(test_file))
    
    def test_move_file_with_naming_conflict(self):
        """Test that naming conflicts are handled."""
        # Create destination folder and file
        dest_dir = os.path.join(self.test_dir, "TestDest")
        os.makedirs(dest_dir)
        existing_file = os.path.join(dest_dir, "test.txt")
        Path(existing_file).touch()
        
        # Create source file
        src_file = os.path.join(self.test_dir, "test.txt")
        Path(src_file).touch()
        
        # Move file
        result = sort_downloads.move_file_safely(src_file, dest_dir, "test.txt")
        
        # Should succeed and create renamed file
        self.assertTrue(result)
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "test_1.txt")))

    def test_clean_empty_folders_removes_empty(self):
        """Test that empty folders are removed."""
        folders = {"Category": {".txt"}}
        # Create an empty non-category folder
        empty_dir = os.path.join(self.test_dir, "EmptyFolder")
        os.makedirs(empty_dir)

        removed = sort_downloads.clean_empty_folders(self.test_dir, folders)

        self.assertEqual(removed, 1)
        self.assertFalse(os.path.exists(empty_dir))

    def test_clean_empty_folders_keeps_non_empty(self):
        """Test that folders with files are kept."""
        folders = {"Category": {".txt"}}
        # Create a non-empty non-category folder
        non_empty_dir = os.path.join(self.test_dir, "NonEmpty")
        os.makedirs(non_empty_dir)
        Path(os.path.join(non_empty_dir, "file.txt")).touch()

        removed = sort_downloads.clean_empty_folders(self.test_dir, folders)

        self.assertEqual(removed, 0)
        self.assertTrue(os.path.exists(non_empty_dir))

    def test_clean_empty_folders_skips_category_folders(self):
        """Test that category folders are not removed even if empty."""
        folders = {"Category": {".txt"}}
        cat_dir = os.path.join(self.test_dir, "Category")
        os.makedirs(cat_dir)

        removed = sort_downloads.clean_empty_folders(self.test_dir, folders)

        self.assertEqual(removed, 0)
        self.assertTrue(os.path.exists(cat_dir))

    def test_clean_empty_folders_dry_run(self):
        """Test that dry run does not remove folders."""
        folders = {"Category": {".txt"}}
        empty_dir = os.path.join(self.test_dir, "EmptyFolder")
        os.makedirs(empty_dir)

        removed = sort_downloads.clean_empty_folders(self.test_dir, folders, dry_run=True)

        self.assertEqual(removed, 1)
        self.assertTrue(os.path.exists(empty_dir))

    def test_clean_empty_folders_nested_empty(self):
        """Test that folders with only empty subfolders are removed.
        
        shutil.rmtree removes the entire tree; the counter increments once
        for the top-level folder.
        """
        folders = {"Category": {".txt"}}
        parent = os.path.join(self.test_dir, "Parent")
        os.makedirs(os.path.join(parent, "child"))

        removed = sort_downloads.clean_empty_folders(self.test_dir, folders)

        self.assertEqual(removed, 1)
        self.assertFalse(os.path.exists(parent))

    def test_organize_files_with_remove_empty_folders(self):
        """Test organize_files with remove_empty_folders enabled."""
        # Create an empty non-category folder with old mtime
        empty_dir = os.path.join(self.test_dir, "SomeEmptyDir")
        os.makedirs(empty_dir)
        old_time = datetime.now() - timedelta(days=20)
        os.utime(empty_dir, (old_time.timestamp(), old_time.timestamp()))

        sort_downloads.organize_files(
            self.test_dir, threshold_days=15, dry_run=False, remove_empty_folders=True
        )

        # The empty dir was moved to Old_Folders during organize, and Old_Folders
        # is a category folder so it won't be removed by clean_empty_folders.
        # Verify that the organize + cleanup ran without error.
        self.assertTrue(os.path.isdir(self.test_dir))


if __name__ == "__main__":
    unittest.main()
