# GeoPython Workshop 2018
## Task queues with Celery and RabbitMQ

introduction

## Before you start...

This application requires [Docker Community Edition and Docker Compose](https://www.docker.com/community-edition)

This application is a docker-compose orchestration of four Docker containers:

- Celery - Python Celery application to produce/consume messages
- Flower - Web app to monitor tasks
- RabbitMQ - Message broker (the queue)
- PostGIS - Spatial database to store task output

### Controlling the application

1. Open a terminal and change directory to the location of `docker-compose.yml`.

2. Build and start the containers:

  `docker-compose up --build`

  The console will display the stdout from each container.

  This command will pull the necessary docker images from Docker hub and build the application from Dockerfiles. You can inspect the docker-compose file to see gain an understanding of the application structure.

3. Check everything is running OK with the command:
  `docker-compose ps`
  The state of each container should be "Up"

### changing the code

### troubleshooting

## Workshop begins...

### Executing tasks asynchronously
run demo.py

### Monitoring tasks

In your browser navigate to http://localhost:5555/

Inspect failed tests exceptions


### Challenge 1
### Challenge 2
### Challenge 3

###########################################



### Running the Celery app

Build and run the containers (RabbitMQ, Celery, Flower)
```bash
docker-compose up -d
```

Run a Python script (executed within the Celery container) to add tasks to the queue
```bash
docker exec -ti celeryworkshopgeopython2018_celery_1 sh -c "python demo.py"
```

### Monitoring

#### Flower

Flower is a monitoring application for Celery and is included in the Compose configuration. In your web browser navigate to http://localhost:5555.

The "processed" tab should have a total of 20 successful tasks after running the Python script once.

#### RabbitMQ Management Plugin

The RabbitMQ management plugin can be found at http://localhost:15672.

The username is "celery_user" and password is "secret".

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
