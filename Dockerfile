FROM python:3.10-alpine

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .
EXPOSE 8080
CMD [ "flask", "run" ]
