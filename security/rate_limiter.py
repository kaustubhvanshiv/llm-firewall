from time import time

REQUEST_LOG = {}

RATE_LIMIT = 10
WINDOW = 60


def is_rate_limited(client_ip):

    now = time()

    if client_ip not in REQUEST_LOG:
        REQUEST_LOG[client_ip] = []

    REQUEST_LOG[client_ip] = [
        t for t in REQUEST_LOG[client_ip]
        if now - t < WINDOW
    ]

    if len(REQUEST_LOG[client_ip]) >= RATE_LIMIT:
        return True

    REQUEST_LOG[client_ip].append(now)

    return False