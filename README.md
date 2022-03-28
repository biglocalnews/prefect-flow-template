A template for [Prefect](prefect.io) [flows](https://docs.prefect.io/orchestration/flow_config/overview.html).

## How it works

This repository contains all the fundamentals needed to develop and deploy a Python routine that runs within Prefect’s cloud pipelines.

It contains:

* A `flow.py` file with an example function that’s ready to run
* A local development configuration that can run independently
* A cloud production configuration for a Google Kubernetes Engine executor with Docker storage
* Easy vertical scaling of production workers via Dask
* Unit tests via pytest
* Automated deployment via GitHub releases and actions

The repository does not include the necessary configuration of a [Prefect Agent](https://docs.prefect.io/orchestration/agents/overview.html) to orchestrate flow runs.

## Getting started

Install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

Create a new repository using this template. Clone your repository and move into the directory on your terminal.

Install our Python dependencies.

```bash
pipenv install --dev
```

Install pre-commit to run a battery of automatic quick fixes against your work.

```bash
pipenv run pre-commit install
```

Set the `PREFECT_FLOW_ENV` environment variable to 'development'. You can do this with an `export` command but if you're using `pipenv` I recommend you add it to [an .env file](https://pipenv.pypa.io/en/latest/advanced/#automatic-loading-of-env) at the root of your project.

```bash
echo 'PREFECT_FLOW_ENV=development' > .env
```

Tell Prefect to run a local server on your computer.

```bash
pipenv run prefect backend server
```

Start the local server.

```bash
pipenv run prefect server start
```

Open a new terminal, move into your code directory and create a local version of our Prefect project on your local machine. The project name is set in your `flow.py` file. If you'd like to customize it right away, edit it there and insert your name in the code below.

```sh
pipenv run prefect create project 'Your Prefect Project'
```

To make changes to the process, edit `flow.py`. Then send your updates to the server with the line below. If you customize the name of the Prefect flow, edit it below to match.

```bash
pipenv run prefect register --project 'Your Prefect Project' -p ./flow.py
```

Start an agent in the background to run your tasks.

```bash
pipenv run prefect agent local start --no-hostname-label --label etl
```

Navigate to `http://localhost:8080` to run flows and see the results.

Future changes to the flow will need to registered with the local server, as before:

```bash
pipenv run prefect register --project 'Your Prefect Project' -p ./flow.py
```
