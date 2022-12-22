FROM python:3

WORKDIR /app

COPY . .

# ubuntu dependencies
RUN apt-get update && apt-get install -y poppler-utils libtesseract-dev tesseract-ocr

# python dependencies
RUN pip install -r requirements.txt

# docker build -tag 'image-name' .'(take docker file from here)'    --> docker build -t myimg .
# docker run --name 'containername' -d 'image-name' 'mycmd-to-run{sleep infinity}'  --> docker run --name mycont -d myimg sleep infinity
# docker exec -it containername bash   
# to get permission --->>  sudo chmod 666 /var/run/docker.sock 
