from pydantic import BaseModel, ConfigDict

class Car(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    brand: str
    model: str
    year: int
    motor_id: int