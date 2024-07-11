
##################
#
# Setup environment
#
# #################

.PHONY: setup
setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip --require-virtualenv
	.venv/bin/pip install -r requirements.txt --require-virtualenv
	echo "Python setup completed!"
	echo "Next, please activate your virtual environment by using `source .venv/bin/activate`"
#
#
################
#
# Start server
#
# ################

.PHONY: server-start
server-start:
	python3 src/app.py

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

.PHONY: build-docker
build-docker:
	docker build -t hive-task .

.PHONY: run-docker
run-docker:
	docker run -it --name hive-task-con -v $(shell pwd):/host_hive hive-task

.PHONY: remove-docker-con
remove-docker-con:
	docker rm hive-task-con
