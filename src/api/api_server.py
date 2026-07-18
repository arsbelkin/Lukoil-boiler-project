from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from opc import OPCBoilerClient

from pathlib import Path

client = OPCBoilerClient()
BASE_DIR = Path(__file__).resolve().parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    client.connect()
    yield
    client.disconnect()


app = FastAPI(lifespan=lifespan)

app.mount("/ui", StaticFiles(directory=BASE_DIR / "ui"), name="ui")


from .controllers import router

app.include_router(router)
