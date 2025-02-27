from pydantic import BaseModel

# First Message API Model
class FirstMessage(BaseModel):
    phone_number: str
    name: str
    interest: str