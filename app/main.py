from fastapi import FastAPI
from . import models
from .database import engine
from .routers import games, auth, sa, admin
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth.router)
# app.include_router(admin.router)
app.include_router(games.router)
