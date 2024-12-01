from fastapi import APIRouter, Body, HTTPException, status, Path
from planner_api.models.events import Event, EventUpdate

event_router = APIRouter(tags=["Events"])

events = []

@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    events.append(body) 
    return {
        "message": "Event created successfully"
    }

@event_router.get("/", response_model=list[Event])
async def retrieve_all_events() -> list[Event]:
    return events 

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    # Use a correct reference to the event variable
    for event in events:
        if event.id == id:  # Change 'events.id' to 'event.id'
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {
                "message": "Event deleted successfully"
            }
    raise HTTPException(  # Use raise instead of returning
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@event_router.put("/{id}", response_model=EventUpdate)
async def update_event( body: EventUpdate,
    id: int = Path(..., title="The ID of the event to be updated")
   
) -> EventUpdate:
    # Iterate over events to find the event by ID
    for event in events:
        if event.id == id:
            # Update the event with the new data from the body
            if body.title is not None:
                event.title = body.title
            if body.image is not None:
                event.image = body.image
            if body.description is not None:
                event.description = body.description
            if body.tags is not None:
                event.tags = body.tags
            if body.location is not None:
                event.location = body.location
            
            # Return the updated event
            return event

    # Raise an error if the event with the specified ID was not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
