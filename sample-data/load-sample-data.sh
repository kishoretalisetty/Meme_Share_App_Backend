#!/bin/bash

mongoimport --db greetings --collection greetings --drop --jsonArray --file ./sample-data.json