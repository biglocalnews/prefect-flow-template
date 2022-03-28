A template for [Prefect](prefect.io) [flows](https://docs.prefect.io/orchestration/flow_config/overview.html)

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

## Deployment

Shipping your code to the production environment preferred by this template requires a few introductory steps.

1. Install Google Cloud’s [gcloud](https://cloud.google.com/sdk/docs/install) command line tool
2. Configure a Workload Identity Federation and Service Account with permission to access Google Artifact Registry
3. Create a Google Artifact Registry repository for a Docker image
4. Give your GitHub repository permission to use the service account to access Google Artifact Registry
5. Spin up a Prefect agent to orchestrate your flows

These steps are arcane. They will be frustrating. But you will likely only have to do them once.

While not included here, all of the steps are documented in the following blog posts by Big Local News.

* [How to push tagged Docker releases to Google Artifact Registry with a GitHub Action](https://gist.github.com/palewire/12c4b2b974ef735d22da7493cf7f4d37)
* [How to deploy a Prefect agent to Google Kubernetes Engine](https://gist.github.com/palewire/072513a9940478370697323c0d15c6ec)

Once all that is done, you'll want to set four secrets in your repository's settings. They will be used to deploy your code from GitHub into Google Cloud and Prefect.

* `PREFECT_API_KEY`: An API key created in your Prefect dashboard
* `PREFECT_PROJECT_NAME`: The name of your Prefect project
* `GCLOUD_WORKLOAD_IDENTITY_PROVIDER`: The name of the Workload Identity Provider created by Google
* `GCLOUD_SERVICE_ACCOUNT`: The name of the service account created by Google



With all that in hand, you should be ready to release.

## Releasing

OTheur release process is automated as a [continuous deployment](https://en.wikipedia.org/wiki/Continuous_deployment) via the [GitHub Actions](https://github.com/features/actions) framework. The logic that governs the process is stored [in the `workflows` directory](tree/.github/workflows/continuous-deployment.yml).

That means that everything necessary to make a release can be done with a few clicks on the GitHub website. All you need to do is make a tagged release at  then wait for the computers to handle the job.

Here's how it's done, step by step. The screenshots are from a different repository, but the process is the same.

### 1. Go to the releases page

The first step is to visit your repository's homepage and click on [the "releases" headline](./releases) in the right rail.

![Release button](.github/images/releasing-releases-button.png)

### 2. Click 'Draft a new release'

Note the number of the latest release. Click the "Draft a new release" button in the upper-right corner. If you don't see this button, you do not have permission to make a release. Only the maintainers of the repository are able to release new code.

![Draft button](.github/images/releasing-draft-button.png)

### 3. Create a new tag

Think about how big your changes are and decide if you're a major, minor or patch release.

All version numbers should feature three numbers separated by the periods, like `1.0.1`. If you're making a major release that isn't backwards compatible, the latest release’s first number should go up by one. If you're making a minor release by adding a feature or major a large change, the second number should go up. If you're only fixing bugs or making small changes, the third number should go up.

If you're unsure, review the standards defined at [semver.org](https://semver.org) to help make a decision. In the end don't worry about it too much. Our version numbers don't need to be perfect. They just need to be three numbers separated by periods.

Once you've settled on the number for your new release, click on the "Choose a tag" pull down.

![Tag button](.github/images/releasing-tag-button.png)

Enter your version number into the box. Then click the "Create new tag" option that appears.

![Tag dropdown](.github/images/releasing-name-tag.png)

### 4. Name the release

Enter the same number into the "Release title" box.

![Name box](.github/images/releasing-name-release.png)

### 5. Auto-generate release notes

Click the "Auto-generate release notes" button in the upper right corner of the large description box.

![Auto-generate release notes button](.github/images/releasing-changelog-button.png)

That should fill in the box below. What appears will depend on how many pull requests you've merged since the last release.

![Auto-generate release notes results](.github/images/releasing-changelog-entered.png)

### 6. Publish the release

Click the green button that says "Publish release" at the bottom of the page.

![Publish button](.github/images/releasing-publish-button.png)

### 7. Wait for the Action to finish

GitHub will take you to a page dedicated to your new release and start an automated process that release our new version to the world. Follow its progress by clicking on the [Actions tab](./actions) near the top of the page.

![Release page](.github/images/releasing-release-published.png)

That will take you to the Actions monitoring page. The task charged with publishing your release should be at the top.

![Actions page](.github/images/releasing-actions-start.png)

And that's it. The action should have released a new version of our Docker image in the Google Artifact Registry and re-registered the flows with Prefect. You could debug this process via Google Cloud Console and the Prefect dashboard, but it shouldn't be necessary if everything works.

## About

The project is sponsored by [Big Local News](https://biglocalnews.org/#/about), a program at Stanford University that collects data for impactful journalism. The code is maintained by [Ben Welsh](https://palewi.re/who-is-ben-welsh/), a visiting data journalist from the Los Angeles Times.
