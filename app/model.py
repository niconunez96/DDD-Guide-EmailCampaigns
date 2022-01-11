from uuid import UUID


class Campaign:
    id: UUID
    name: str
    subject: str

    def __init__(self, id: UUID, name: str, subject: str):
        self.id = id
        self.name = name
        self.subject = subject
