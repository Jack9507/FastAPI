from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

app = FastAPI()

class Service(BaseModel):
    url: str
    status: str
    details: str = None    # non mandatory param

# my in memory database for now to hold service details
status_db: Dict[str, Service] = {}

@app.get("/")
def root():
    return {"Welcome to FastAPI development."}

@app.post("/service/status")
async def send_status(payload: Service):
    status_db[payload.url] = payload
    return {"message": f"Status for {payload.url} updated successfully."}


@app.get("/service/status/all")
def get_status_all():
    return status_db

@app.get("/service/status")
async def get_status(service_url: str):
    if service_url in status_db:
        return status_db[service_url]
    else:
        raise HTTPException(status_code=404, detail=f"Service: {service_url} not found")
    

