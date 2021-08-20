from fastapi import FastAPI 
app = FastAPI()


@app.get("/")
def plug():
    pass
