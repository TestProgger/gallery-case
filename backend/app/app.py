from fastapi import FastAPI 
from .middlware import pqt_to_list
from json import dump
app = FastAPI()


@app.get("/")
def plug():
    l = pqt_to_list('./userdata1.parquet')
    
    with open('test.json' , "w") as wt:
        dump( l , wt )
