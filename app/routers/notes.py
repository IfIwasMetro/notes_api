from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user, get_owned_note, get_readable_note

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    note_in: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    note = models.Note(
        title=note_in.title,
        content=note_in.content,
        is_public=note_in.is_public,
        tags=note_in.tags,
        owner=current_user.username,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("/", response_model=List[schemas.NoteOut])
def list_notes(
    tag: Optional[str] = Query(None, description="Only notes containing this tag"),
    search_term: Optional[str] = Query(None, description="Search title and content"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Note)

    # Visibility: admins see everything, others see own + public
    if current_user.role != "admin":
        query = query.filter(
            or_(
                models.Note.owner == current_user.username,
                models.Note.is_public.is_(True),
            )
        )

    if search_term:
        pattern = f"%{search_term}%"
        query = query.filter(
            or_(
                models.Note.title.ilike(pattern),
                models.Note.content.ilike(pattern),
            )
        )

    notes = query.order_by(models.Note.created_at.desc()).all()

    # Tags live in a JSON column, so filter in Python
    if tag:
        wanted = tag.lower()
        notes = [n for n in notes if wanted in [t.lower() for t in (n.tags or [])]]

    return notes


@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(note: models.Note = Depends(get_readable_note)):
    return note


@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(
    note_in: schemas.NoteUpdate,
    note: models.Note = Depends(get_owned_note),
    db: Session = Depends(get_db),
):
    for field, value in note_in.model_dump(exclude_unset=True).items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note: models.Note = Depends(get_owned_note),
    db: Session = Depends(get_db),
):
    db.delete(note)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
