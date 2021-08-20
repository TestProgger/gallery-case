from typing import List
from .. import models
from . import Vendor
from pydantic import BaseModel


class CreateT:
    mac  : str
    timestamp :  str
async def create( dto : CreateT) -> models.DeviceInfo:
    oui = ":".join( dto.mac.split(":")[0:3] )
    vendor = await Vendor.get_by_oui(oui)
    return await models.objects.create( models.DeviceInfo , mac = dto.mac , timestamp = dto.timestamp , vendor = vendor )

async def delete( id : int ) -> models.DeviceInfo:
    obj = await models.objects.get( models.DeviceInfo , id = id)
    return await models.objects.delete(obj)

async def get_by_id( id : int ) -> models.DeviceInfo:
    return await models.objects.get( models.DeviceInfo , id = id )

async def get_all() -> List[models.DeviceInfo]:
    return list(models.DeviceInfo.select())