from typing import List
from .. import models

class OUI:
    def __init__(self , oui : str) -> None:
        self.oui = oui

class ActivityType:
    def __init__(self, name : str) -> None:
        self.name = name

class CreateT:
    def __init__(self, name : str , ouis : List[OUI] , activity_types : List[ActivityType]) -> None:
        self.name  = name
        self.ouis  = ouis
        self.activity_types  = activity_types

async def create( dto : CreateT) -> models.Vendor:
    vendor = await models.objects.create( models.Vendor , name = dto.name )
    if vendor:
        for oui in dto.ouis:
            await models.objects.get_or_create( models.OUI , oui = oui.oui , vendor = vendor )
        for at in dto.activity_types:
            s_at , created = await models.objects.get_or_create( models.ActivityType , name = at.name )
            vendor.activity_types.add(s_at)
    return vendor

async def delete( id : int ) -> models.Vendor:
    obj = await models.objects.get( models.Vendor , id = id)
    return await models.objects.delete(obj)

async def get_by_id( id : int ) -> models.Vendor:
    return await models.objects.get( models.Vendor , id = id )

async def get_by_oui( oui : str ) -> models.Vendor:
    try:
        v_oui = await models.objects.get(models.OUI ,  oui = oui)
        return v_oui.vendor
    except:
        return None
    
async def get_all() -> List[models.Vendor]:
    return list(models.Vendor.select())