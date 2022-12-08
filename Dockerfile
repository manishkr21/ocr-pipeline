FROM python:3

WORKDIR /app

COPY . .

# ubuntu dependencies
RUN apt update && apt install -y poppler-utils libtesseract-dev  tesserect-ocr

# python dependencies
RUN pip install -r requirements.txt

# docker build -t 'image-name' .'(take docker file from here)'
# docker run --name 'containername' -d 'image-name' 'mycmd-to-run{sleep infinity}'
# docker exec -it containername bash 