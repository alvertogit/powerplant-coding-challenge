# SOLUTION TO POWERPLANT CODING CHALLENGE <!-- omit in toc -->

This repository stores a solution to Powerplant coding challenge using [Python], [FastAPI], [Docker] and [Docker Compose].

The original README with the full description can be found [here](/README_ORIGINAL.md).

- [DEPENDENCIES](#dependencies)
- [REPO CONTENT](#repo-content)
- [IMPLEMENTED SOLUTION](#implemented-solution)
  - [CODE FORMAT \& TESTING](#code-format--testing)
- [CREDITS](#credits)

## DEPENDENCIES

The code has been tested using:

- [Python] (3.12): an interpreted high-level programming language for general-purpose programming.
- [FastAPI] (0.115): a modern, fast (high-performance), web framework for building [APIs] with [Python].
- [Docker] (27.3): an open platform for developers and sysadmins to build, ship, and run distributed applications, whether on laptops, data center VMs, or the cloud.
- [Docker Compose] (2.29): a tool for defining and running multi-container [Docker] applications.

Command to start the project with Makefile:

```bash
~/powerplant-coding-challenge$ make run
```

Command to stop the project with Makefile:

```bash
~/powerplant-coding-challenge$ make stop
```

Command to launch test of the project with Makefile:

```bash
~/powerplant-coding-challenge$ make test
```

## REPO CONTENT

The main folder contains the following files. Please note the folder for `api`.

Virtual environment **.venv** can be generated with **requirements.txt** file found in project main folder.

```bash
powerplant-coding-challenge
├── .gitignore
├── .pre-commit-config.yaml
├── api
│   ├── Dockerfile
│   ├── main.py
│   ├── production_plan.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       └── test_production_plan.py
├── docker-compose.yml
├── example_payloads
│   ├── payload1.json
│   ├── payload2.json
│   ├── payload3.json
│   └── response3.json
├── Makefile
├── pyproject.toml
├── README.md
├── README_ORIGINAL.md
└── requirements.txt
```

## IMPLEMENTED SOLUTION

The implemented solution uses a Docker container for `api` microservice that provides the `productionplan` POST endpoint `http://localhost:8888/productionplant`.

### CODE FORMAT & TESTING

Ruff is used as linter and code formatter and is executed using pre-commit.
Pytest is used for testing and tests are executed using Makefile command `make test` locally.

The `/productionplan` endpoint API can also be tested manually in:

```bash
http://localhost:8888/docs
```

## CREDITS

author: alvertogit
copyright: 2024

[APIs]: https://en.wikipedia.org/wiki/API
[Docker]: https://www.docker.com/
[Docker Compose]: https://github.com/docker/compose
[FastAPI]: https://fastapi.tiangolo.com/
[Python]: https://www.python.org/
