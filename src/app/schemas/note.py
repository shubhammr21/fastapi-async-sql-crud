from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Shared properties
class NoteBase(BaseModel):
    title: str | None = None
    content: str | None = None


# schema for creating a note
class NoteCreate(NoteBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "Sample title",
                "content": "Sample content",
            },
        },
    )


# Properties to receive on Note update
class NoteUpdate(NoteBase):
    pass


# Properties shared by models stored in DB
class NoteInDBBase(NoteBase):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class NoteSchema(NoteInDBBase):
    pass


# Properties properties stored in DB
class NoteInDB(NoteInDBBase):
    pass
