from pydantic import BaseModel


convert_map = {
    "inputHotTemp": "InputTempHot",
    "inputColdTemp": "InputTempCold",
    "outputTemp": "OutputTemp",
    "waterLevel": "WaterLevel",
    "valveHot": "ValveHotIn",
    "valveCold": "ValveColdIn",
    "valveOut": "ValveOut",
}


class SetValueDTO(BaseModel):
    name: str
    value: float

    def get_name(self):
        return convert_map.get(self.name, "")
