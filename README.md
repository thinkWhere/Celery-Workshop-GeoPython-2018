## GeoPython Workshop 2018
## Task queues with Celery and RabbitMQ

### Requirements

[Docker Community Edition including Docker Compose](https://www.docker.com/community-edition)

### Running the Celery app

Build and run the containers (RabbitMQ, Celery, Flower)
```bash
docker-compose up -d
```

Run a Python script (executed within the Celery container) to add tasks to the queue
```bash
docker exec -i geopythonceleryworkshop_celery_1 /bin/sh <<'EOF'
python demo.py
exit
EOF
```

### Monitoring

#### Flower

Flower is a monitoring application for Celery and is included in the Compose configuration. In your web browser navigate to http://localhost:5555. 

The "processed" tab should have a total of 20 successful tasks after running the Python script once.

#### RabbitMQ Management Plugin

The RabbitMQ management plugin can be found at http://localhost:15672.

The username is "python_user" and password is "secret".

### Tests

```bash
python -m pytest tests
```
