FROM python:3.11

WORKDIR /codes

RUN apt update
RUN apt install -y cron
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob

COPY src/mnist/main.py /codes/

RUN pip install --no-cache-dir --upgrade git+https://github.com/rlaehgus97/mnist.git@0.3/cron

CMD service cron start;uvicorn main:app --host 0.0.0.0 --port 8080 --reload
