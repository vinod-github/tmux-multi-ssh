#!/usr/bin/env python
# coding: utf-8
from os import system

user = "myuser"
password = "mypassword"

HOSTS = {
    'mongo' : 'mongo.vinod.local',
    'flask': 'flask.vinod.local',
    'redis': 'redis.vinod.local',
    'kafka': 'kafka.vinod.local'
}

SESSION_NAME = 'myserver'


def tmux(command):
    system('tmux %s' % command)


def tmux_shell(command):
    tmux('send-keys "%s" "C-m"' % command)


def create_session():
    # Kill old session with same name

    session = tmux('kill-session -t {}'.format(SESSION_NAME))
    tmux('new-session -d -s {}'.format(SESSION_NAME))


for index, key in enumerate(HOSTS):

    if index != 0:
        # first window is already created while starting new session
        tmux('new-window')

    tmux('select-window -t {}'.format(index))
    tmux_shell('sshpass -p {} ssh -o StrictHostKeyChecking=no {}@{}'.format(password, user,
                                                                            HOSTS.get(key)))
    tmux('rename-window "{}"'.format(key))
    print "created window for {}".format(HOSTS.get(key))

tmux('select-window -t 0')
