import random
import string

import requests
from invoke import task

import fmt


@task
def k8s_generate_tokens(c, number=20):
    """Generates random tokens"""

    fmt.print_title(f"generating {number} tokens")

    letters = string.ascii_lowercase + string.digits
    for _ in range(number):
        value = ''.join(random.choice(letters) for i in range(36))

        data = {
            'value': value,
            'is_available': True
        }
        response = requests.post('http://127.0.0.1/tokens', json=data)
        response.raise_for_status()

    fmt.print_title("done!")


@task
def k8s_pop_token(c):
    """Returns a k8s token from the pool"""

    response = requests.put('http://127.0.0.1/tokens/pop')
    response.raise_for_status()

    token = response.json()
    fmt.print_title("token:", str(token))


@task
def k8s_available_tokens(c):
    """Shows available tokens"""

    response = requests.get('http://127.0.0.1/tokens')
    response.raise_for_status()

    tokens = response.json()
    for token in tokens:
        print(token['value'], token['is_available'])

    fmt.print_title(f"number of tokens available: {len(tokens)}")
