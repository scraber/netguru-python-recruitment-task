FROM python:3.8.6-buster
WORKDIR /netguru
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /netguru/
RUN pip install -r requirements.txt
COPY . /netguru/
