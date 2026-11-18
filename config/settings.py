from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str 
    DEFAULT_LLM: str 
    DEFAULT_OPENAI_MODEL: str 
    DEFAULT_ANTHROPIC_MODEL: str 

    model_config={

        "env_file":".env"
    }

settings=Settings()






