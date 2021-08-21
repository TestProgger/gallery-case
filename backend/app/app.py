from . import models
from fastapi import FastAPI 
from fastapi.responses import JSONResponse 
from fastapi.encoders import jsonable_encoder
from .model_handers import DeviceInfo , Vendor
from .dto_types import DeviceInfoDTO

app = FastAPI()


@app.get("/init_db")
async def init_db():
    # with open("./oui_data_m1.json" , "r") as jr:
    #     vendors = load(jr)

    # vendor_names = list(vendors.keys())

    # for vendor_name  in vendor_names:
    #     await Vendor.create(
    #         Vendor.CreateT(
    #             name = vendor_name,
    #             ouis = [ Vendor.OUI( oui )  for oui in vendors[vendor_name]['macAdresses'] ],
    #             activity_types= [ Vendor.ActivityType( at )  for at in vendors[vendor_name]['activityType'] ]
    #         )
    #     )
    
    await DeviceInfo.from_parquet( './month=2021-2.parquet' )
    # await DeviceInfo.from_parquet( './month=2021-6.parquet' )
    return {'a' : 111}

@app.post("/create_device")
async def create_device(dev :  DeviceInfoDTO):
    return await DeviceInfo.create( DeviceInfo.CreateT( mac = dev.mac , timestamp=dev.timestamp , bilboard_id=dev.bilboard_id ) )





@app.post("/get_info")
async def get_info():
    timestamps =  await DeviceInfo.get_distinct_timestamps()
    
    response = dict()
    
    for timestamp in timestamps:
        r = await models.objects.execute(models.DeviceInfo.select( models.DeviceInfo.id ).where(models.DeviceInfo.timestamp == timestamp))
        response[str(timestamp)] = len(r)
    
    return JSONResponse(content=response)
    