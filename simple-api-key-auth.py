from fastapi import FastAPI, HTTPException, Depends, Security, Header
from pydantic import BaseModel
from typing import Dict, Annotated
from fastapi.security import APIKeyHeader

app = FastAPI()

class Service(BaseModel):
    url: str
    status: str
    details: str = None    # non mandatory param

# my in memory database for now to hold service details
status_db: Dict[str, Service] = {}

Server_API_KEY = "01fb55b48cf7010ec7fd7f4c74b4c64192d2c471a28b66f55611615817d27805"
API_KEY_NAME = "FAST-API-KEY"
api_key_header= APIKeyHeader(name= API_KEY_NAME, auto_error=True)

def validate_api_key(incoming_api_key: str = Security(api_key_header)):   # ... Ellipsis object makes Header required, if missing then fastapi returns "422 Unprocessable Entity error"
    if incoming_api_key != Server_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return True


@app.get("/")
def root():
    return {"Welcome to FastAPI development."}

@app.post("/service/status")
async def send_status(payload: Service):
    status_db[payload.url] = payload
    return {"message": f"Status for {payload.url} updated successfully."}


@app.get("/service/status/all")
def get_status_all(auth: None = Security(validate_api_key)):
    return status_db

@app.get("/service/status")
async def get_status(service_url: str, auth: Annotated[None, Security(validate_api_key)]):
    if service_url in status_db:
        return status_db[service_url]
    else:
        raise HTTPException(status_code=404, detail=f"Service: {service_url} not found")
    

