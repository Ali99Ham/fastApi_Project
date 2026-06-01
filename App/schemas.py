from pydantic import BaseModel

class newPost(BaseModel):
    title: str
    content: str
    
class postResponse(BaseModel):
    id: int
    title: str
    content: str    