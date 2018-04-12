# GeoPython Workshop 2018
## Task queues with Celery and RabbitMQ

Celery is a popular task queue library for the Python language. This demo application asynchronously executes a simple geoprocessing task which creates a geometry and writes it to a PostGIS database. RabbitMQ is configured as the message broker. No results backend is used for this application.

## Before you start...

This application requires [Docker Community Edition and Docker Compose](https://www.docker.com/community-edition).

This application is a [docker-compose](https://docs.docker.com/compose/) orchestration of four Docker containers:

- Celery - Python Celery application to produce/consume messages (the worker)
- [RabbitMQ](https://www.rabbitmq.com/#getstarted) - Message broker (the queue)
- [Flower]((http://flower.readthedocs.io/en/latest/)) - Web app to monitor tasks
- [PostGIS](https://postgis.net/) - Spatial database to store task output

#### Build and run the containers

1. Open a terminal and change directory to the location of `docker-compose.yml`.

2. Build and start the containers (some images are pulled from Docker hub - be patient!):

  ```docker
  docker-compose up --build
  ```

  The console will display the stdout from each container as they build and run.

  You can inspect the docker-compose file to gain a further understanding of the application structure.

3. Check everything is running OK, in a new terminal window (as it is starting up interactively in the first console):

  ```docker
  docker-compose ps
  ```

  The state of each container should be "Up".

4. You may wish to execute commands inside a container:

  ```docker
  docker exec -it <container id> /bin/sh -c "<command for container>"
  ```

5. Stop the containers by cancelling the process in terminal window.

#### Re-deploying changes to the code

Each time you make a change to any Python files run the command in step 2 - `docker-compose up --build`. This will rebuild the images incorporating any changes.

#### Monitoring tasks with Flower

Flower is a web application for monitoring Celery tasks. Once the application is running, in your web browser navigate to http://localhost:5555.

Flower provides monitoring of task executed by the worker. Some of Flowers features include:

- View tasks on the queue
- Inspect and control tasks
- Inspect failed tasks exception messages
- Control worker process pool size
- Monitor [perodic tasks](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)

Not all of these features are avaliable in this project.

#### Troubleshooting

The logs of each container can be inspected with the command:

```docker
docker logs <container id>
```

The container ID's can be identified with the docker ps command.

If you think you container is broken beyond repair run:

```docker
docker-compose up --force-recreate
```

This will force a complete rebuild so be aware this will also pull external images again.

## Workshop begins...

#### Instantiate Celery object

Before defining any tasks, a Celery application object must be instantiated.

*celery_app/app/tasks.py*
```python
from celery import Celery

# URL to connect to broker
broker_url = 'amqp://celery_user:secret@rabbitmq:5672/celery_app'

# Create Celery application
application = Celery('tasks', broker=broker_url)

...
```

The `Celery` object has two required paramters:
- Name of the current module - 'tasks'
- URL of the message broker as a keyword argument

#### Defining a task

To define a task to run asynchronously, simply apply the `task` decorator to a function. In this application a single task `do_task` is defined in `tasks.py`.

*celery_app/app/tasks.py*
```python
...

@application.task(base=AppBaseTask, bind=True, max_retries=3, soft_time_limit=5)
def do_task(self, x, y):
    """Performs simple geoprocessing task.

    Failed tasks are retried x times by the Task classes on_retry method.
    When tasks fail completely they are handled by the Task classes on_failure method

    Args:
        self: instance of the Task
        x: integer
        y: integer

    Raises:
        TaskError: failed tasked are handled by the parent task class.
    Returns:
        None
    """
    try:
        geoprocess(x, y)
    except ServiceError as se:
        self.retry(countdown=10, exc=se)
    except Exception as exc:
        raise TaskError(exc)
...
```

#### Calling tasks asynchronously

To call the task asynchronously the Python file demo.py:
```docker
docker exec -it <container id> /bin/sh -c "python demo.py"
```

#### Challenge 1
#### Challenge 2
#### Challenge 3

### Tests

```bash
python -m pytest tests
```

### Postgis database
Port: 5432

DB: geopython-db
User: geopython
schema: geopython

tables: grid_squares - for holding results. style_cat field will hold the 3-letter codes below
uk_boundary - UK dataset in BNG. Has several columns with names, but gu_a3 contains 3-letter code for each region: ENG, SCT, NIR, IMN, WLS

Have included the docker scripts in the pull request for reference, but they shouldn't be needed for the workshop. Docker image download size ~ 174MB
