FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y libmysqlclient-dev
COPY . /app
WORKDIR /app
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN pip install flask-WTF
RUN pip install passlib
EXPOSE 5000 
ENTRYPOINT ["python"]

