from pydantic import BaseModel

class ChatResponse(BaseModel):
    ai_reply:dict   #here we took dict because to support for json response  