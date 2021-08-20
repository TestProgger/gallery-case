from pydantic import BaseModel , validator , ValidationError
import re


class DeviceInfoDTO(BaseModel):
    mac : str
    timestamp : str

    @validator('mac')
    def mac_validator(cls , v : str):
        if not re.fullmatch(r"[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}" , v.lower()):
            raise ValidationError(f" MAC is not valid : {v}")
        return v