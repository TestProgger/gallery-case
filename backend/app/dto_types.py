from pydantic import BaseModel , validator , ValidationError
import re


class DeviceInfoDTO(BaseModel):
    mac : str
    timestamp : str

    @validator('mac')
    def mac_validator(cls , v):
        if not re.fullmatch(r"[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}"):
            raise ValidationError(f" MAC is not valid : {v}")
        return v