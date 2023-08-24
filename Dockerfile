# TranslationServer:1.0
#FROM debian
FROM debian
MAINTAINER TEST <placeholder@mail.local>
WORKDIR /app
copy requirements.txt requirements.txt

#  This is instead configured in docker-compose, mount ./ to /app
#copy translation_server translation_server
#copy main.py main.py

RUN apt update -y

RUN apt upgrade -y
RUN apt install python3 python3-pip -y
RUN pip3 install --upgrade pip --break-system-packages
#RUN pip3 install setuptools_rust docker-compose  --break-system-packages
# If you dont have a CUDA GPU, remove the "torch" part from the requirements.txt and uncomment the below line.
# RUN pip3 install torch  --extra-index-url https://download.pytorch.org/whl/cpu

#RUN pip3 install -r ./requirements.txt # For Debian 11 and older
RUN pip3 install -r ./requirements.txt --break-system-packages # For Debian 12

# Command to run
# docker build -t translationserver:1.0 ./


