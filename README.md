# Wrathserver

A REST API for facilitating the creation of characters for Wrathskeller.

## Planned Features

- [x] Store characters from Wrathspriter
- [x] Retrieve characters from Wrathskeller
- [x] Remove image backgrounds using machine learning
- [ ] Normalize pose images
- [x] Normalize audio volume
- [ ] Lessen audio background noise
- [ ] Trim audio silence

## Setup
- Install Python 3.8.13
- Install FFMPEG
- Install [Poetry package manager](https://python-poetry.org/docs/)
- Clone repository `$ git clone git@github.com:Apexal/wrathserver.git`
- Download dependencies `$ poetry install`
- Create `.env` file with environment variables `$ cp .env.example .env`

## Running Locally

```bash
$ poetry shell
$ uvicorn api.main:app --reload
```

Navigate to `http://localhost:8000/docs` to view the OpenAPI dashboard.

## Running Tests

Write tests under `api/tests` in files that start with `test_`. Simply write functions that start with `test_` and they will be run when you run the commands below.

```bash
$ poetry shell
$ pytest .
```
