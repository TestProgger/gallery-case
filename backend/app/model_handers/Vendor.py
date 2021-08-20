from typing import List
from .. import models
from pydantic import BaseModel


class CreateT(BaseModel):
    oui  : str
    name :  str
async def create( dto : CreateT) -> models.Vendor:
    return await models.objects.create( models.Vendor , oui = dto.oui , name = dto.name )

class UpdateT(BaseModel) :
    id : int
    oui : str
    name : str
async def update( dto : UpdateT ) -> models.Vendor:
    obj = await models.objects.get( models.Vendor ,  id = dto.id )
    obj.oui = dto.oui
    obj.name = dto.name
    return await models.objects.update(obj)

async def delete( id : int ) -> models.Vendor:
    obj = await models.objects.get( models.Vendor , id = id)
    return await models.objects.delete(obj)

async def get_by_id( id : int ) -> models.Vendor:
    return await models.objects.get( models.Vendor , id = id )

async def get_by_oui( oui : str ) -> models.Vendor:
    return await models.objects.get( models.Vendor ,  oui = oui )
    
async def get_all() -> List[models.Vendor]:
    return list(models.Vendor.select())