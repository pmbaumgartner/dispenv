from typing import NewType, Optional
from pydantic import BaseModel

URLString = NewType("URLString", str)


class Options(BaseModel):
    build_image: bool


class EnvData(BaseModel):
    python_version: str
    folder_name: str
    environment_type: str
    environment_name: str
    requirements_txt_gist: Optional[URLString]
    options: Optional[Options]
