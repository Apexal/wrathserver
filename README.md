# Wrathserver

A REST API and websocket server for facilitating the creation of characters for Wrathskeller.

## Planned Features

- [ ] Store characters from Wrathspriter
- [ ] Retrieve characters from Wrathskeller
- [ ] Remove image backgrounds using machine learning
- [ ] Check match between proposed image and template image

## Setup

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

```bash
$ poetry shell
$ pytest .
```
