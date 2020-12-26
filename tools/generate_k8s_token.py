
import string
import random

# [a-z0-9]{6}.[a-z0-9]{16}"

def generate_token():
    letters = string.ascii_lowercase + string.digits
    part1 = ''.join(random.choice(letters) for i in range(6))
    part2 = ''.join(random.choice(letters) for i in range(16))

    print(f"{part1}.{part2}")

if __name__ == "__main__":
    generate_token()