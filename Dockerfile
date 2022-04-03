FROM python:3.10-slim-buster

RUN apt-get update && apt-get install default-libmysqlclient-dev -y \
&& apt-get install gcc -y
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .
EXPOSE 8080
CMD [ "flask", "run" ]
