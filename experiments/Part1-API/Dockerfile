# syntax=docker/dockerfile:1
FROM python:alpine
WORKDIR /code
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN apk add mysql mysql-client
#RUN pip install mysqlclient
RUN pip install -r requirements.txt
RUN apk del build-deps
EXPOSE 5000
COPY . .
CMD ["flask", "run", "--debug"]


