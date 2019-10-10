# Lift App

[![Build Status](https://travis-ci.com/RDK90/lift_app.svg?token=DSACVxyKczSxGskhxsZK&branch=master)](https://travis-ci.com/RDK90/lift_app)
[![BCH compliance](https://bettercodehub.com/edge/badge/RDK90/lift_app?branch=master)](https://bettercodehub.com/)
[![Coverage Status](https://coveralls.io/repos/github/RDK90/lift_app/badge.svg?branch=ops/coveralls)](https://coveralls.io/github/RDK90/lift_app?branch=ops/coveralls)

## Intro
This app is designed to track workouts for analysis, with a particular emphasis on powerlifting. 

API documentation can be found at:
> lift/api.md

This is where the detailed information of each endpoint can be found including HTTP response codes, request parameters and body responses.

## Prerequisites
This app requires both docker and docker-compose to be installed locally. All other packages and requirements are installed in the containers specified in the docker and docker-compose files.

## Running the app
Clone the repo to your desired file location such as (on Linux):
```
mkdir file_location
git clone https://github.com/RDK90/lift_app.git
```
The Django app and Postgres database can be started by running both the containers. This can be done via docker-compose by running:
```
docker-compose up
```
The Django app can be found by navigating to 
> localhost:8000

Localhost, 127.0.0.1 or 0.0.0.0 are all valid hosts for this application

## Loading the database
Firstly, the tables need to be created. This can be using the migration method from the models API on the Django application.

Console into the Django container:
```
docker exec -it django bash
```
From there, run the migrations
```
django manage.py makemigrations
django manage.py migrate
```
This will create the required tables in Postgres based on the models specified in
> lift/workouts/models.py

Now run the following command in the Django container:
```
python port_data.py
```
This is migrate the data from the _traininglog.csv_ file into the Postgres database. To see this navigate to:
> localhost:8000/api/workouts

## Unit Tests
To run the unit tests, there are two main options. The first option is to use Django's built in testing framework. This can be done by logging into the Django container and running:
```
python manage.py test
```
The second option is to use Pytest. Pytest has been installed as part of the project and can give more in-depth statistics including test coverage. This can be run by logging into the Django container and running:
```
pytest
```
If you would like more detailed statistics about test coverage, pytest-cov has also been included. This will give a more detailed breakdown of the unit test coverage per Python file in the project. This can be run by logging into the Django container and running:
```
pytest --cov
```
This will run any of the tests in the following folder:
> lift/workouts/tests

## Postgres_monitor.py
On occasion the application can fail to run from the docker-compose file if the Django container tries to boot before the Postgres container. The _postgres_monitor.py_ file has been built to poll the Postgres container and only boot up the Django container once the Postgres container is ready to accept connections.
