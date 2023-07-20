FROM gradle:jdk11-focal

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y install git redis-server wget gnupg

RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org

USER root

RUN mkdir code
COPY . /code

RUN cd /code && chmod +x gradlew && ./gradlew bootjar

CMD /code/start.sh
