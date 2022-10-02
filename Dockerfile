ARG PYTHON_VERSION=3.10.6

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel


RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt 

COPY . .
RUN mkdir -p storage
RUN python3 manage.py collectstatic --noinput


EXPOSE 8080


CMD bash run.sh