#!/bin/bash

#echo DB_IP=$DB_IP >> /etc/environment;
#echo LINE_TOKEN=$LINE_TOKEN >> /etc/environment;
env >> /etc/environment;

service cron start;uvicorn main:app --host 0.0.0.0 --port 8080 --reload
