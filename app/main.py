from fastapi import FastAPI
from .database import get_db
from .routers import link, user, auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins= ["* "]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine) #used when we are not using alembic to generate tables

app.include_router(link.app)
app.include_router(user.app)
app.include_router(auth.app)

#Root
@app.get("/")
async def root():
    return {"message": "The API is Running"}


