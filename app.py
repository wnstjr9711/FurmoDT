# -*-coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI
from routes import auth, websocket
from database.conn import SQLAlchemy


db = SQLAlchemy()
db.create_table()

app = FastAPI()
app.include_router(auth.router)
app.include_router(websocket.router)

if __name__ == "__main__":
    uvicorn.run('app:app', host='0.0.0.0', reload=True)