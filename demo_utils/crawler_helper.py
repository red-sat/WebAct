import random


def get_random_link(links):
    if len(links) == 0:
        return None
    random_link = random.choice(links)
    links.remove(random_link)
    return random_link