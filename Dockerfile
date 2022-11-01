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
# This is for the CPU version, remove the extra index url for GPU
RUN pip3 install torch  --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r ./requirements.txt

#docker build -t translationserver:1.0 ./


