from pydantic import BaseModel, Field, field_validator
from typing import Literal


class UserMeasurement(BaseModel):
    user_id: str
    height: float = Field(..., gt=50, lt=300, description="Height in cm (50–300)")
    weight: float = Field(..., gt=10, lt=500, description="Weight in kg (10–500)")
    chest: float = Field(..., gt=10, lt=80, description="Chest in inches (10–80)")
    waist: float = Field(..., gt=10, lt=70, description="Waist in inches (10–70)")
    hips: float = Field(..., gt=10, lt=80, description="Hips in inches (10–80)")
    shoulder: float = Field(..., gt=10, lt=30, description="Shoulder width in inches (10–30)")
    sleeve: float = Field(..., gt=10, lt=40, description="Sleeve length in inches (10–40)")
    gender: Literal["male", "female"] = Field(..., description="Gender as string: 'male' or 'female'")
    
    def get_encoded_type(self):
        return 0 if self.gender == "male" else 1
    
    @field_validator(
        "height", "weight", "chest", "waist", "hips", "shoulder", "sleeve"
    )
    def must_be_positive(cls, v, info):
        if v <= 0:
            raise ValueError(f"{info.field_name} must be greater than zero.")
        return v

