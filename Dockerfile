FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

WORKDIR /app

RUN apk --update add bash nano

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY src/ .env application.py /app/

ENTRYPOINT ["python3", "application.py"]
