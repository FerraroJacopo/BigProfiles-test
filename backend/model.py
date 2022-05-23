from pydantic import BaseModel, EmailStr, Field, validator

class DataSchema(BaseModel):
    payload: str = Field(...)
    key: int = Field(..., gt=0, lt=7)

    @validator('payload')
    def payload_lenght(cls, v):
        if len(v) > 255 or len(v) < 10:
            raise ValueError('Payload length should be between 10 and 255')
        return v

def ResponseModel(data, metrics, message, status_code=200):
    d = {}

    if metrics:
        d['values'] = metrics

    d["logs"] = data,
    d["status_code"] = status_code,
    d["message"] = message,

    return d
