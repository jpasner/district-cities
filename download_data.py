import os
import requests
import zipfile
from bs4 import BeautifulSoup

# Step1: Download the 2023 National Gazetteer Places File and unzip it to the `data` directory
gazetteer_url = "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2023_Gazetteer/2023_Gaz_place_national.zip"
gazetteer_zip_path = "data/2023_Gaz_place_national.zip"
os.makedirs("data", exist_ok=True)

print(f"Downloading National Gazetteer Places File from {gazetteer_url} ...")
with requests.get(gazetteer_url, stream=True) as r:
    r.raise_for_status()
    with open(gazetteer_zip_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
print("Downloaded National Gazetteer Places File.")

print("Unzipping the National Gazetteer Places File ...")
with zipfile.ZipFile(gazetteer_zip_path, "r") as zip_ref:
    zip_ref.extractall("data")
# Unzipped National Gazetteer Places File.
print("Unzipped National Gazetteer Places File.")

# Step 2: Download the 2023 Census file of Incorporated Places and save it to the data directory
incorporated_places_url = "https://www2.census.gov/programs-surveys/popest/tables/2020-2023/cities/totals/SUB-IP-EST2023-POP.xlsx"
incorporated_places_path = "data/SUB-IP-EST2023-POP.xlsx"
print(f"Downloading 2023 Census Incorporated Places file from {incorporated_places_url} ...")
with requests.get(incorporated_places_url, stream=True) as r:
    r.raise_for_status()
    with open(incorporated_places_path, "wb") as f:
         for chunk in r.iter_content(chunk_size=8192):
             f.write(chunk)
print("Downloaded 2023 Census Incorporated Places file.")

# Step 3:Download TIGER 2023 Congressional District shapefiles
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