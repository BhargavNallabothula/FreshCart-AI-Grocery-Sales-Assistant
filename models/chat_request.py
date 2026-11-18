from pydantic import BaseModel

class ChatRequestModel(BaseModel):
    user_message:str
    conv_id:str