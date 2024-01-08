# YouTube Downloader

## Overview
This is a simple YouTube downloader GUI built with Python using the Pytube library. The application allows you to download YouTube videos or playlists with ease.

## Requirements
- Python 3.x
- Pytube library

## Installation
1. Clone or download the repository.
2. Install the required dependencies using:
   ```bash
   pip install pytube
   ```

## Usage
1. Run the YouTube downloader GUI using the following command:
   ```bash
   pyinstaller --onefile --noconsole --name ytdownload --clean pytube_inference.py
   ```
   This will generate an executable file named `ytdownload.exe` in the `dist` directory.

2. Double-click on the executable to run the YouTube downloader without requiring a Python interpreter.

3. Enter the YouTube URL in the provided field.

4. Specify the output path for downloaded files.

5. Choose options like "Audio Only" and resolution.

6. Click the "Download" button to start the download process.

## Additional Options
- `--icon`: You can specify an icon file for the executable using `--icon`. Example:
  ```bash
  pyinstaller --onefile --noconsole --name ytdownload --icon=your_icon.ico pytube_inference.py
  ```

- `--specpath`: Specify the location to store the spec file. Example:
  ```bash
  pyinstaller --onefile --noconsole --name ytdownload --specpath=your_spec_directory pytube_inference.py
  ```
