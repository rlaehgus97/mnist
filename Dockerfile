FROM python:3.11

WORKDIR /codes

COPY src/mnist/main.py /codes/
COPY run.sh /codes/run.sh

RUN apt update
RUN apt install -y cron
RUN apt install -y vim
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob
#RUN apt install -y vim

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade git+https://github.com/rlaehgus97/mnist.git@0.4/model

CMD ["sh", "run.sh"]
