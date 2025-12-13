"""
Command data model for the Physical AI & Humanoid Robotics project.

This module defines the Command entity with all required attributes as
specified in the data model.
"""
from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum

class CommandType(Enum):
    TEXT = "text"
    VOICE = "voice"

class CommandStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Command:
    """Natural language input from the user that needs to be processed and executed by the robot."""
    
    def __init__(
        self,
        text: str,
        type_: CommandType,
        user_id: UUID,
        id_: Optional[UUID] = None,
        timestamp: Optional[datetime] = None,
        status: CommandStatus = CommandStatus.PENDING
    ):
        if not text.strip():
            raise ValueError("Command text must not be empty")
        
        self.id = id_ or uuid4()
        self.text = text
        self.type = type_
        self.timestamp = timestamp or datetime.now()
        self.status = status
        self.user_id = user_id
    
    def to_dict(self):
        """Convert the command to a dictionary representation."""
        return {
            "id": str(self.id),
            "text": self.text,
            "type": self.type.value,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "user_id": str(self.user_id)
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create a Command instance from a dictionary."""
        return cls(
            id_=UUID(data["id"]),
            text=data["text"],
            type_=CommandType(data["type"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            status=CommandStatus(data["status"]),
            user_id=UUID(data["user_id"])
        )