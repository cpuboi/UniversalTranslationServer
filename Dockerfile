# TranslationServer:1.0
#FROM debian
FROM debian
MAINTAINER TEST <placeholder@mail.local>
WORKDIR /app
copy requirements.txt requirements.txt
copy translation_server translation_server
copy main.py main.py
RUN apt update -y

RUN apt upgrade -y
RUN apt install python3 python3-pip -y
RUN pip3 install setuptools_rust docker-compose
RUN pip3 install --upgrade pip
# If you dont have a CUDA GPU, remove the "torch" part from the requirements.txt and uncomment the below line.
# RUN pip3 install torch  --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r ./requirements.txt

#docker build -t translationserver:1.0 ./


