from datetime import datetime

from fastapi import FastAPI, Depends

from utils.api_client import get_api_client

app = FastAPI()


@app.get("/api/v1/stackstats")
async def root(since: datetime, until: datetime, client=Depends(get_api_client)):
    return client.final_data(since=since, until=until)
