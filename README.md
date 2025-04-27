# iBackups
**A Python, Tkinter-based tool to make backups of your device** \
This is a frontend for the idevicebackup2 tool, part of the libimobiledevice library.

## Dependencies
- **Linux**: usbmuxd, libimobiledevice, Python 3

## Installation
### Linux
1. Clone the repository and navigate into it:

```bash
git clone https://github.com/naturelessGit/iBackups.git
cd iBackups
```

2. Install the dependencies:

```bash
sudo apt install usbmuxd libimoibledevice python3 python3-tk
```

*(Note: Package manager can vary depending on system)*

3. Its highly reccomended to use a virtual enviroment:

```bash
python3 -m venv .env
source .env/bin/activate
```

4. Run the app:

```bash
python3 main.py
```

## Usage
1. Connect your phone to your PC using your charging cable.
2. Install and run iBackups.
3. Select your backup directory and click "Backup!".
4. Wait until your device has been backed up. If you run into an issue, paste the terminal output into our GitHub issues page.

## Will there be a macOS/Windows version eventually?
Probably! A macOS/Windows export and distribution will be released soon.

## Authors
This project is made with love by **Natureless**.
