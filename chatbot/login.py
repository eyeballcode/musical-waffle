import os
from ChatExchange6.chatexchange6.client import Client
from chatbot import Chatbot
from util import FileIO
import sys
import getpass


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def write_info_to_config(payload):
    FileIO.create_if_not_exist('config.json', filetype='json')
    json = FileIO.read_json('config.json')
    json = merge_two_dicts(payload, json)
    FileIO.write_json(jsondata=json, file='config.json')


def login_from_env():
    username = os.environ['CHATBOT_USERNAME']
    password = os.environ['CHATBOT_PASSWORD']
    if 'CHATBOT_SITE' in os.environ:
        site = os.environ['CHATBOT_SITE']
    else:
        site = 'stackexchange.com'
    if 'CHATBOT_ROOM' in os.environ:
        room = int(os.environ['CHATBOT_ROOM'])
    else:
        room = 1
    client = Client(email=username, password=password, host=site)
    client = 'a'
    write_info_to_config({'username': username, 'password': password, 'room': room, 'site': site})
    return Chatbot.Chatbot(client, room)


def can_login_from_env():
    return 'CHATBOT_USERNAME' in os.environ and 'CHATBOT_PASSWORD' in os.environ


def can_login_from_args():
    password_index, username_index = find_username_and_password()

    args_length = len(sys.argv)
    username_exists = args_length > username_index + 1
    password_exists = args_length > password_index + 1
    return not username_index == -1 and not password_index == -1 and username_exists and password_exists


def find_username_and_password():
    username_index = -1
    if '-u' in sys.argv:
        username_index = sys.argv.index('-u')
    elif '--username' in sys.argv:
        username_index = sys.argv.index('--username')
    password_index = -1
    if '-p' in sys.argv:
        password_index = sys.argv.index('-p')
    elif '--password' in sys.argv:
        password_index = sys.argv.index('--password')
    return password_index, username_index


def args_has(name):
    if name in sys.argv:
        return len(sys.argv) > sys.argv.index(name) + 1


def args_lookup(name):
    if args_has(name):
        return sys.argv[sys.argv.index(name) + 1]


def login_from_args():
    password_index, username_index = find_username_and_password()
    username = sys.argv[username_index + 1]
    password = sys.argv[password_index + 1]
    if args_has('--site'):
        site = args_lookup('--site')
    elif args_has('-s'):
        site = args_lookup('-s')
    else:
        site = 'stackexchange.com'
    if args_has('--room'):
        room = args_lookup('--room')
    elif args_has('-r'):
        room = args_lookup('-r')
    else:
        room = 1
    client = Client(host=site, email=username, password=password)
    write_info_to_config({'username': username, 'password': password, 'room': room, 'site': site})
    return Chatbot.Chatbot(client, room)


def can_login_from_config():
    if not FileIO.exists('config.json'):
        return False
    json = FileIO.read_json('config.json')
    return 'username' in json and 'password' in json


def login_from_config():
    if FileIO.exists('config.json'):
        json = FileIO.read_json('config.json')
        username = json['username']
        password = json['password']
        if 'site' in json:
            site = json['site']
        else:
            site = 'stackexchange.com'
        if 'room' in json:
            room = json['room']
        else:
            room = 1
        client = Client(host=site, email=username, password=password)
        write_info_to_config({'username': username, 'password': password, 'room': room, 'site': site})
        return Chatbot.Chatbot(client, room)


def login_on_the_spot():
    read = None
    if sys.version_info.major == 2:
        read = raw_input
    else:
        read = input
    username = read('Username: ')
    password = getpass.getpass('Password: ')
    site = read('Chat Site: ')
    room = read('Room ID: ')
    if site == '':
        site = 'stackexchange.com'
    if room == '':
        room = 1
    print(username)
    print(password)
    print(site)
    client = Client(host=site, email=username, password=password)
    write_info_to_config({'username': username, 'password': password, 'room': room, 'site': site})
    return Chatbot.Chatbot(client, room)
