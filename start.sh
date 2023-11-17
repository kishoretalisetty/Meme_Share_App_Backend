#!/bin/bash

mkdir -p /data/db
mkdir log
mongod --fork --logpath log/mongod.log --bind_ip 0.0.0.0
ps -aux | grep mongod

cd /code/sample-data
./load-sample-data.sh
cd -
java -jar /code/build/libs/spring-starter-0.0.1-SNAPSHOT.jar