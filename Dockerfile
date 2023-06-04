#from the docker hub, get the linux environment-baseImage
FROM python:3.8-slim-buster
WORKDIR /app

#copy entire project folder => /app folder
COPY . /app

RUN apt update -y && apt install awscli -y

RUN pip install -r requirements.txt
CMD ["python3", "app.py"]