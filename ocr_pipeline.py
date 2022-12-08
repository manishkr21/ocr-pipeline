# basic lib require to implement the funtions
import os
import sys
from tracemalloc import start
from tqdm import tqdm
import re                       
import json
from pathlib import Path
import urllib
import pandas as pd


# li to convert pdf to images
import pytesseract
from pdf2image import *


# lib to extract pdfs
import concurrent.futures    # to make it parrallel execution
import requests              # to request to server
import base64                # to convert the encoding   


# lib to generate the data with the help of pytesseract
import time
from PIL import Image
import pytesseract
from langdetect import detect_langs
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'




# this function dwonmload the pdf files if exist   -->   regno is with '/'
# def download_pdf(regno):
#    base_url = "https://pgportal.gov.in/services/api/GetDocument/GetDocument?"
#    params = { "token": "b72368f3d242f5f6dca0cea1638a931fdba37651f63a9b7a9f3a9858669bf51a"}
#    #"https://pgportal.gov.in/services/api/GetDocument/GetDocument?key=MODEF&token=b72368f3d242f5f6dca0cea1638a931fdba37651f63a9b7a9f3a9858669bf51a&regno="+line
#    params["regno"] = regno
#    print(regno)
#    params["key"] = regno[0:5]
#    download_url = base_url + urllib.parse.urlencode(params) 
#    response = requests.get(download_url, allow_redirects=True )
#    temp = response.json()
#    if "Document" in temp:
#        doc = base64.b64decode(temp["Document"])
#        fname = regno.replace("/", "-") + ".pdf"
#        (BASE_DIR1 / fname).write_bytes(doc)
#        return "yes"
#    else:      
#        return regno


# if pdf exist then it direct to download_pdf otherwise store the info into NO_PDF_FOUND.TXT
# def fetch_pdf(filename):
#     with concurrent.futures.ThreadPoolExecutor() as e:
#         f=open('NO_PDF_FOUND.TXT','a')
        
#         with open(filename) as pmopg:
#             f2r = {e.submit(download_pdf, reg.strip()): reg.strip() for reg in pmopg}
            
#             for future in concurrent.futures.as_completed(f2r):
#                 regno = f2r[future]
#                 print(regno)
#                 try:
#                     data = future.result()
#                 except Exception as exc:
#                     f.write(regno + '\n')
#                     f.flush()
#                 else:
#                     if data is not None:
#                         f.write(regno + '\n')
#                         f.flush()
#         f.close()


# fetch the image from the pdf
def pdf_to_image(dir):
    for pdf in tqdm(os.listdir(dir)):
        pdf_name=pdf.split('.')
        print(pdf_name[0], end =' ')
        image_path='./'+str(BASE_DIR2)+'/'+pdf_name[0]
        image_num=1
        # print(pdf)
        # try:
        if os.path.getsize('./'+str(BASE_DIR1)+'/'+pdf)<1900000:
            pages=convert_from_path('./'+str(BASE_DIR1)+'/'+pdf,300)
            print(len(pages))
            os.mkdir(image_path)
            for page in pages:
                image_name='page_'+str(image_num)+'.jpg'
                page.save(image_path+'/'+image_name,'JPEG')
                image_num+=1
        # except:
            # continue
    

# using tesseract extract the text data from the given path 
def image_to_data(dir):
    
    for folder in tqdm(os.listdir(dir)):
        # try:
           
        images_path='./'+str(BASE_DIR2)+'/'+folder
        print(images_path)
        images=os.listdir(images_path)
        text_file=open('./'+str(BASE_DIR3)+'/'+folder+'.txt','w', encoding='utf-16')
        
        # if not os.path.exists('./'+str(BASE_DIR2)+'/'+folder+'.jpg'):
        #     continue
        
        for num in range(1,len(images)+1):
            
            image_path=images_path+'/page_'+str(num)+'.jpg'
            print(image_path)
            text=pytesseract.image_to_string(Image.open(image_path), lang='eng')

            text=text.replace('-\n','')
            text_file.write(text)
        text_file.close()
        # except:
            # print("An Exception is occured")


#  funtion to preprocess the data
import re
def pre_process(text):
    
    # lowercase
    text=text.lower()
    
    #remove tags
    text=re.sub("</?.*?>"," <> ",text)
    
    # remove special characters 
    text=re.sub("(\\W)+"," ",text)
    
    return text


# stored pdf data into mysql database
# def save_text_into_database(dir):
#     list_of_data = []
#     for data in os.listdir(dir):
#         docname = data.split('.')
#         reg_no = docname[0].replace('-',"/")
        
#         filename = open("./DATA_FILES/"+data,'r', encoding='utf-16')
#         list_of_data.append([str(reg_no),str(filename.readlines())])

#     # Create the pandas DataFrame
#     df = pd.DataFrame(list_of_data, columns=['regno', 'pdf_data'])
#     df['pdf_data'] = df['pdf_data'].apply(lambda x:pre_process(x))
    
#     list_data = df.to_dict('records')

#     import sqlalchemy
#     engine = sqlalchemy.create_engine('mysql://cpgrams:rajnath@localhost/cpgrams')

#     # create the test environment
#     with engine.begin() as conn:
#         conn.exec_driver_sql("DROP TABLE IF EXISTS table2")
#         conn.exec_driver_sql(
#             """
#             CREATE TABLE table2 (
#             regno varchar(50) primary key,
#             pdf_data longtext        
#             )
#             """
#         )

#     df_data = pd.DataFrame(list_data)

#     # run the test
#     with engine.begin() as conn:

#         sql = """
#             INSERT INTO table2 (regno, pdf_data) VALUES 
#             (:regno,:pdf_data)
#             """
#         params = df_data.to_dict("records")
#         print(len(params))
#         conn.execute(sqlalchemy.text(sql), params)


# location where pdf file will store
BASE_DIR1 = Path("mypdfs")
BASE_DIR1.mkdir(exist_ok=True)

# # location where image file will store
BASE_DIR2 = Path("IMAGE_FILES")
BASE_DIR2.mkdir(exist_ok=True)

# # location where text data will store
BASE_DIR3 = Path("DATA_FILES")
BASE_DIR3.mkdir(exist_ok=True)

# start_time=time.time()
# # fetch_pdf("REGISTRATION_NOS.TXT")
# print("\n****************DOWNLOADING THE PDF DATA****************\n")
# fetch_pdf("rough.txt")

# print("\n****************CONVERT THE DOCUMENT INTO IMAGES****************\n")
pdf_to_image(BASE_DIR1)   # call fn to generate the pdfs

# print("\n****************APPLY TESSERACT TO CONVERT THE IMAGE INTO TEXTFILE****************\n")
image_to_data(BASE_DIR2)

# print("\n****************SAVE THE TEXT DATA INTO DATABASE****************\n")
# save_text_into_database(BASE_DIR3)

# print("\n****************TIME TAKEN****************\n")
# end_time=time.time()
# print(end_time - start_time)


