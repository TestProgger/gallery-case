from json import load
from os import times
from fastapi import FastAPI 
from .model_handers import DeviceInfo , Vendor
from .dto_types import DeviceInfoDTO

app = FastAPI()


@app.get("/{id}")
async def plug(id : int):
    return await DeviceInfo.get_by_id(id)



@app.get("/create_device")
async def create_device(dev :  DeviceInfoDTO):
    return await DeviceInfo.create( DeviceInfo.CreateT( mac = dev.mac , timestamp=dev.timestamp ) )