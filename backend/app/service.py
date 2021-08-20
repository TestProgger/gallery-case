from peewee import TimestampField
from peewee_async import delete
from .models import objects , BilboardInfo
from .types.BilboardInfoTypes import Create_T , Delete_T , Update_T


class BilboardInfo:
    async def create( dto :  Create_T ):
        return await objects.create( BilboardInfo , **dto )
    
    async def get( id : int ):
        return await objects.get( BilboardInfo , id = id )
    
    async def get_all():
        return await objects.get(BilboardInfo)

    async def update( dto : Update_T ):
        obj = await objects.get(BilboardInfo , id = dto.id)
        obj.mac = dto.mac
        obj.timestamp = dto.timestamp
        return await objects.update(obj)

    async def delete( dto : Delete_T ):
        obj = await objects.get(BilboardInfo , **dto)
        return await objects.delete(obj)


            
