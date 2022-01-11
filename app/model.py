from uuid import UUID


class Campaign:
    id: UUID
    name: str
    subject: str

    def __init__(self, id, name, subject):
        self.id = id
        self.name = name
        self.subject = subject
