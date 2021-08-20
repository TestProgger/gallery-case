from pydantic import BaseModel
from typing import Optional

class Create_T(BaseModel):
        mac : str
        timestamp :  str

class Update_T(BaseModel):
        id :  int
        mac : str
        timestamp : str
    
class Delete_T(BaseModel):
        id :  int 