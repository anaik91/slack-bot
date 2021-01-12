FROM python:3.7
RUN apt-get update && apt-get install -y python3-tk
RUN mkdir -p /slackbot
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /slackbot
EXPOSE 8080
WORKDIR /slackbot
ENTRYPOINT ["python"]
CMD ["bolt_app.py"]