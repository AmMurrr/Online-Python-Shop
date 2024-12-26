from pydantic import BaseModel, Field, validator
from typing import List, Optional, ClassVar
from datetime import datetime

# Base Config
class BaseConfig:
    from_attributes = True


class ItemBase(BaseModel):
    item_name: str
    item_category: str


