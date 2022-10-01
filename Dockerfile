ARG PYTHON_VERSION=3.10.6

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel
RUN sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
RUN sudo mkdir -p /etc/apt/keyrings
RUN  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN sudo apt-get update
RUN sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
RUN sudo service docker start

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt 

COPY . .
RUN mkdir -p storage
RUN python3 manage.py collectstatic --noinput


EXPOSE 8080

# replace APP_NAME with module name

CMD docker run -p 6379:6379 -d redis:5 && uvicorn social.asgi:application --workers 2
