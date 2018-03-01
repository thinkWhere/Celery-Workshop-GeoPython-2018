## GeoPython Workshop 2018
## Task queues with Celery and RabbitMQ

Build and run the containers (RabbitMQ, Celery, Flower)
```bash
docker-compose up -d
```

Attach to the celery container
```bash
docker exec -it geopythonceleryworkshop_celery_1 /bin/sh
```

Run a Python script to add tasks to the queue
```bash
python call_task.py
```

Flower is a monitoring application for Celery. In your web browser navigate to http://localhost:5555.

The RabbitMQ management plugin can be found at http://localhost:15672.

The username is "python_user" and password is "secret"
