# Lift App

[![Build Status](https://travis-ci.com/RDK90/lift_app.svg?token=DSACVxyKczSxGskhxsZK&branch=master)](https://travis-ci.com/RDK90/lift_app)
[![Coverage Status](https://coveralls.io/repos/github/RDK90/lift_app/badge.svg?branch=development)](https://coveralls.io/github/RDK90/lift_app?branch=development)

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
This app uses port 80 for incoming connections so before running ensure port 80 is not in use by another app. Or if another port is needed it can be modified in docker-compose configuration in the nginx port section.

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
> localhost/api/workouts

## Create a user
This app uses basic auth for all the APIs. To create a superuser for Django admin, follow the guide [here](https://docs.djangoproject.com/en/1.8/intro/tutorial02/#creating-an-admin-user). Use this user, or create another user in the [Django admin console](https://docs.djangoproject.com/en/1.8/intro/tutorial02/#enter-the-admin-site), to generate an auth token. This can be done by raising a POST request to the endpoint:
> localhost/api/login

with the username and password in the request body. An example curl request is below:
```
curl --location --request POST "http://localhost/api/login" \
--header "Accept: application/json" \
--header "Content-Type: application/json" \
--form "username=username" \
--form "password=password"
```
The token returned from this API can then be passed in as a value in the Authorization header such as: 
```
curl --location --request GET 'http://localhost/api/characteristics/999999' \
--header 'Accept: application/json' \
--header 'Authorization: Token token'
```

## Unit Tests
To run the unit tests, there are two main options. The first option is to use Django's built in testing framework. This can be done by logging into the Django container and running:
```
python manage.py test
```
The second option is to use Pytest. Pytest has been installed as part of the project and can give more in-depth statistics including test coverage. This can be run by logging into the Django container and running:

If you would like more detailed statistics about test coverage, pytest-cov has also been included. This will give a more detailed breakdown of the unit test coverage per Python file in the project. This can be run by logging into the Django container and running:
```
pytest --cov
```
This will run any of the tests in the following folder:
> lift/workouts/tests

## Postgres_monitor.py
On occasion the application can fail to run from the docker-compose file if the Django container tries to boot before the Postgres container. The _postgres_monitor.py_ file has been built to poll the Postgres container and only boot up the Django container once the Postgres container is ready to accept connections.
