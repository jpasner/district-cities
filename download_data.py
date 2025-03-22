import os
import requests
from bs4 import BeautifulSoup

# URL of the TIGER 2023 Congressional District shapefiles
base_url = "https://www2.census.gov/geo/tiger/TIGER2023/CD/"

# Send a request to the URL and parse the HTML content
response = requests.get(base_url)
response.raise_for_status()  # Ensure we notice bad responses
soup = BeautifulSoup(response.text, "html.parser")

# Create a directory to store the downloaded files
download_dir = "data/tiger_cd_shapefiles"
os.makedirs(download_dir, exist_ok=True)

# Loop through all the anchor tags and download .zip files
for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.endswith(".zip"):
        file_url = base_url + href
        local_path = os.path.join(download_dir, href)
        print(f"Downloading {file_url} ...")
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded {href}")

print("All TIGER Congressional District shapefiles have been downloaded.")