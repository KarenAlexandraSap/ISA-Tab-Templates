import os
import requests
import zipfile

# Replace with your API token
API_TOKEN = os.getenv("METABOLIGHTS_API_TOKEN")
if not API_TOKEN:
    raise ValueError("Please set the METABOLIGHTS_API_TOKEN environment variable.")
STUDY_ID = "MTBLS2159"
BASE_URL = f"https://www.ebi.ac.uk/metabolights/ws/studies/{STUDY_ID}/download?file=metadata"

# Directory to save the downloaded files
output_dir = f"~/CFM_ISA/ISA-Tab-Templates/{STUDY_ID}"
output_dir = os.path.expanduser(output_dir)
os.makedirs(output_dir, exist_ok=True)

# Define headers
headers = {
    "user_token": API_TOKEN,
}

# Send GET request to download the study archive
response = requests.get(BASE_URL, headers=headers, stream=True)
#requests.get(BASE_URL, headers=headers, stream=True)

if response.status_code == 200:
    zip_file_path = os.path.join(output_dir, f"{STUDY_ID}.zip")
    with open(zip_file_path, "wb") as zip_file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                zip_file.write(chunk)
    print(f"Downloaded study archive to {zip_file_path}")

    # Extract the zip file
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
        print(f"Extracted files to {output_dir}")
        os.remove(zip_file_path)  # Optional: Remove the zip file after extraction
    except zipfile.BadZipFile:
        print("Error: Downloaded file is not a valid zip archive.")
else:
    print(f"Failed to download study archive. HTTP Status: {response.status_code}")
    print("Response:", response.text)

