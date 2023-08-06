from attr import dataclass


@dataclass
class Author:
    name: str
    email: str
    organisation: str
