from httpMessage import httpMessage
from httpStatusCode import HTTPStatusCode
 
class httpResponse(httpMessage):
    def __init__(self, rawMessage = None, httpVersion= None, statusCode = None):
        super().__init__(rawMessage)
        self.SplittedStartLine = rawMessage.split(self.CRLF)[0].split(' ')
        self.HttpVersion = self.SplittedStartLine[0] if self.SplittedStartLine[0] is not None else (_ for _ in ()).throw(ValueError("Method cannot be null!"))
        self.StatusCode = self.SplittedStartLine[1] if self.SplittedStartLine[1] is not None else (_ for _ in ()).throw(ValueError("Method cannot be null!"))
        self.ReasonPhrase =self.SplittedStartLine[2] if self.SplittedStartLine[2] is not None else (_ for _ in ()).throw(ValueError("Method cannot be null!"))

    @staticmethod
    def not_implemented(httpVersion, body="", headers=""):
        rawMessage = httpResponse.messageGenerator(httpVersion, HTTPStatusCode.Not_Implemented, headers, body )
        return httpResponse(rawMessage)
    
    @staticmethod
    def NotFound(httpVersion, body="", headers=""):

        rawMessage = httpResponse.messageGenerator(httpVersion, HTTPStatusCode.Not_Found, headers, body )
        return httpResponse(rawMessage)
    
    @staticmethod
    def Ok(httpVersion, body="", headers=""):
        rawMessage = httpResponse.messageGenerator(httpVersion, HTTPStatusCode.OK, headers, body )
        return httpResponse(rawMessage)

    @staticmethod
    def Created(httpVersion, body="", headers=""):
        rawMessage = httpResponse.messageGenerator(httpVersion, HTTPStatusCode.Created, headers, body )
        return httpResponse(rawMessage)
    
    @staticmethod
    def messageGenerator(httpVersion, statusCode, listHeaders:list, body=""):
        headers = httpResponse.GetHeadersOfList(listHeaders)
        rawMessage = "{} {} {}\r\n{}\r\n\r\n\r\n{}".format(httpVersion, statusCode.value, statusCode.reasonPhrase, headers,  body)
        return rawMessage
    
    @staticmethod 
    def GetHeadersOfList( ListHeaders:list):
        headers = ""
        for header in ListHeaders:
            headers += "{}:{}".format(header, ListHeaders[header]) 
        return headers
    


