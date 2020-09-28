#!/bin/bash

mongoimport --db greetings --collection greetings --drop --jsonArray --file /code/sample-data/sample-data.json