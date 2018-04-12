# GeoPython Workshop 2018
## Task queues with Celery and RabbitMQ

Celery is a popular task queue library for the Python programming language. This demo application asynchronously executes a simple geoprocessing task which creates a geometry and writes it to a PostGIS database.

This application is a [docker-compose](https://docs.docker.com/compose/) orchestration of four Docker containers:

- [Celery](http://docs.celeryproject.org/en/latest/index.html) - Python Celery application to produce/consume messages (the worker)
- [RabbitMQ](https://www.rabbitmq.com/#getstarted) - Message broker (the queue)
- [Flower](http://flower.readthedocs.io/en/latest/) - Web app to monitor tasks
- [PostGIS](https://postgis.net/) - Spatial database to store task output

## Before you start...

This application requires [Docker Community Edition and Docker Compose](https://www.docker.com/community-edition).

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
- Monitor
- [periodic tasks](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)

Not all of these features are available in this project.

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

**This will force a complete rebuild so be aware this will also pull external images again.**

## Workshop begins...

#### Instantiate Celery application object

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

The `Celery` object has two required parameters:
- Name of the current module - 'tasks'
- URL of the message broker as a keyword argument

#### Defining a task

To define a task to run asynchronously, simply apply the `task` decorator to a function. This application has a single task `do_task` defined in `tasks.py`.

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

The `task` decorator takes several optional keyword arguments including the maximum number of reties to attempt in the event of a failure and a timeout limit for hanging tasks.

#### Calling tasks asynchronously

To "queue" a task use the `delay` function and provide the arguments which the `do_task` function requires.

*celery_app/demo.py*
```python
from app.tasks import do_task

def call_do_task():
    """Call the do_task task x times."""
    iterations = 2500

    for task_execution in range(iterations):

        x = get_random_x()
        y = get_random_y()

        do_task.delay(x, y)

        print(f"called do_task({x}, {y}) asynchronously")
...
```
Run `demo.py` from within the celery container:

```docker
docker exec -it <container id> /bin/sh -c "python demo.py"
```

As you can see the `do_task` function has been called 2500 times with random x and y values.

Check the process of the running/queued tasks in the [Flower web app](#monitoring-tasks-with-flower).

#### Viewing the results

If you have desktop GIS package (such as QGIS), you will be able to connect to PostGIS and add the `grid_squares` table as a vector layer.

The database connection details are:
- DB = geopython-db
- User = geopython
- Schema = geopython

From this table and the code, try and work out what the task does.

#### Challenge 1

The challenge is to write code to add tasks to the queue.

Hints:

1. Checkout branch `challenge-1`:
```bash
git checkout challenge-1
```

2. Look in *celery_app/demo.py* for the TODO comment relating to challenge 1

3. Look in *celery_app/app/tasks.py* to identify the function names and expected parameters of the the celery task.

4. In *celery_app/demo.py* write a loop that will iterate 2500 times.  Inside the loop, use the two helper functions `get_random_x` and `get_random_y` to get suitable x and y values, add these values to the queue.  You will need to use the special celery `delay` function.

5. Rebuild the docker containers after you have made your changes, then run `demo.py` within the docker container using docker exec.

6. You should now see your tasks being added to the queue in Flower, and hopefully being successfully processed.  You can optionally confirm that things are working by looking in QGIS or PgAdmin to see the items being added to the database table.

#### Challenge 2

The challenge is to get celery to retry processing a task in the event of a recoverable error.

Hints:

1. Checkout branch `challenge-2`.

2. Rebuild the docker containers, then run `demo.py`.  Observe that some tasks fail and none are retried.

3. Check the celery docs for [retrying failed tasks](http://docs.celeryproject.org/en/latest/userguide/tasks.html#retrying).

4. Look in *celery_app/app/service.py* to see where a random artificial error is thrown.  Note the exception type.

5. In the place where the celery task is executed (look for `TODO - challenge 2`), handle the above error using python exception handling, and trigger the Celery retry mechanism.  See if you can also add a retry delay.

6. Rebuild the docker containers after you have made your changes, then run `demo.py` - If you have been successful, you should see the retry counter in flower incrementing, and most likely no fails.  All tasks should pass after being retried.

#### Challenge 3

### Tests

```bash
python -m pytest tests
```
