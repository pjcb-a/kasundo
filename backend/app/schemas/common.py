from pydantic import BaseModel


class ORMBaseSchema(BaseModel):
    class Config:
        from_attributes = True



class MessageResponse(BaseModel):
    message: str


class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int