# Dockerfile
FROM python:3.9.0
RUN mkdir /workspace　
WORKDIR /workspace
COPY requirements.txt /workspace/
RUN pip install -r requirements.txt
RUN cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
COPY . /workspace/
RUN apt update
RUN apt-get install -y cron
RUN apt-get install -y vim
RUN chmod +x /workspace/script.sh

CMD cron && tail -f /var/log/cron.log