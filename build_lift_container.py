#Build Lift App Container
import argparse
from getpass import getpass

import docker

my_parser = argparse.ArgumentParser()
my_parser.add_argument('--repo', action='store', type=str, required=True)
my_parser.add_argument('--user', action='store', type=str, required=True)
my_parser.add_argument('--passwd', action='store', type=str, required=True)

args = my_parser.parse_args()

#Define Docker variables
tag="latest"
repo=args.repo
client = docker.from_env()
lift_app = client.images.get("liftapp_web")
client.login(username=args.user, password=args.passwd)
lift_app.tag(repo, tag=tag)
for line in client.images.push(repo, stream=True, decode=True):
    print(line)
