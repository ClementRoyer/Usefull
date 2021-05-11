#!/usr/bin/env python3

# Author     : clement.royer@epitech.eu
# Descrption : Create new github repository

#   - Github API -> https://pygithub.readthedocs.io/en/latest/introduction.html
#   - argparse   -> https://pypi.org/project/argparse/
#   - requests
#   - JSON
#   - gitpython

# Args:
#   - name (string) -n
#   - description (string) -d
#   - --api_key | -k
#   - --private | -p
#   - --public (default)

# Token scope:
# - repo (to create private and public repository)

import subprocess
import requests
import argparse
import json
import git
import sys
import os

from dotenv import dotenv_values
from github import Github
from git import Repo
from utils import ask

class Repository:
    name = "",
    path = "",
    description = "",
    public = True,

class User:
    _profile = "",
    token = "",
    g = ""

def load_args(r):
    argparser = argparse.ArgumentParser(sys.argv[0], "Create and init github repository.")
    argparser.add_argument("--path", default="./", help="Current position path")
    argparser.add_argument("--name", "-n", default="", help="Repository name")
    argparser.add_argument("--description", "-d", default="", help="Repository description")
    argparser.add_argument("--private", "-p", action="store_true", default=False, help="Create private repository")
    argparser.add_argument("--public", action="store_true", default=False, help="Create public repository")
    args = argparser.parse_args()
    r.path = args.path
    r.name = args.name
    r.description = args.description
    r.public = args.private

def input_cli(r):
    if (r.name == None or len(r.name) == 0):
        r.name = ask("🤖 Repo name:\n-> ")
    if (r.description == None or len(r.description) == 0):
        r.description = ask("🤖 Repo description:\n-> ")

def load_env(r):
    config = dotenv_values()
    user = User()
    user.token = config['github_token']
    user.g = Github(user.token)
    user._profile = user.g.get_user()
    return user

def create_repo(user, repo):
    # ref https://docs.github.com/en/rest/reference/repos#create-a-repository-for-the-authenticated-user
    sPath = 'https://api.github.com/user/repos'
    headers = {'Authorization': 'token '+user.token,"accept": "application/vnd.github.v3+json"}
    body = '{"name": "'+repository.name+'", "private": '+ ('true' if repository.public else 'false') + '}'

    r = requests.post(sPath,headers=headers, data=body)
    if (r.status_code != 201):
        print(f'❌ Error {r.text}', r.status_code)
        sys.exit(84)
    print(f'✔ {repository.name} created.')
    r = r.json();
    git.Git(repo.path).clone(r['ssh_url']);
    print(f'✔ Clone: Done')

def init_repo(user, repo):
    r = requests.get('https://raw.githubusercontent.com/ClementRoyer/Usefull/master/template/markdown/basic-w-badge-template.md')
    f = open(repo.name+"/README.md", "x", encoding="utf-8")
    txt = r.text.replace('{{repo}}', repo.name)
    txt = txt.replace('{{description}}', repo.description)
    f.write(txt)
    f.close()
    print(f'✔ README created.')

def push_init(repository):
    repo = Repo(repository.name)
    repo.index.add('README.md')
    repo.index.commit(':rocket: Initial commit')
    origin = repo.remote(name='origin')
    origin.push()
    print(f'✔ Initial push: Done')

def run(user, repository):
    create_repo(user, repository)
    init_repo(user, repository)
    push_init(repository)

def exit():
    print('\n🤖 Bye')
    os._exit(0)

if __name__ == '__main__':
    try:
        repository = Repository()
        load_args(repository)
        input_cli(repository)
        user = load_env(repository)
        run(user, repository)
        sys.exit()
    except KeyboardInterrupt:
        exit()
    except SystemExit:
        exit()
