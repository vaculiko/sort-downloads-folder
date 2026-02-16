# Contributing to Downloads Folder Organizer

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/sort-downloads-folder.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

This project uses only Python standard library modules, so no external dependencies are required for the main script.

For development and testing:

```bash
pip install -r requirements-dev.txt
```

## Running Tests

Run the test suite:

```bash
python3 test_sort_downloads.py
```

Run with verbose output:

```bash
python3 test_sort_downloads.py -v
```

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions
- Keep functions focused and modular
- Add comments for complex logic

You can use black for formatting (optional):

```bash
black sort_downloads.py test_sort_downloads.py
```

## Testing Your Changes

1. Always test your changes manually before submitting
2. Use `--dry-run` mode to verify behavior
3. Add tests for new features
4. Ensure existing tests still pass
5. Test with various file types and edge cases

## Submitting Changes

1. Make sure all tests pass
2. Update documentation if needed
3. Commit your changes with clear, descriptive messages
4. Push to your fork
5. Create a Pull Request

## Pull Request Guidelines

- Describe what your PR does
- Reference any related issues
- Include examples if adding features
- Update README.md if adding user-facing changes
- Ensure tests pass

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Any error messages or logs

## Feature Requests

Feature requests are welcome! Please:

- Explain the use case
- Describe the desired behavior
- Discuss potential implementation approaches

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing! 🎉
