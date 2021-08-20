from fastapi import FastAPI 
from .model_handers import BilboardInfo
app = FastAPI()


@app.get("/{id}")
async def plug(id : int):
    return await BilboardInfo.get_by_id(id)
