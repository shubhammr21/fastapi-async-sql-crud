from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.managers.note import note_manager
from app.schemas.note import NoteCreate, NoteSchema, NoteUpdate

router = APIRouter()


@router.get(
    "",
    response_model=list[NoteSchema],
    status_code=status.HTTP_200_OK,
)
async def read_all_notes(session: AsyncSession = Depends(get_db)):
    notes = await note_manager.get_multi(session)
    return notes


@router.get(
    "/{note_id}",
    response_model=NoteSchema,
    status_code=status.HTTP_200_OK,
)
async def read_note(note_id: int, session: AsyncSession = Depends(get_db)):
    note = await note_manager.get(session, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    return note


@router.post("/", response_model=NoteSchema, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreate, session: AsyncSession = Depends(get_db)):
    response = await note_manager.create(session, obj_in=payload)
    return response


@router.put("/{note_id}", response_model=NoteSchema, status_code=status.HTTP_200_OK)
async def update_note(
    note_id: int,
    payload: NoteUpdate,
    session: AsyncSession = Depends(get_db),
):
    note = await note_manager.get(session, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    response = await note_manager.update(session, db_obj=note, obj_in=payload)
    return response


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, session: AsyncSession = Depends(get_db)):
    note = await note_manager.get(session, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    await note_manager.remove(session, obj=note)
    return note
