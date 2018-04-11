# GeoPython Workshop 2018
## Task queues with Celery and RabbitMQ

introduction

## Before you start...

This application requires [Docker Community Edition and Docker Compose](https://www.docker.com/community-edition).

This application is a docker-compose orchestration of four Docker containers:

- Celery - Python Celery application to produce/consume messages (the worker)
- Flower - Web app to monitor tasks
- RabbitMQ - Message broker (the queue)
- PostGIS - Spatial database to store task output

### Build and run the containers

1. Open a terminal and change directory to the location of `docker-compose.yml`.

2. Build and start the containers (some images are pulled from Docker hub - be patient!):

  `docker-compose up --build`

  The console will display the stdout from each container as they build and run.

  You can inspect the docker-compose file to gain a further understanding of the application structure.

3. Check everything is running OK with the command:

  `docker-compose ps`

  The state of each container should be "Up".

4. You may wish to execute commands inside a container:

  `docker exec -it <container id> /bin/sh -c "<command for container>"`

5. Stop the containers by cancelling the process in terminal window.

### Redeploying changes to the code

Each time you make a change to any Python files run the command in step 2 - `docker-compose up --build`. This will rebuild the images incorporating any changes.

### Monitoring tasks with Flower

Flower is a web application for monitoring Celery tasks. In your web browser navigate to http://localhost:5555.

Flower enables monitoring of task being excecuting by the worker including

### Troubleshooting

The logs of each container can be inspected with the command:

`docker logs <container id>`

The container ID's can be identified with the docker ps command.

If you think a container is broken beyond repair run:

`docker-compose up --force-recreate`

Be aware this will also pull external images again.

## Workshop begins...

### Executing tasks asynchronously

To call the task asynchronously run the command:

`docker exec -it <container id> /bin/sh -c "python demo.py"`

### Challenge 1
### Challenge 2
### Challenge 3

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
