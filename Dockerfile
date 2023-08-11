FROM python:3.10-alpine3.18

WORKDIR /bots/burns_bot

RUN pip install --upgrade pip
RUN pip3 install --upgrade setuptools
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN chmod 755 .
COPY . .