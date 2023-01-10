import pandas as pd
import numpy as np
import sqlalchemy
import pymysql
import sys
import os
import shutil

#Database Connection
engine = sqlalchemy.create_engine("mysql+pymysql://cpgrams:rajnath@localhost/cpgrams")
connection = engine.connect()

#Query
count_query="select count(*) as count from pdfdata"
find_query="select count(*) as count from pdfdata where regno ='{0}'"

# find existing registration numbers
curr_length=int(pd.read_sql(count_query,con=connection)['count'])
print("Number of records in pdf_data = ", curr_length)


####################################################################################################>


# basic lib require to implement the funtions
from tracemalloc import start
from tqdm import tqdm
from pathlib import Path
import pandas as pd


# lib to convert pdf to images
import pytesseract
from pdf2image import *


# lib to generate the data with the help of pytesseract
import time
from PIL import Image
from langdetect import detect_langs
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# location where pdf file will store
BASE_DIR1 = Path("/tmp")
BASE_DIR1.mkdir(exist_ok=True)

# location where image file will store
BASE_DIR2 = Path("IMAGE_FILES")
BASE_DIR2.mkdir(exist_ok=True)

# get daily regsitration numbers
get_regno="SELECT regno from livedata where DocumentUrl='{0}' is not null AND reciveddate='{1}'"


import itertools

# funtion to convert data into chunks     [list of reg no]  --> [chunks of regno]
def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := tuple(itertools.islice(it, n))):
        yield batch

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


# make chunks of regno to work on
l=sorted(os.listdir(BASE_DIR1))
chunked_rno = batched(l,10)

for chunk in chunked_rno:
    
    data = []
    for regno in chunk:
               
        try:

            # convert pdf into image
            pdf_name=regno.split('.')[0]

            regno_exist = int(pd.read_sql(find_query.format(pdf_name), con=connection)['count'])
            if regno_exist==1:
                continue

            print(pdf_name)
            image_path=str(BASE_DIR2)+'/'+pdf_name
            image_num=1

            #if os.path.getsize(str(BASE_DIR1)+'/'+regno)<1900000
            pages=convert_from_path(str(BASE_DIR1)+'/'+regno,300)

            image_dir = Path(image_path)        
            image_dir.mkdir(exist_ok = True)
            for page in pages:
                image_name='page_'+str(image_num)+'.jpg'
                page.save(image_path+'/'+image_name,'JPEG')
                image_num+=1

            # convert image to text data
            images_path=str(BASE_DIR2)+'/'+pdf_name
            images=os.listdir(images_path)
            text_dict={}
            fnl_text = str()
            for num in range(1,len(images)+1):

                image_path=images_path+'/page_'+str(num)+'.jpg'
                text=pytesseract.image_to_string(Image.open(image_path), lang='eng')
                text=text.replace('-\n','')
                fnl_text += text

            text_dict['regno'] = pdf_name
            text_dict['data'] = fnl_text
            data.append(text_dict)
        except:
            continue
        
    print("*********************Data Created***********************************")
    df = pd.DataFrame.from_dict(data)
    
    df.to_sql('pdfdata', engine, if_exists='append', index=False)
    
    print("*********************Data Inserted**********************************")
    for item in data:
        rno=item['regno']
        os.remove(str(BASE_DIR1)+'/'+rno+'.pdf')
        shutil.rmtree(str(BASE_DIR2)+'/'+rno, ignore_errors=False, onerror=None) 
connection.close()

