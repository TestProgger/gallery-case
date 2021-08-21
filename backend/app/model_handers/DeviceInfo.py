from random import choice
from typing import List

from pydantic.schema import model_schema
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

async def get_devices(limit: int = 100 , offset :int = 0):
    devs = await models.objects.execute(
        models.DeviceInfo.select( models.DeviceInfo.mac , models.DeviceInfo.timestamp , models.DeviceInfo.bilboard_id , models.DeviceInfo.vendor  )
                        .limit( limit )
                        .offset( offset )
    )
    return [
        { 
            "timestamp" : d.timestamp , 
            "mac" : d.mac  , 
            "vendor" : d.vendor , 
            "bilboard_id" : d.bilboard_id
        }  
        for d in devs
    ]

async def get_number_devices_with_timestamp():
    timestamps =  await get_distinct_timestamps()
    response = dict()
    for timestamp in timestamps:
        r = await models.objects.execute(models.DeviceInfo.select( models.DeviceInfo.id ).where(models.DeviceInfo.timestamp == timestamp))
        response[str(timestamp)] = { "ftime" : timestamp.strftime("%a,%b,%Y-%m-%d,%H:%M%S") , "count" : len(r)} 
    return response

async def get_devices_by_timestamp(timestamp :  str, limit: int = 100 , offset :int = 0 ):
    devs = await models.objects.execute( models.DeviceInfo.select( models.DeviceInfo.mac , models.DeviceInfo.vendor , models.DeviceInfo.bilboard_id).where(models.DeviceInfo.timestamp == timestamp).limit(limit).offset(offset) )
    return [ { "vendor" : dev.vendor , "mac" : dev.mac  , "bilboard_id" : dev.bilboard_id} for dev in devs ]

async def get_devices_by_vendor_id(vendor_id : int , limit: int = 100 , offset :int = 0 ):
    vendor = await models.objects.get(models.Vendor , id  = vendor_id )
    devs = await models.objects.execute( 
        models.DeviceInfo.select( models.DeviceInfo.mac , models.DeviceInfo.timestamp , models.DeviceInfo.bilboard_id)
                        .where(models.DeviceInfo.vendor == vendor)
                        .limit(limit)
                        .offset(offset) 
                        )
    return [ { "timestamp" : dev.timestamp , "mac" : dev.mac  , "bilboard_id" : dev.bilboard_id} for dev in devs ]

async def get_devices_by_bilboard_id( bilboard_id : int ,  limit: int = 100 , offset :int = 0 ):
    devs = await models.objects.execute( 
        models.DeviceInfo.select( models.DeviceInfo.mac , models.DeviceInfo.timestamp , models.DeviceInfo.vendor)
        .where(models.DeviceInfo.bilboard_id == bilboard_id)
        .limit(limit)
        .offset(offset) 
        )
    return [ { "timestamp" : dev.timestamp , "mac" : dev.mac  , "vendor" : dev.vendor} for dev in devs ]

async def get_devices_by_weekday(weekday: int , limit: int = 100 , offset :int = 0  ):
    timestamps = await get_distinct_timestamps()
    valid_tmstp = [ timestamp for timestamp  in timestamps if int(timestamp.isocalendar().weekday) == weekday]

    d_limit = limit // len(valid_tmstp)
    devs = [] 
    for tmp in valid_tmstp:
        tmp_d = await models.objects.execute( 
            models.DeviceInfo.select(models.DeviceInfo.mac , models.DeviceInfo.timestamp , models.DeviceInfo.bilboard_id , models.DeviceInfo.vendor)
                            .where( models.DeviceInfo.timestamp == tmp )
                            .limit(d_limit)
                            .offset(offset)
        )
        devs += [ { "timestamp" : d.timestamp , "mac" : d.mac  , "vendor" : d.vendor , "bilboard_id" : d.bilboard_id}  for d in tmp_d ] 

    return devs

async def get_number_devices_by_weekday(weekday: int):
    timestamps = await get_distinct_timestamps()
    valid_tmstp = [ timestamp for timestamp  in timestamps if int(timestamp.isocalendar().weekday) == weekday]

    devs = dict()
    for tmp in valid_tmstp:
        tmp_d = models.DeviceInfo.select( models.DeviceInfo.id )\
                .where( models.DeviceInfo.timestamp == tmp )\
                .count()
        
        devs[str( tmp )] = tmp_d
    return devs
