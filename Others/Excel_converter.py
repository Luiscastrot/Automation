import os
import requests
import io
import pandas as pd

dropbox_url = os.environ.get("INVOICING_BOOK_URL")
if not dropbox_url:
    raise Exception("INVOICING_BOOK_URL not set")

# Extract filename from URL path and replace extension
filename = dropbox_url.split('/')[-1].split('?')[0]  # get last path part, remove query
output_file = filename.replace('.xlsb', '.xlsx')

# Download file
r = requests.get(dropbox_url)
r.raise_for_status()  # raise error if download failed

# Read XLSB and convert to XLSX
xlsb_data = io.BytesIO(r.content)
xlsb = pd.ExcelFile(xlsb_data, engine='pyxlsb')
with pd.ExcelWriter(output_file) as writer:
    for sheet in xlsb.sheet_names:
        df = xlsb.parse(sheet_name=sheet, header=None)
        df.to_excel(writer, sheet_name=sheet, index=False, header=False)

# Write the output filename to the GitHub Actions environment file
env_file_path = os.getenv('GITHUB_ENV')
if env_file_path:
    with open(env_file_path, "a") as env_file:
        env_file.write(f"ENV_CUSTOM_DATE_FILE={output_file}\n")
else:
    # Fallback: print filename if GITHUB_ENV is not set (e.g., local run)
    print(output_file)
