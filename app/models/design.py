from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class DesignBase(BaseModel):
    name: str
    data: Dict[str, Any]

class DesignCreate(DesignBase):
    pass

class DesignUpdate(BaseModel):
    name: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class Design(DesignBase):
    id: str
    ownerId: str