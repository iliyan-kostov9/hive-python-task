# Introduction

This application is created based on the Hive requirements, listed at `TASK.md`.

## Setup instructions

### 1. Install dev tools

First we need to install the necessary tools, in order to clone and execute the app.
I have provided instructions for both Ubuntu and NixOS (for Arch/ Redhat, you can just swap the `apt` with `pacman/dnf`)

#### Ubuntu

Please make sure you have `git` and `python3` installed, if not then please execute:

```bash
sudo apt install git
sudo apt install python3
# For using virtual environment
# Replace with the python version you are using, you can check it with `python3 --version`
sudo apt install python3.12-venv
```

Usually you should have python3 already installed, you can check with:

```bash
python3 --version
```

#### NixOS

You can either add the packages to `configuration.nix` or create a temporarily shell:

```bash
# configuration.nix

  environment.systemPackages = [
    pkgs.python3
    pkgs.git
  ];
```

Nix shell

```bash
nix-shell -p python3
nix-shell -p git
```

### 2. Clone the repository

Now let's clone the application repo by running the command:

```bash
git clone https://github.com/IliyanKostov9/hive-python-task
```

The output of a successful message should look something similar like:

```bash
sandbox@sandbox-Standard-PC-Q35-ICH9-2009:~/repos$ git clone https://github.com/IliyanKostov9/hive-python-task.git
Cloning into 'hive-python-task'...
remote: Enumerating objects: 97, done.
remote: Counting objects: 100% (97/97), done.
remote: Compressing objects: 100% (79/79), done.
remote: Total 97 (delta 32), reused 61 (delta 8), pack-reused 0
Receiving objects: 100% (97/97), 36.38 KiB | 564.00 KiB/s, done.
Resolving deltas: 100% (32/32), done.
sandbox@sandbox-Standard-PC-Q35-ICH9-2009:~/repos$ cd hive-python-task/
```

If yes, then you are ready to go to step 3!

### 3. Install project dependencies

There are several approaches for installing and running the app:

#### 1. CMake (recommended)

CMake is a build automation tool, that can help us organize a collection of scripts into a single one.
If you don't have it already installed, then run:

```bash
sudo apt install make
```

For Nix use:

```bash
nix-shell -p make
```

1. Create a virtual environment and install the dependencies:

```bash
make setup
```

2. Activate the virtual environment

```bash
source .venv/bin/activate
```

3. Run the web server:

```bash
make server-start
```

2. Manual

1. Create and activate the virtual environment

```bash
    python3 -m venv .venv
    source .venv/bin/activate
```

2. Install the dependencies

```bash
    pip install --upgrade pip
    pip install -r requirements.txt
```

3. Run the web server

```bash
    python3 src/app.py
```

3. Docker

<div style="border-left: 4px solid #007bff; padding-left: 10px; margin-bottom: 10px;">
  <strong>Note:</strong> The docker image is still in development and for some reason the python app is not able to function as intended, due to the native container isolation affecting the async running of the web server && socket. Until I release a `RELEASE` image version, please ignore this part</div>

1. Pull the docker image:
    - GitHub: `docker pull ghcr.io/iliyankostov9/hive-python-task:0.0.1-snapshot`
    - Codeberg: `docker pull codeberg.org/iliyan-kostov/hive-python-task:0.0.1-snapshot`

2. Create a container and run it:

```bash
docker run -d -p 8080:8080 -p 8001:8001 --network host -m 2g --cpus=2 --name hive-python-task hive-python-task:0.0.1-RELEASE
```

Or simply with docker compose

```bash
docker compose up -d
```
