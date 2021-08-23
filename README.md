# GALLERY CASE

## Python Enviroment BACKEND

#### Installing Dependencies:

```bash
    python -m pip install asyncio uvicorn fastapi peewee peewee_async aiopg asyncio pandas pyarrow
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

## Angular 12 Enviroment FRONTEND

#### Installing NodeJS(NPM) from site

#### Update npm packages

```bash
    cd frontend
    npm install
```

#### Starting Front-End

```bash
    ng serve --open
```