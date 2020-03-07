FROM python:3.7-alpine

WORKDIR /app

# check config.yaml before copy files in container
COPY iliadbot/ iliadbot/
COPY config/ config/
COPY setup.py .

RUN apk add --update --no-cache --virtual .build-deps \
    g++ \
    libxml2 \
    libffi-dev \
    openssl-dev \
    libxml2-dev && \
    apk add libxslt-dev

RUN python setup.py install

RUN apk del .build-deps

VOLUME [ "/app/localdb" ]

CMD [ "iliadbot", "config/config.yaml"] 
