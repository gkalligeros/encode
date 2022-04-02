import datetime
from os import cpu_count, getenv, path

STACK_EXCHANGE_HOST = "https://api.stackexchange.com/"
STACK_EXCHANGE_SITE = "stackoverflow"
STACK_EXCHANGE_ANSWERS_ENDPOINT = "/2.3/answers"
STACK_EXCHANGE_TOKEN = getenv("STACK_EXCHANGE_TOKEN", "zosxIUpzRqCFbn87TPMynQ))")
STACK_EXCHANGE_KEY = "Ohq8Gend55wB49aAXyZnpw(("

REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_USER = getenv("REDIS_USER", None)
REDIS_PASSWORD = getenv("REDIS_PASSWORD", None)

CACHE_LIFETIME = datetime.timedelta(days=1)
