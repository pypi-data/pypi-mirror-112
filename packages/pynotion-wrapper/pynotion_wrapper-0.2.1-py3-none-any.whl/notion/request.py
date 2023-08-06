from dataclasses import dataclass
from .models import NotionConfig


@dataclass
class DatabaseRequest:
    url = f"{NotionConfig.endpoint}/databases"


@dataclass
class UserRequest:
    url = f"{NotionConfig.endpoint}/users"


@dataclass
class PageRequest:
    url = f"{NotionConfig.endpoint}/pages"


