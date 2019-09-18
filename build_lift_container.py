#Build Lift App Container
import docker
from getpass import getpass

#Define Docker variables
tag="latest"
repo=docker_repo
client = docker.from_env()
lift_app = client.images.get("liftapp_web")
client.login(username=docker_username, password=docker_password)
lift_app.tag(repo, tag=tag)
for line in client.images.push(repo, stream=True, decode=True):
    print(line)
