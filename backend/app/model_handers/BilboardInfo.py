from typing import List
from .. import models
from pydantic import BaseModel


class CreateT(BaseModel):
    mac  : str
    timestamp :  str
async def create( dto : CreateT) -> models.BilboardInfo:
    return await models.objects.create( models.BilboardInfo , mac = dto.mac , timestamp = dto.timestamp )

class UpdateT(BaseModel) :
    id : int
    mac : str
    timestamp : str
async def update( dto : UpdateT ) -> models.BilboardInfo:
    obj = await models.objects.get( models.BilboardInfo ,  id = dto.id )
    obj.mac = dto.mac
    obj.timestamp = dto.timestamp
    return await models.objects.update(obj)

async def delete( id : int ) -> models.BilboardInfo:
    obj = await models.objects.get( models.BilboardInfo , id = id)
    return await models.objects.delete(obj)

async def get_by_id( id : int ) -> models.BilboardInfo:
    return await models.objects.get( models.BilboardInfo , id = id )
    
async def get_all() -> List[models.BilboardInfo]:
    return list(models.BilboardInfo.select())