FROM eclipse-temurin:18 AS builder

ARG user=hive-member
ARG group=hive
ARG uid=1000
ARG gid=1000

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	software-properties-common \
	python3.11 python3.11-venv python3.11-dev \
	vim cmake build-essential \
	libgl1-mesa-glx libglib2.0-0 \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${gid} ${group} \
	&& useradd -u ${uid} -g ${gid} -m -s /bin/bash ${user}

WORKDIR /hive
RUN chown -R ${user}:${group} /hive

COPY --chown=${user}:${group} requirements.txt /hive/
COPY --chown=${user}:${group} src /hive/src/
COPY --chown=${user}:${group} assets /hive/assets/
COPY --chown=${user}:${group} pages /hive/pages/
COPY --chown=${user}:${group} Makefile /hive/Makefile

USER ${user}

RUN python3.11 -m venv /hive/.venv \
	&& /hive/.venv/bin/pip install --upgrade pip \
	&& /hive/.venv/bin/pip install -r /hive/requirements.txt \
	&& ls -l /hive \
	&& ls -l /hive/.venv \
	&& /hive/.venv/bin/python --version

ENV VIRTUAL_ENV=/hive/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENTRYPOINT ["/bin/bash"]
