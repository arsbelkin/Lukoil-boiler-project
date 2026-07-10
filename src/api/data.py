from pydantic import BaseModel


class BoilerData(BaseModel):
    inputHotTemp: float = 85.0
    inputColdTemp: float = 15.0
    outputTemp: float = 0
    waterLevel: float = 0
    valveHot: float = 50
    valveCold: float = 50
    valveOut: float = 50
    