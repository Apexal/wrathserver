from typing import List, Optional
from pydantic import BaseModel, Field


class SoundEffect(BaseModel):
    name: Optional[str]
    base64EncodedAudio: str


class Vector2(BaseModel):
    x: int
    y: int


class BodyCollider(BaseModel):
    size: Vector2
    position: Vector2


class HitCollider(BaseModel):
    isEnabled: bool
    size: Optional[Vector2]
    position: Optional[Vector2]


class PoseAngle(BaseModel):
    poseIndex1: int
    poseIndex2: int
    poseIndex3: int
    angleMin: int
    angleMax: int


class AnimationFrame(BaseModel):
    base64EncodedImage: str
    pose: Optional[List[PoseAngle]]
    hitCollider: HitCollider
    bodyCollider: BodyCollider
    durationInS: float


class CharacterAction(BaseModel):
    name: str
    type: str
    animation: List[AnimationFrame]
    soundEffect: Optional[SoundEffect]


class SchoolProgram(BaseModel):
    id: str
    name: str
    backstory: str
    actionTemplates: List[CharacterAction]


class StateSoundEffects(BaseModel):
    hurt: List[SoundEffect]
    enter: List[SoundEffect]
    win: List[SoundEffect]
    lose: List[SoundEffect]


class StateAnimations(BaseModel):
    idle: List[AnimationFrame]
    enter: List[AnimationFrame]
    walk: List[AnimationFrame]
    dash: List[AnimationFrame]
    jump: List[AnimationFrame]
    crouch: List[AnimationFrame]
    block: List[AnimationFrame]
    grappled: List[AnimationFrame]
    hurt: List[AnimationFrame]
    win: List[AnimationFrame]
    lose: List[AnimationFrame]


class CharacterBase(BaseModel):
    """Based on https://github.com/Apexal/wrathspriter/blob/master/src/interfaces/character.ts"""

    name: str
    backstory: str
    actions: List[CharacterAction]
    major: Optional[SchoolProgram]
    minor: Optional[SchoolProgram]
    stateSoundEffects: StateSoundEffects
    stateAnimations: StateAnimations


class CharacterOut(CharacterBase):
    id: str


class AudioBody(BaseModel):
    base64EncodedAudio: str


class PoseLandmark(BaseModel):
    x: int
    y: int
    z: int


class ImageBodyBase(BaseModel):
    base64EncodedImage: str


class ImageBodyIn(ImageBodyBase):
    normalizedPoseLandmarks: List[PoseLandmark]


class ImageBodyOut(ImageBodyBase):
    pass
