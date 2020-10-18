FROM python:3

RUN apt-get update && apt-get install git

RUN mkdir /bot
WORKDIR /bot

COPY . /bot/ 
RUN pip install --upgrade pip && pip install -r requirements.txt
