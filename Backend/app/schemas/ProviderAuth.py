from pydantic import BaseModel

class ProviderAuth(BaseModel):
    token: str