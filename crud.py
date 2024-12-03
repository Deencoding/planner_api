from sqlalchemy.orm import Session
from planner_api.schemas.users import UserCreate
from planner_api.models.users import User
from planner_api.schemas.events import EventCreate, EventUpdate
from planner_api.models.events import Event

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_event(db: Session, events: EventCreate, user_id: int):
    db_event = Event(
        title=events.title,
        image=events.image,
        description=events.description,
        # tags=','.join(events.tags), # Convert list to comma-separated string
        # tags=events.tags, 
        location=events.location,
        created_by=user_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_event_by_id(db: Session, id: int):
    return db.query(Event).filter(Event.id == id).first()

def get_events_by_user(db: Session, email: str):
    """Fetch all events for a given user email"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    return db.query(Event).filter(Event.created_by == user.id).all()

def update_event(db: Session, title: str, event_data: EventUpdate):
    event = db.query(Event).filter(Event.title == title).first()
    if not event:
        return None
    if event_data.title is not None:
        event.title = event_data.title
    if event_data.image is not None:
        event.image = event_data.image
    if event_data.description is not None:
        event.description = event_data.description
    # if event_data.tags is not None:
    #     event.tags = ','.join(event_data.tags)  # Convert list to string
    if event_data.location is not None:
        event.location = event_data.location
    db.commit()
    db.refresh(event)
    return event

# def update_event(db: Session, event_id: int, event_data: EventUpdate):
#     event = db.query(Event).filter(Event.id == event_id).first()
#     if not event:
#         return None
#     for field, value in event_data.dict(exclude_unset=True).items():
#         setattr(event, field, value)
#     db.commit()
#     db.refresh(event)
#     return event

def delete_event(db: Session, title: str):
    event = db.query(Event).filter(Event.title == title).first()
    if event:
        db.delete(event)
        db.commit()
    return event

def delete_user(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        db.delete(user)
        db.commit()
    return user
