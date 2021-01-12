FROM python:3.8.5-slim-buster as builder
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.8.5-slim-buster
RUN apt-get update && apt-get install -y python3-tk
RUN mkdir -p /slackbot
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY . /slackbot
EXPOSE 8080
WORKDIR /slackbot
#ENTRYPOINT ["python"]
#CMD ["app.py"]
ENTRYPOINT gunicorn --bind :8080 --workers 2 --threads 2 --timeout 0 main:flask_app