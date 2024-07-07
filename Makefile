.PHONY: setup
setup:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.txt
	echo "Python setup completed!"

.PHONY: server-start
server-start:
	python3 -m http.server -b 127.0.0.0 8080 -d pages

.PHONY: watchdog-install
watchdog-install:
	pip install 'watchdog[watchmedo]' --require-virtualenv -q
	echo "watchdog installed!"

.PHONY: socket-start
socket-start:
	watchmedo auto-restart --pattern "*.py" --recursive --signal SIGTERM \
    python3 src/main.py

.PHONY: simulate-user
simulate-user:
	python3 -m websockets ws://localhost:8001/
