import os

import prefect
from prefect.executors import LocalDaskExecutor
from prefect.run_configs import KubernetesRun, LocalRun
from prefect.storage import Docker, Local

#
# Environment variables
#

# Get the environment where the flow is operating.
# Options are 'development' and 'production'. The default is 'production'.
# When you are working locally you should create .env file and add:
#   PREFECT_FLOW_ENV=development
# You can do that automatically with:
#   echo 'PREFECT_FLOW_ENV=development' > .env
PREFECT_FLOW_ENV = os.getenv("PREFECT_FLOW_ENV", "production")


#
# Tasks
#


@prefect.task(name="Hello task")
def hello_task():
    """Run an example task."""
    logger = prefect.context.get("logger")
    logger.info("Hello world!")


#
# Flows
#


def get_storage(env: str = "production"):
    """Get the storage method used by the flow.

    Args:
        env (str): the environment where the task is running. Options are 'development' and 'production'.

    Returns Prefect Storage instance
    """
    logger = prefect.context.get("logger")
    logger.debug(f"Loading {env} storage method")
    options = {
        "development": Local(
            # The flow is stored as a file here on your laptop
            add_default_labels=False,  # <-- This makes sure the hostname label isn't applied
        ),
        "production": Docker(
            # An image containing the flow's code, as well as our Python dependencies,
            # will be compiled when `pipenv run prefect register` is run and then
            # uploaded to our repository on Google Artifact Registry.
            registry_url="your-region-docker.pkg.dev",  # <-- Here's the docker registry where it will go
            image_name="your-project-id/your-docker-repo/your-docker-image-name",  # <-- Here's the path within the registry to your image
            python_dependencies=[],
        ),
    }
    return options[env]


def get_run_config(env: str = "production"):
    """Get the run_config used by the flow.

    Args:
        env (str): the environment where the task is running. Options are 'development' and 'production'.

    Returns Prefect Run instance
    """
    logger = prefect.context.get("logger")
    logger.debug(f"Loading {env} run_config method")
    options = {
        "development": LocalRun(
            # The flow is run here on your laptop
            env={
                # Print logs from our dependencies
                "PREFECT__LOGGING__EXTRA_LOGGERS": "[]",
                # Print debugging level code from Prefect
                "PREFECT__LOGGING__LEVEL": "DEBUG",
            },
            # Tag the task
            labels=["etl"],
        ),
        "production": KubernetesRun(
            # The flow is run as a job in our k8s cluster
            env={
                # Print logs from our dependencies
                "PREFECT__LOGGING__EXTRA_LOGGERS": "[]",
                # Print debugging level code from Prefect
                "PREFECT__LOGGING__LEVEL": "DEBUG",
            },
            # Tag the task
            labels=["etl"],
            # Tell k8s how big the server should be that runs the jobs
            # By setting it to two CPUs, we can use the local dask executor
            # to run multiple jobs at the same time.
            cpu_request=2,
            memory_request="2Gi",
        ),
    }
    return options[env]


def get_executor(env: str = "production"):
    """Get the executor used by the flow.

    Args:
        env (str): the environment where the task is running. Options are 'development' and 'production'.

    Returns Prefect Executor instance
    """
    logger = prefect.context.get("logger")
    logger.debug(f"Loading {env} executor method")
    options = {
        "development": LocalDaskExecutor(),
        "production": LocalDaskExecutor(
            scheduler="threads",
            num_workers=4,
        ),
    }
    return options[env]


with prefect.Flow(
    "Your Prefect Flow",
    storage=get_storage(PREFECT_FLOW_ENV),
    run_config=get_run_config(PREFECT_FLOW_ENV),
    executor=get_executor(PREFECT_FLOW_ENV),
) as flow:
    # Run example task
    hello_task()
