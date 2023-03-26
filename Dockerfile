FROM python:3.10
WORKDIR /tasker
ADD requirements.txt /tasker/
ENV REDIS_PATH="redis://redis:6379"
RUN pip install -r requirements.txt
ADD . /tasker/
