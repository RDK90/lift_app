import docker
from time import sleep

client = docker.from_env()
limit = 10
num_of_tries = 1
check_message = "database system is ready to accept connections\\n'"
while num_of_tries < limit:
    try:
        postgres = client.containers.get('postgres')
        postgres_logs = postgres.logs(tail=1)
        message = str(postgres_logs).split("LOG:  ")
        if message[1] == check_message:
            print("Postgres is ready")
            break
        else:
            print("Attempt number: " + str(num_of_tries) + " out of: " + str(limit))
            num_of_tries += 1
            sleep(1)
    except docker.errors.APIError as error:
        print(error)