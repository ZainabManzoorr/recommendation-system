from pydantic import BaseModel

class BodyInput(BaseModel):
  height: float
  weight: float
  chest: float
  waist: float
  hips: float
  shoulder: float
  sleeve: float