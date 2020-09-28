# IMPORTANT!
# Image should be built on the context of `cloud-assessment` directory.
# Command to be run in `cloud-assessment` dir - `docker build -t <image_name>:<tag> -f me_assessments/me_qeats_review/Dockerfile .

FROM gradle:jdk11

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install git redis-server wget
RUN wget https://repo.mongodb.org/apt/ubuntu/dists/bionic/mongodb-org/4.2/multiverse/binary-amd64/mongodb-org-server_4.2.1_amd64.deb -P /mongo-temp && cd /mongo-temp && apt-get install -y ./mongodb-org-server_4.2.1_amd64.deb && rm -rf /mongo-temp

USER root

RUN mkdir code
COPY . /code

RUN cd /code && ./gradlew bootjar --stacktrace

CMD /code/start.sh