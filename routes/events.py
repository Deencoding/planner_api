from fastapi import APIRouter, Body, HTTPException, status, Path, Depends
from planner_api.schemas.events import EventCreate, EventUpdate
from sqlalchemy.orm import Session
from planner_api import crud
from planner_api.databases.database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

event_router = APIRouter(tags=["Events"])


@event_router.post("/new", response_model=EventCreate)
async def create_event(email: str, event: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event for a specific user identified by email.
    """
    # Fetch the user by email
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied email does not exist"
        )

    # Create the event, associating it with the user
    db_event = crud.create_event(db, event, user.id)
    return db_event

@event_router.get("/events/{email}")
async def retrieve_events_by_user(email: str, db: Session = Depends(get_db)):
    """
    Retrieve all events created by a specific user (email).
    """
    events = crud.get_events_by_user(db, email)
    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No events found for the specified user"
        )
    return events

@event_router.get("/{id}")
async def get_event_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve an event by its ID.
    """
    event = crud.get_event_by_id(db, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with the supplied ID does not exist"
        )
    return event

@event_router.put("/{title}")
async def update_event(title: str, event_data: EventUpdate, db: Session = Depends(get_db)):
    """
    Update an existing event.
    """
    event = crud.update_event(db, title, event_data)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with the specified title not found"
        )
    return event

@event_router.delete("/{title}")
async def delete_event(title: str, db: Session = Depends(get_db)):
    """
    Delete an event by its title.
    """
    event = crud.delete_event(db, title)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with the specified title not found"
        )
    return {"message": f"Event '{title}' deleted successfully"}
