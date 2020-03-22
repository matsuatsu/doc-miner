FROM node:10.14-alpine

RUN mkdir /app
WORKDIR /app

COPY ./package.json ./package-lock.json ./

RUN npm install
COPY . .

ENV HOST 0.0.0.0
