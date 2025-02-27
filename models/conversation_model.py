from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_messages = Column(Text, nullable=False)

    # Relationship to User table
    user = relationship("User")