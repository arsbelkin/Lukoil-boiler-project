from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import status

from opc import OPCBoilerClient
from .api_model import SetValueDTO

from pathlib import Path

app = FastAPI()

client = OPCBoilerClient()
client.connect()

convert_map = {
            "inputHotTemp": "InputTempHot",
            "inputColdTemp": "InputTempCold",
            "outputTemp": "OutputTemp",
            "waterLevel": "WaterLevel",
            "valveHot": "ValveHotIn",
            "valveCold": "ValveColdIn",
            "valveOut": "ValveOut",
        }

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/ui", StaticFiles(directory=BASE_DIR / "ui"), name="ui")


@app.get("/", response_class=FileResponse)
def index():
    html_path = BASE_DIR / "ui" / "index.html"
    return FileResponse(html_path, media_type="text/html")


@app.get("/api/v1/data")
def get_data():
    return client.get_data()


@app.post("/api/v1/data")
def set_value(dto: SetValueDTO):
    client.set_value(convert_map[dto.name], dto.value)
    return status.HTTP_200_OK
