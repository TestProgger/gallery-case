from typing import List
from .. import models
from pydantic import BaseModel

class OUI(BaseModel):
    oui : str
class CreateT(BaseModel):
    name :  str
    ouis : List[OUI]

async def create( dto : CreateT) -> models.Vendor:
    vendor = await models.objects.create( models.Vendor , name = dto.name )
    for oui in dto.ouis:
        models.objects.create( models.OUI , oui = oui.oui , vendor = vendor )
    return vendor

async def delete( id : int ) -> models.Vendor:
    obj = await models.objects.get( models.Vendor , id = id)
    return await models.objects.delete(obj)

async def get_by_id( id : int ) -> models.Vendor:
    return await models.objects.get( models.Vendor , id = id )

async def get_by_oui( oui : str ) -> models.Vendor:
    v_oui = await models.objects.get(models.OUI ,  oui = oui)
    return v_oui.vendor
    
async def get_all() -> List[models.Vendor]:
    return list(models.Vendor.select())