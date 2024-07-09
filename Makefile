
##################
#
# Setup environment
#
# #################

.PHONY: setup
setup:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.txt
	echo "Python setup completed!"

###################
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


