FROM python:3.6.4

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools
RUN pip install pipenv
RUN pipenv install

WORKDIR /app

COPY . .
