FROM python:3.9-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    netcat \
    libpq-dev python-dev

RUN groupadd steam && useradd -m -s /bin/bash -g steam steam

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

USER $steam
CMD ["python", "server.py"]
