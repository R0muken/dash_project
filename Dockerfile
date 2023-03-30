FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y nano
RUN mkdir -p /opt/program
RUN mkdir -p /opt/ml/processing

WORKDIR /opt/ml/processing/

COPY requirements.txt /opt/ml/processing/
COPY json_generator.py /opt/ml/processing/
COPY data.json /opt/ml/processing/

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT python3 json_generator.py