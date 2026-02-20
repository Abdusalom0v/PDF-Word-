Installation (For Users)
Option 1 – Using Installer

Download the latest version from the Releases section.

Run the installer (.exe).

Follow the setup wizard.

Launch from Desktop or Start Menu.

Option 2 – Run from Source
Requirements

Python 3.9+

pip

Install dependencies
pip install -r requirements.txt
Run the application
python main.py
Building the Executable

To create a standalone Windows executable:

pip install pyinstaller
pyinstaller --onefile --windowed main.py

The executable will be generated inside:

dist/main.exe
