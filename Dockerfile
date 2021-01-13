FROM python:3.8.5-slim-buster
RUN mkdir -p /slackbot
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /slackbot
EXPOSE 8080
WORKDIR /slackbot
ENTRYPOINT ["python"]
CMD ["app.py"]