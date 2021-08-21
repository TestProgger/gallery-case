from json import load
from os import times
from fastapi import FastAPI 
from .model_handers import DeviceInfo , Vendor
from .dto_types import DeviceInfoDTO

from json import load

app = FastAPI()


@app.get("/init_db")
async def init_db():
    with open("./oui_data_m1.json" , "r") as jr:
        vendors = load(jr)

    vendor_names = list(vendors.keys())

    for vendor_name  in vendor_names:
        await Vendor.create(
            Vendor.CreateT(
                name = vendor_name,
                ouis = [ Vendor.OUI( oui )  for oui in vendors[vendor_name]['macAdresses'] ],
                activity_types= [ Vendor.ActivityType( at )  for at in vendors[vendor_name]['activityType'] ]
            )
        )
    
    await DeviceInfo.from_parquet( './month=2020-11.parquet' )
    await DeviceInfo.from_parquet( './month=2021-6.parquet' )
    

    return {'a' : 111}

@app.post("/create_device")
async def create_device(dev :  DeviceInfoDTO):
    return await DeviceInfo.create( DeviceInfo.CreateT( mac = dev.mac , timestamp=dev.timestamp ) )