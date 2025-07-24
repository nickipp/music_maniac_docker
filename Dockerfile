FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY main.py ./
COPY maniac.py ./
COPY urlcheck.py ./

RUN apk update
RUN apk upgrade
RUN apk add --no-cache ffmpeg git
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del git

CMD [ "python", "./main.py" ]
