FROM python:3.11.9-slim-bookworm
WORKDIR /app
COPY requirements.txt /app

RUN apt-get update && apt-get install -y libgl1-mesa-dev libglib2.0-0 libsm6 libxrender1 libxext6 cmake

RUN pip install --upgrade pip -q \
	&& pip install wheel \
	&& pip install -r requirements.txt
COPY . /app

EXPOSE 8080 8001

LABEL org.opencontainers.image.source=https://codeberg.org/iliyan-kostov/hive-python-task \
	version="0.0.1-RELEASE" \
	description="Hive python task for image capture"

LABEL org.opencontainers.image.source=https://github.com/IliyanKostov9/hive-python-task \
	version="0.0.1-RELEASE" \
	description="Hive python task for image capture"

ENTRYPOINT ["make","server-start"]
