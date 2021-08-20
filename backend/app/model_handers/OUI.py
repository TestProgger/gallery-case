from typing import List
from .. import models

class CreateT:
    def __init__(self, oui) -> None:
        self.oui = oui
async def create( dto : CreateT) -> models.OUI:
    return await models.objects.create( models.OUI , oui = dto.oui )

async def get_by_id( id : int ) -> models.OUI:
    return await models.objects.get( models.OUI , id = id )
    
async def get_all() -> List[models.OUI]:
    return list(models.OUI.select())