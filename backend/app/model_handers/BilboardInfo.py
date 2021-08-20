from .. import models
from pydantic import BaseModel

class CreateT:
    mac  : str
    timestamp :  str
async def create( dto : CreateT):
    return await models.objects.create( models.BilboardInfo , mac = dto.mac , timestamp = dto.timestamp )

class UpdateT:
    id : int
    mac : str
    timestamp : str
async def update( dto : UpdateT ):
    obj = await models.objects.get( models.BilboardInfo ,  id = dto.id )
    obj.mac = dto.mac
    obj.timestamp = dto.timestamp
    return await models.objects.update(obj)

async def delete( id : int ):
    obj = await models.objects.get( models.BilboardInfo , id = id)
    return await models.objects.delete(obj)

async def get_by_id( id : int ):
    return await models.objects.get( models.BilboardInfo , id = id )
async def get_all():
    return await models.objects.get(models.BilboardInfo)