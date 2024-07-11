
##################
#
# Setup environment
#
# #################

.PHONY: setup
setup:
	python3 -m venv .venv && \
	.venv/bin/pip install --upgrade pip --require-virtualenv && \
	.venv/bin/pip install -r requirements.txt --require-virtualenv && \
	. .venv/bin/activate && \
	echo "Python setup completed!"###################
#
# Start server
#
# ################


.PHONY: server-start
server-start:
	python3 src/app.py

# python3 -m http.server -b 127.0.0.0 8080 -d pages


##################
#
# Testing
#
# ###############

.PHONY: simulate-user
simulate-user:
	python3 -m websockets ws://localhost:8001/


################

# Utility functions
#
# ################

.PHONY: watchdog-install
watchdog-install:
	pip install 'watchdog[watchmedo]' --require-virtualenv -q
	echo "watchdog installed!"


####################
#
# Docker
#
# ################



.PHONY: setup-docker
setup-docker:
	docker build -t hive-task .
# docker run -it --name hive-task-con -v $(pwd):/hive hive-task

.PHONY: remove-docker-con
remove-docker-con:
	docker rm hive-task-con
