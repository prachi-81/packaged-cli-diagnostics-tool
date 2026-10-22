
# Packaged CLI Diagnostics Tool

A Python command-line application that checks a developer's
environment and generates a readable or JSON health report.

## Features

- Detects the Python version and operating system.
- Checks available disk space.
- Checks selected environment variables without exposing their values.
- Detects common developer tools.
- Prints a readable report or structured JSON.
- Saves reports to files.
- Includes unit tests.

## Requirements

Python 3.10 or later.

## Installation

Create and activate a virtual environment, then run:

    python -m pip install -e .

## Usage

Readable report:

    envdoctor

JSON report:

    envdoctor --json

Save a text report:

    envdoctor --output reports/sample-report.txt

Save a JSON report:

    envdoctor --json --output reports/sample-report.json

## Run Tests

    python -m unittest discover -s tests -v

## Project Structure

- src/envdoctor/cli.py: main application
- tests/test_cli.py: automated tests
- reports/: example reports
- pyproject.toml: package configuration

## License

Choose and add a license before redistributing this project.
