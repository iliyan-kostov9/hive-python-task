FROM eclipse-temurin:18 AS builder

ARG user=appuser
ARG group=appuser
ARG uid=1000
ARG gid=1000

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	software-properties-common \
	python3.11 python3.11-venv python3.11-dev \
	vim cmake build-essential \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${gid} ${group} \
	&& useradd -u ${uid} -g ${gid} -m -s /bin/bash ${user}

WORKDIR /hive
RUN chown -R ${user}:${group} /hive

USER ${user}


ENTRYPOINT ["/bin/bash"]
