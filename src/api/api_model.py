from pydantic import BaseModel


class SetValueDTO(BaseModel):
    name: str
    value: float
