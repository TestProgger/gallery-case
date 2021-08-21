from typing import List
from .. import models , assistants
from . import Vendor , DeviceAddress


class CreateT:
    def __init__(self , mac : str  , timestamp : str , address:str) -> None:
        self.mac = mac
        self.timestamp = timestamp
        self.address = address
async def create( dto : CreateT) -> models.DeviceInfo:
    oui = ":".join( dto.mac.split(":")[0:3] )
    vendor = await Vendor.get_by_oui(oui)
    address , _ = await DeviceAddress.create( dto.address )
    if vendor:
        return await models.objects.create( models.DeviceInfo , mac = dto.mac , timestamp = dto.timestamp , vendor = vendor , address=address )

async def delete( id : int ) -> models.DeviceInfo:
    obj = await models.objects.get( models.DeviceInfo , id = id)
    return await models.objects.delete(obj)

async def get_by_id( id : int ) -> models.DeviceInfo:
    return await models.objects.get( models.DeviceInfo , id = id )

async def get_all() -> List[models.DeviceInfo]:
    return list(models.DeviceInfo.select())

async def from_parquet(path_to_parquet : str) -> bool:
    data_list =  assistants.pqt_to_list(path_to_parquet)

    for data in data_list:
        await create( CreateT( mac = data["Mac"] , timestamp = data["AddedOnDate"]) )
    return True