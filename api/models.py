from typing import Optional
from pydantic import BaseModel, Field


class Character(BaseModel):
    """Based on https://github.com/Apexal/wrathspriter/blob/master/src/interfaces/character.ts"""

    name: str
    backstory: str


class AudioBody(BaseModel):
    base64EncodedAudio: str


class ImageBody(BaseModel):
    base64EncodedImage: str
