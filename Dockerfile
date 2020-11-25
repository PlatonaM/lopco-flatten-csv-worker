FROM python:3-alpine

RUN apk update && apk upgrade && apk add curl

RUN mkdir data_cache

WORKDIR /usr/src/worker

COPY . .

CMD [ "./main.sh"]
