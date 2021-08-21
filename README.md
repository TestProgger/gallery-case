# GALLERY CASE

## Python Enviroment BACKEND

#### Installing Dependencies:

```bash
    python -m pip install asyncio uvicorn fastapi peewee peewee_async aiopg asyncio pandas
```

#### config.json in backend directory

```bash
    {
        "database" : "PTO_YONVOS",
        "user" : "postgres" ,
        "password" : "ros1337ini" ,
        "host"  : "localhost" ,
        "port" : 5432 ,
        "max_connections" : 20
    }
```

#### Starting Back-End

```bash
    python ./backend/main.py
```
