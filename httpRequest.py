from httpMessage import httpMessage

class httpRequest(httpMessage):
    def __init__(self, RawMessage:str) -> None:
        super().__init__(RawMessage)
        self.SplittedStartLine = RawMessage.split(self.CRLF)[0].split(' ')
        self.Method = self.SplittedStartLine[0] if self.SplittedStartLine[0] is not None else (_ for _ in ()).throw(ValueError("Method cannot be null!"))
        self.RequestUri = self.SplittedStartLine[1]  if self.SplittedStartLine[1] is not None else (_ for _ in ()).throw(ValueError("Uri cannot be null!"))
        self.HttpVersion = self.SplittedStartLine [2]  if self.SplittedStartLine[2] is not None else (_ for _ in ()).throw(ValueError("HTTP/version cannot be null!"))

    def IsGet(self):
        return self.Method == "GET"
    def IsPost(self):
        return self.Method == "POST"