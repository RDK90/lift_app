import docker
from time import sleep

client = docker.from_env()
limit = 10
num_of_tries = 1
check_message = "database system is ready to accept connections\\n'"
postgresup = False
while num_of_tries < limit:
    try:
        postgres = client.containers.get('postgres')
        print(postgres.status)
        postgres_logs = postgres.logs()
        print(str(postgres_logs))
        message = str(postgres_logs).split("LOG:  ")
        print(message)
        if message[1] == check_message:
            print("Postgres is ready")
            postgresup = True
            break
        else:
            print("Attempt number: " + str(num_of_tries) + " out of: " + str(limit))
            num_of_tries += 1
            sleep(1)
    except docker.errors.APIError as error:
        print(error)
assert (postgresup)