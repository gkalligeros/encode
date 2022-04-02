# Encode assigment 

## Info

### External services required 

#### Redis https://hub.docker.com/_/redis 
#### pipenv https://pipenv.pypa.io/en/latest/


### Environmental Variables

```bash
REDIS_HOST        # Host of running redis instance
REDIS_USER        # Redis username 
REDIS_PASSWORD    # Redis password 
# Default values are working keys 
# the app will work without that but with the API limitation for anonymous users
# https://stackoverflow.com/questions/62586521/stack-exchange-api-with-curl-command
STACK_EXCHANGE_TOKEN
STACK_EXCHANGE_KEY
```

### How to run 
```bash
pipenv install 
pipenv shell 
uvicorn api.main:app --reload
```

