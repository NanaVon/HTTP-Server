from enum import Enum

class HTTPStatusCode(Enum):
    OK = 200
    Not_Found = 404
    Not_Implemented = 501
    Created = 201

    @property
    def reasonPhrase(self):
        return self.name.replace('_', ' ').title()
