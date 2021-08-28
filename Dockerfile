FROM node:16.7.0-alpine3.14

RUN npm i -g hasura-cli
RUN mkdir -p /hasura

WORKDIR /hasura

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY config.yaml config.yaml
COPY migrations migrations
COPY metadata metadata

ENTRYPOINT [ "docker-entrypoint.sh" ]
