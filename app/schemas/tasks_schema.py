from pydantic import BaseModel, Field


class Tasks(BaseModel):
    name: str = Field(min_length=3)
    discriptions:str = Field(min_length=3)
    date:str 