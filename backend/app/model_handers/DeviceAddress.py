from typing import List
from .. import models

class CreateT:
    def __init__(self, address : str) -> None:
        self.address = address
async def create( dto : CreateT) -> models.DeviceAddress:
    return await models.objects.get_or_create( models.DeviceAddress , address = dto.address )

async def get_by_id( id : int ) -> models.DeviceAddress:
    return await models.objects.get( models.DeviceAddress , id = id )
    
async def get_all() -> List[models.DeviceAddress]:
    return list(models.DeviceAddress.select())