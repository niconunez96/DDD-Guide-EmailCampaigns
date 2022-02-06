class Campaign:
    _name: str
    _subject: str
    _body: str
    _sender: str

    def __init__(self, name: str, subject: str, body: str, sender: str):
        self._name = name
        self._subject = subject
        self._body = body
        self._sender = sender
