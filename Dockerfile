FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk update
RUN apk upgrade
RUN apk add --no-cache ffmpeg git
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
