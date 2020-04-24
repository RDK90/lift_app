from time import sleep

import docker

client = docker.from_env()
limit = 20
num_of_tries = 1
check_message = "database system is ready to accept connections\\n'"
postgresup = False
while num_of_tries < limit:
    try:
        postgres = client.containers.get('postgres')
        postgres_logs = postgres.logs(tail=1)
        message = str(postgres_logs).split("LOG:  ")
        print(message)
        if len(message) > 1:
            message = message[1]
        if message == check_message:
            print("Postgres is ready")
            postgresup = True
            break
        else:
            print("Attempt number: " + str(num_of_tries) + " out of: " + str(limit))
            num_of_tries += 1
            sleep(2)
    except docker.errors.APIError as error:
        print(error)
assert (postgresup)
