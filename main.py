from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from planner_api.routes.events import event_router
from planner_api.routes.users import user_router

app = FastAPI(
    title="Event and User Management API", 
    description="An API for managing events and user authentication.",
    version="1.0.0"
)

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(event_router, prefix="/event")
app.include_router(user_router, prefix="/user")

