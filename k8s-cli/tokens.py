import random
import string

import requests
from colorama import Back, Fore, Style
from invoke import task


def _print_title(text: str):
    print(Back.YELLOW + Fore.BLACK + text + Style.RESET_ALL)


@task
def k8s_generate_tokens(c, number=20):
    """Generates random tokens"""

    letters = string.ascii_lowercase + string.digits
    for _ in range(number):
        value = ''.join(random.choice(letters) for i in range(36))

        data = {
            'value': value,
            'is_available': True
        }
        response = requests.post('http://127.0.0.1/tokens', json=data)
        response.raise_for_status()


@task
def k8s_pop_token(c):
    """Returns a k8s token from the pool"""

    response = requests.put('http://127.0.0.1/tokens/pop')
    response.raise_for_status()

    token = response.json()
    print(token)


@task
def k8s_available_tokens(c):
    """Shows available tokens"""

    response = requests.get('http://127.0.0.1/tokens')
    response.raise_for_status()

    tokens = response.json()
    for token in tokens:
        print(token['value'], token['is_available'])

    _print_title(f"number of tokens available: {len(tokens)}")
