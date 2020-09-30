FROM gradle:jdk11

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install git redis-server wget

RUN apt-get install -y gnupg
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN echo "deb https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list
RUN apt-get update
RUN apt-get install -y mongodb-org

USER root

RUN mkdir code
COPY . /code

RUN cd /code && ./gradlew bootjar

CMD /code/start.sh