from pydantic import BaseModel
from typing import List

class MilvusResult(BaseModel):
    distance: float
    content: str

class MilvusSearchResponse(BaseModel):
    code: int
    data: List[MilvusResult]

class MyRecord(BaseModel):
    instruction: str
    input: str
    output: str

class MessageTurn(BaseModel):
    user: str
    assistant: str
