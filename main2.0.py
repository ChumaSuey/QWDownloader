import requests
import os
import time
from bs4 import BeautifulSoup

# Website URL of Quakeworld Quake 1 maps database.
URL = "https://maps.quakeworld.nu/all/"

# Destination folder for the downloaded maps
DEST_FOLDER = "./qwmaps"

def verify_destination_folder():
    """Verify and/or create the destination folder for the maps."""
    if not os.path.exists(DEST_FOLDER):
        os.makedirs(DEST_FOLDER)
        print(f"Folder {DEST_FOLDER} created.")

def download_file(download_url, file_name):
    """Download the file from the given URL and save it to the destination folder."""
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        file_path = os.path.join(DEST_FOLDER, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"{file_name} file downloaded successfully.")
    except requests.RequestException as e:
        print(f"Failed to download {file_name}: {e}")

def process_rows(rows):
    """Process the rows to find and download .bsp files."""
    for row in rows:
        elements = row.find_all("td")
        if len(elements) == 3:
            file_name = elements[0].text.strip()
            if file_name.endswith(".bsp"):
                download_link = elements[0].find("a")["href"]
                download_url = URL + download_link
                download_file(download_url, file_name)
                time.sleep(5)  # Pause between downloads

def get_website_content():
    """Get the content from the website."""
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to access the website: {e}")
        return None

def main():
    """Main function to orchestrate the downloading of maps."""
    try:
        verify_destination_folder()
        content = get_website_content()
        if content:
            soup = BeautifulSoup(content, "html.parser")
            rows = soup.find_all("tr")
            process_rows(rows)
    except KeyboardInterrupt:
        print("Download process stopped by user.")

if __name__ == "__main__":
    main()