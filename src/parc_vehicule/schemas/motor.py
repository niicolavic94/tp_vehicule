from pydantic import BaseModel

class MotorSchema(BaseModel):
    power: int
    type: str
    consumption: float
    capacity_thermic: int
    consumption_electric: float
    capacity_electric: int
    