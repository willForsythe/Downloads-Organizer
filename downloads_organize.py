from fileinput import filename
from os import scandir, rename, makedirs, getlogin
from os.path import splitext, exists
from shutil import move
from time import sleep
from pathlib import Path
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Listing source and destination directories for folder items
# Grabbing current user signed into system
current_user = getlogin()

source_dir_downloads = f"/Users/{current_user}/Downloads"
source_dir_documents = f"/Users/{current_user}/Documents"

destination_dir_documents = Path(f"/Users/{current_user}/Documents/Office Documents")
destination_dir_spreadsheets = Path(f"/Users/{current_user}/Documents/Spreadsheets")
destination_dir_email = Path(f"/Users/{current_user}/Documents/Downloaded Emails")
destination_dir_screenshots = Path(f"/Users/{current_user}/Documents/Screenshots")
desintation_dir_pdf = Path(f"/Users/{current_user}/Documents/PDFs")
destination_dir_installers = Path(f"/Users/{current_user}/Documents/Installers")

# Listing Extension Variables 
extensions_documents = [".doc", ".ppt", ".docx", ".pptx"]
extensions_spreadsheets = [".xlsx", ".xlsm", ".xlsb", ".xml", ".xls", ".csv"]
extensions_emails = [".eml"]
extensions_screenshots = [".jpg", ".jpeg", ".gif", ".png", ".heic"]
extensions_pdfs = [".pdf"]
extensions_installers = [".dmg", ".iso"]

# Checking if directory exists and creating if not
if destination_dir_documents.is_dir():
    print("Office Documents Directory Exists")
else:
    makedirs(destination_dir_documents)
    print("Office Documents Created")

if destination_dir_spreadsheets.is_dir():
    print("Screenshots Directory Exists")
else:
    makedirs(destination_dir_spreadsheets)
    print("Screenshots Directory Created")

if destination_dir_email.is_dir():
    print("Email Directory Exists")
else:
    makedirs(destination_dir_email)
    print("Email Directory Created")

if destination_dir_screenshots.is_dir():
    print("Screenshots Directory Exists")
else:
    makedirs(destination_dir_screenshots)
    print("Screenshots Directory Created")

if desintation_dir_pdf.is_dir():
    print("PDF Directory Exists")
else:
    makedirs(desintation_dir_pdf)
    print("PDF Directory Created")

if destination_dir_installers.is_dir():
    print("Installer Directory Exists")
else:
    makedirs(destination_dir_installers)
    print("Installer Directory Created")


# Function for creating unique files in the case of duplicate names
def unique_file(path):
    filename, extension = splitext(path)
    counter = 1

    while exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1
    return path

# Function for moving files to destination directories
def move_file(destination, entry, name):
    if exists(f"{destination}/{name}"):
        unique_name = unique_file(name)
        rename(entry, unique_name)
    move(entry, destination)

# Class for Scanning and Moving Download Folder Items
class DownloadsHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir_downloads) as entries:
            for entry in entries:
                name = entry.name
                self.files_documents(entry, name)
                self.files_spreadsheets(entry, name)
                self.files_emails(entry, name)
                self.files_screenshots(entry, name)
                self.files_pdfs(entry, name)
                self.files_installers(entry, name)
    
    def files_documents(self, entry, name):
        for extensions_document in extensions_documents:
            if name.endswith(extensions_document) or name.endswith(extensions_document.upper()):
                move_file(destination_dir_documents, entry, name)
                logging.info(f"Moved Document: {name}")
    
    def files_spreadsheets(self, entry, name):
        for extensions_spreadsheet in extensions_spreadsheets:
            if name.endswith(extensions_spreadsheet) or name.endswith(extensions_spreadsheet.upper()):
                move_file(destination_dir_spreadsheets, entry, name)
                logging.info(f"Moved Spreadsheet: {name}")

    def files_emails(self, entry, name):
        for extensions_email in extensions_emails:
            if name.endswith(extensions_email) or name.endswith(extensions_email.upper()):
                move_file(destination_dir_email, entry, name)
                logging.info(f"Moved Email: {name}")
    
    def files_screenshots(self, entry, name):
        for extensions_screenshot in extensions_screenshots:
            if name.endswith(extensions_screenshot) or name.endswith(extensions_screenshot.upper()):
                move_file(destination_dir_screenshots, entry, name)
                logging.info(f"Moved Screenshot: {name}")

    def files_pdfs(self, entry, name):
        for extensions_pdf in extensions_pdfs:
            if name.endswith(extensions_pdf) or name.endswith(extensions_pdf.upper()):
                move_file(desintation_dir_pdf, entry, name)
                logging.info(f"Moved PDF: {name}")
    
    def files_installers(self, entry, name):
        for extensions_installer in extensions_installers:
            if name.endswith(extensions_installer) or name.endswith(extensions_installer.upper()):
                move_file(destination_dir_installers, entry, name)
                logging.info(f"Moved Installer: {name}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir_downloads
    event_handler = DownloadsHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    finally:
        observer.stop()
        observer.join()