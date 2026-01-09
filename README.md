# SpaceX Launch Tracker

A Python application that fetches, analyzes, and tracks SpaceX launches using the public SpaceX API v4.  
The application helps users explore launch history, apply filters, and generate meaningful launch statistics.

---

## Overview

This project uses SpaceX’s public REST API to retrieve information about launches, rockets, and launchpads.  
It provides tools to filter launches, calculate statistics, and analyze launch trends, while minimizing API calls through local caching.

---

## Features

- Fetch launch data from SpaceX API v4  
- Local caching to reduce repeated API requests  
- Filter launches by:
  - Date range
  - Launch success or failure
  - Rocket
  - Launch site
- Generate statistics:
  - Success rate by rocket
  - Total launches per launch site
  - Monthly and yearly launch frequency
- Fully unit-tested using `pytest`
- Written in Python 3.8+ with type hints
- Executable as a Python package


---

## Setup Instructions

## 1️.Clone the repository

git clone <your-repository-url>
cd spacex-launch-tracker

## 2️.Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate 

## 3️.Install dependencies
pip install -r requirements.txt

## Running the Application
python3 -m spacex_tracker

## Running the tests

python -m pytest
