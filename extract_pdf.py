import concurrent.futures
import requests
import base64
import re
import json
from pathlib import Path
import urllib

BASE_DIR = Path("PDF_PMOPG_FILES")
BASE_DIR.mkdir(exist_ok=True)
        
def download_pdf(regno):
   base_url = "https://pgportal.gov.in/services/api/GetDocument/GetDocument?"
   params = { "token": "b72368f3d242f5f6dca0cea1638a931fdba37651f63a9b7a9f3a9858669bf51a"}
   #"https://pgportal.gov.in/services/api/GetDocument/GetDocument?key=MODEF&token=b72368f3d242f5f6dca0cea1638a931fdba37651f63a9b7a9f3a9858669bf51a&regno="+line
   params["regno"] = regno
   params["key"] = regno[0:5]
   download_url = base_url + urllib.parse.urlencode(params) 
   response = requests.get(download_url, allow_redirects=True )
   temp = response.json()
   print(temp)
   if "Document" in temp:
       doc = base64.b64decode(temp["Document"])
       fname = regno.replace("/", "-") + ".pdf"
       (BASE_DIR / fname).write_bytes(doc)
   else:
       #print("ehllo")
       return regno
       #f.write(line +'\n')
       #f.flush()

with concurrent.futures.ThreadPoolExecutor() as e:
    f=open('have_pdfs.txt','a')
    with open("file_regno.txt") as pmopg:
        f2r = {e.submit(download_pdf, reg.strip()): reg.strip() for reg in pmopg}
        for future in concurrent.futures.as_completed(f2r):
            regno = f2r[future]
            try:
                data = future.result()
            except Exception as exc:
                f.write(regno + '\n')
                f.flush()
            else:
                if data is not None:
                    f.write(regno + '\n')
                    f.flush()
    f.close()
