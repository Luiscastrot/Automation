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

print(output_file)  # print only filename for GitHub Actions
