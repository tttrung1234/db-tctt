FROM node:lts-alpine

WORKDIR /code

RUN npm install --global vite
COPY ./app/package.json .

RUN npm install


# COPY ./frontend ./app