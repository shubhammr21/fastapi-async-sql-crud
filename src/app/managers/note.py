from app.managers.base import BaseManager
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class NoteManager(BaseManager[Note, NoteCreate, NoteUpdate]):
    ...


note_manager = NoteManager(Note)
