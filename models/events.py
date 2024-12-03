from planner_api.databases.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    image = Column(String, nullable=True)
    description = Column(String(1000), nullable=False)
    # tags = Column(String(500), nullable=True)
    location = Column (String(255), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

    # Define relationship with the User model
    creator = relationship("User", back_populates = "events")

    # @property
    # def tag_list(self):
    #     return self.tags.split(',') if self.tags else []