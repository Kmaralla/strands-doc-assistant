# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **CRITICAL**: Fixed `--docs-path` parameter not being passed to DocumentSearchTool
  - The application was always using the default `./docs` directory regardless of the `--docs-path` parameter
  - Root cause: `create_agent()` function wasn't accepting or passing the `docs_path` parameter
  - Solution: Modified `create_agent()` to accept `docs_path` parameter and pass it to `DocumentSearchTool()`

### Added
- Comprehensive logging throughout the application for better debugging
- `--dry-run` mode for testing configuration without AWS credentials
- Validation script (`test_setup.py`) for verifying installation
- Enhanced error handling and user feedback
- Detailed documentation with troubleshooting section

### Changed
- Updated README.md with comprehensive setup and testing instructions
- Improved CLI help text and parameter documentation
- Enhanced DocumentSearchTool with better logging and error reporting
- Fixed logical bug in document search loop (early return issue)

### Security
- Updated .gitignore to exclude AWS credentials and sensitive files

## [Previous Versions]

This changelog was started with the docs-path fix. Previous changes were not tracked in this format. 