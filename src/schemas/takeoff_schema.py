from pydantic import BaseModel, Field, NonNegativeInt, ConfigDict


class TakeoffSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')
    target_altitude: NonNegativeInt = Field(..., le=50)