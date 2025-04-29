from pydantic import BaseModel, Field


class Background(BaseModel):
    name: str

class Settings(BaseModel):
    backgrounds: list[Background] = Field(default_factory=list)
