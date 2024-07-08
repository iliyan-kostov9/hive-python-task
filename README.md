# Introduction

This application is created based on the requiremnets, listed at `TASK.md`.


## Setup instruction

1. Via CMake (recommended)

    1. Create a virtual environment and install the dependencies:

    ```bash
    make setup
    ```

    2. Run the webserver:

    ```bash
   mmake server-start
    ```


2. Manual

    1. Create and activate the virtual environment

    ```bash
	python3 -m venv .venv
	source .venv/bin/activate
    ```

    2. Install the dependencies

    ```bash
	pip install -r requirements.txt
    ```

    3. Run the webserver

    ```bash
	python3 -m http.server -b 127.0.0.0 8080 -d pages
    ```
