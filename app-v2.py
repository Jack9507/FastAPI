# adding LRU Cache to handle in memory database
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from collections import OrderedDict
import os

app = FastAPI()

class Service(BaseModel):
    url: str
    status: str
    details: str = None    # non mandatory param

MAX_CACHE_SIZE = int(os.getenv('MAX_CACHE_SIZE', 10000)) #default is 10000

class LRUCache():
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str):
        if key not in self.cache:
            return None
        #move to end to mark it as recently used
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: str, value: Service):
        '''
        insert or update element in cache, remove LRU item if cache is full
        '''
        if key not in self.cache:
            #insert as its a fresh entry, but first check the cache size
            if len(self.cache) >= self.capacity:
                #remove the LRU item from cache 
                self.cache.popitem(last=False)
            self.cache[key]= value
        else:
            # update the item and move it to end to mark it as recently used
            self.cache[key] = value
            self.cache.move_to_end(key)
    
    def get_all(self):
        return dict(self.cache)

    def delete(self, key: str):
        return self.cache.pop(key, None)

# Initialize LRU Cache
status_db = LRUCache(MAX_CACHE_SIZE)

# my in memory database for now to hold service details
# status_db: Dict[str, Service] = {}

@app.get("/")
def root():
    return {"Welcome to FastAPI, please use /docs path to check the available API's"}

@app.get("/ping")
def ping():
    return {"response": "pong"}

@app.post("/api/v1/service/status")
async def send_status(payload: Service):
    status_db.put(payload.url, payload)
    return {"message": f"Status for {payload.url} updated successfully.", "payload": dict(payload)}

@app.get("/api/v1/service/status/all")
def get_status_all():
    return status_db.get_all()

@app.get("/api/v1/service/status")
async def get_status(service_url: str):
    service = status_db.get(service_url)
    if service:
        return service
    else:
        raise HTTPException(status_code=404, detail=f"Service: {service_url} not found.")
    

# Health endpoint for mointoring
@app.get("/api/v1/health")
async def health_check():
    cache_size = len(status_db.cache)
    return {
        "API status": "healthy",
        "cache size": cache_size,
        "max cache size": MAX_CACHE_SIZE,
        "memory usage %": (cache_size/MAX_CACHE_SIZE) * 100,
        "will evict on next add": cache_size >= MAX_CACHE_SIZE
    }

@app.delete("/api/v1/delete")
def delete(self, key: str):
    deleted_item = status_db.delete(key)
    if deleted_item:
        return deleted_item
    else:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        raise HTTPException(404, f"Item: {key} not found.")
