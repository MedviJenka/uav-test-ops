from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat


class BeforeStartupChecklist(BaseModel):

    model_config = ConfigDict(extra='forbid')

    battery_health: Literal['not_healthy', 'healthy'] = Field(...,           description='')
    gps_connection: bool                              = Field(default=False, description='')
    controls:       Literal['error', 'free']          = Field(...,           description='')
    voltage:        NonNegativeFloat                  = Field(..., description='')
    amp:            NonNegativeFloat                  = Field(..., description='amperage')


class AfterStartupChecklist(BaseModel): ...


class BeforeTakeoffChecklist(BaseModel): ...


class AfterTakeoffChecklist(BaseModel): ...


class RouteChecklist(BaseModel): ...


class BeforeLandingChecklist(BaseModel): ...
