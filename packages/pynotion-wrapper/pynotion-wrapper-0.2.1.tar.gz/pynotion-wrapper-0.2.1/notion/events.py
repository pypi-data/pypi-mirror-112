from dataclasses import dataclass
from uuid import UUID


@dataclass
class DatabaseEvent:
    database_id: UUID


@dataclass
class UserEvent:
    user_id: UUID
