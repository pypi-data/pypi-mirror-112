from getpass import getpass
import json
import pyDes
import requests
import time

from kortical.helpers.print_helpers import printc, Colour


session = requests.session()
project_url = None
website_url = None
email = None
password = None


def get_website_url():
    return website_url


def get_project_url():
    return project_url


def web_call(function, url, *args, throw=True, **kwargs):
    retries = 3
    response = None
    url = get_project_url() + url
    while not response:
        try:
            response = function(url, *args, **kwargs)
            if response.status_code == 401:
                raise ConnectionRefusedError("You are not logged in. This may be becasue you accessed the system via the UI")
            if throw and response.status_code not in [200, 204]:
                raise Exception(f"POST Request [{url}] failed with status code [{response.status_code}]\n\n{response.content.decode()}")
            return response
        # Our nginx controller may have caused a config reload, this drops existing connections
        # and so we need to retry here in the case of a connection error
        except requests.exceptions.ConnectionError as e:
            if retries <= 0:
                raise e
            printc(Colour.FAIL, f"Retrying due to connection drop")
            retries -= 1
            time.sleep(1)
        except ConnectionRefusedError as e:
            if retries <= 0:
                raise e
            retries -= 1
            # backoff
            sleep = 60 * (3-retries)
            printc(Colour.FAIL, f"Retrying after [{sleep}] seconds, as user has been logged out.")
            time.sleep(sleep)
            # login
            _login()

def get(url, *args, throw=True, **kwargs):
    return web_call(session.get, url, *args, throw=throw, **kwargs)


def post(url, *args, throw=True, **kwargs):
    return web_call(session.post, url, *args, throw=throw, **kwargs)


def set_url(url):
    global project_url
    global website_url
    # check and fix the url
    if not url.startswith("https://"):
        url = "https://" + url
    project_url = url
    slash_index = project_url[9:].find('/')
    website_url = project_url[: 9 + slash_index]


def init(url, credentials=None):
    global project_url
    global website_url
    global email
    global password

    if credentials is not None:
        email = credentials['email']
        password = credentials['password']
        set_url(url)
        _login()
        return

    if project_url is not None and url in project_url:
        return None

    # get user details from disk or command line
    k = pyDes.des(b"SUPRSAFE", pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    try:
        with open("kortical_credentials", 'rb') as f:
            content = k.decrypt(f.read())
            content = json.loads(content)
            email = content['email']
            password = content['password']
    except:
        print(f"Please enter kortical login email:")
        email = input()
        password = getpass()
        print(f"Would you like to save credentials to this machine? y/n")
        save = input()
        if save[0].lower() == 'y':
            with open("kortical_credentials", 'wb') as f:
                content = {
                    'email' :email,
                    'password': password
                }
                content = json.dumps(content)
                content = k.encrypt(content)
                f.write(content)

    set_url(url)
    _login()


def _login():
    global project_url
    global website_url
    global email
    global password

    form = {'email': email, 'password': password}
    retries = 3
    response = None
    while not response:
        try:
            response = session.post(get_website_url(), data=form)
            if response.status_code != 200:
                raise Exception(f"Request login failed with status code [{response.status_code}]\n\n{response.content.decode()}")
        # Our nginx controller may have caused a config reload, this drops existing connections
        # and so we need to retry here in the case of a connection error
        except requests.exceptions.ConnectionError as e:
            if retries <= 0:
                raise e
            printc(Colour.FAIL, f"Retrying due to connection drop")
            retries -= 1
            time.sleep(1)

    post('/login', data=form)