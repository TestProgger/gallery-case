from random import choice
from typing import List
from .. import models , assistants
from . import Vendor 


class CreateT:
    def __init__(self , mac : str  , timestamp : str , bilboard_id : int ) -> None:
        self.mac = mac
        self.timestamp = timestamp
        self.bilboard_id = bilboard_id

async def create( dto : CreateT) -> models.DeviceInfo:
    oui = ":".join( dto.mac.split(":")[0:3] )
    vendor = await Vendor.get_by_oui(oui)
    if vendor:
        return await models.objects.create( 
                                            models.DeviceInfo , mac = dto.mac , timestamp = dto.timestamp , 
                                            vendor = vendor , bilboard_id=dto.bilboard_id
                                            )

async def delete( id : int ) -> models.DeviceInfo:
    obj = await models.objects.get( models.DeviceInfo , id = id)
    return await models.objects.delete(obj)

async def get_by_id( id : int ) -> models.DeviceInfo:
    return await models.objects.get( models.DeviceInfo , id = id )

async def get_all() -> List[models.DeviceInfo]:
    return list(models.DeviceInfo.select())

async def from_parquet(path_to_parquet : str) -> bool:
    print("## Loading data from " + path_to_parquet)
    data_list =  assistants.pqt_to_list(path_to_parquet)
    print("## Loaded " + path_to_parquet)
    b_ids = [
                1548 , 1549 , 1572 , 257, 258 , 
                259 , 260 , 261 , 262 , 263 , 
                264 , 267 , 265 , 266 , 2657 , 
                268 , 269 , 270 , 271 , 272 , 273 , 333 , 40 , 403
            ]
    for data in data_list:
        await create( CreateT( mac = data["Mac"] , timestamp = data["AddedOnDate"] , bilboard_id = choice(b_ids)) )
    return True

async def get_distinct_timestamps():
    timestamps =  await models.objects.execute( models.DeviceInfo.select(models.DeviceInfo.timestamp).distinct() )  
    return [ tm.timestamp for tm in timestamps ]

async def get_device_ids():
    ids = await models.objects.execute( models.DeviceInfo.select( models.DeviceInfo.bilboard_id ).distinct() )
    return [ id.bilboard_id for id in ids ]