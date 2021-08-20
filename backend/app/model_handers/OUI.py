from typing import List
from .. import models
from pydantic import BaseModel

class CreateT:
    oui : str
async def create( dto : CreateT) -> models.OUI:
    return await models.objects.create( models.OUI , oui = dto.oui )

async def get_by_id( id : int ) -> models.OUI:
    return await models.objects.get( models.OUI , id = id )
    
async def get_all() -> List[models.OUI]:
    return list(models.OUI.select())