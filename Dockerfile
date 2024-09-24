FROM python:3.11

WORKDIR /codes

RUN apt update
RUN apt install -y cron
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob

COPY src/mnist/main.py /codes/
COPY run.sh /codes/run.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/rlaehgus97/mnist.git@0.3

CMD ["sh", "run.sh"]
