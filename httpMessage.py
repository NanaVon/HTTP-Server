import json

class httpMessage:
    startLine:str
    RawMessage:str 
    Headers: dict 
    def __init__(self, RawMessage):
        self.CRLF = "\r\n"
        self.RawMessage = RawMessage
        self.StartLine = self.parserStartline(RawMessage)
        self.Headers = self.parserHeaders()
        self.Body = self.parserBody()
        self.UserAgent = ""
        self.ProccessHeaders()
    def parserStartline(self,RawMessage:str="", StartLine:str=""):
        if RawMessage:
            messageSplited = RawMessage.split(self.CRLF)
            return messageSplited[0]
        if StartLine:
            return StartLine
        
    def parserBody(self):
        messageSplited = self.RawMessage.split(self.CRLF) 
        return messageSplited[-1]
    def parserHeaders(self):
        messageSplited = self.RawMessage.split(self.CRLF)
        if len(messageSplited) < 3:
            raise Exception("Unexpected message format")
        if messageSplited[1]:
            RawHeaders = messageSplited[1:-1]
            headers ={}
            for line in RawHeaders:
                header = line.split(":", 1)
                if len(header) == 2:
                    headers[header[0]] = header[1]
            return headers

    def ProccessHeaders(self):
        if self.Headers:
            for header in self.Headers:
                if header.lower() == "user-agent":
                    self.UserAgent = self.Headers[header]


    def __str__(self):
        if self.Headers:
            headers = self.CRLF.join(f"{key}:{value}" for key, value in self.Headers.items())
        else:
            headers = ""
        return "{}{}{}{}{}{}".format(self.StartLine,self.CRLF,headers, self.CRLF, self.CRLF, self.Body)
