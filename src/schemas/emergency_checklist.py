from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat


class EngineFailure(BaseModel): ...


class ElectricFailure(BaseModel): ...


class FireInFlight(BaseModel): ...
