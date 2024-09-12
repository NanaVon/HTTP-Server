from datetime import datetime
from httpMessage import httpMessage
from httpRequest import httpRequest
from httpResponse import httpResponse
from tcpServer import TCPserver
from typing import List 
import argparse
import asyncio
import os
import logging


class httpServer(TCPserver):
    def __init__(self, dir= None, IP="0.0.0.0", PORT=4456):
        super().__init__(IP=IP, PORT=PORT)
        self.defaultEncoding = 'ascii'
        self.httpVersion = "HTTP/1.0"
        self.SupportedMethods = ["GET", "POST"]
        self.Routes = []
        self.Dir = dir
    async def processRequest(self, byte: bytes):
        MessageRaw = byte.decode(self.defaultEncoding)
        message = httpRequest(MessageRaw)
        if message.Method not in self.SupportedMethods:
            return self.encode(httpResponse.not_implemented(self.httpVersion))
        if message.RequestUri == "/":
            return self.encode(httpResponse.Ok(self.httpVersion, body="Hello World"))
        if message.RequestUri.lower() == "/user-agent":
            return self.encode(httpResponse.Ok(self.httpVersion, body=message.UserAgent))
        if message.RequestUri.lower().find("/echo/") == 0:
            return self.encode(httpResponse.Ok(self.httpVersion, self.handleEcho(message.RequestUri), headers={"Content-Type": "text/plain"}))
        if message.RequestUri.lower().find("/files/") == 0:
            fileName = message.RequestUri[len("/files/"):]
            if not self.Dir:
                return self.encode(httpResponse.NotFound(self.httpVersion))
            if message.IsGet():
                filepath = os.path.join(self.Dir, fileName)
                if os.path.exists(filepath) and os.path.isfile(filepath):
                        with open(filepath, 'rb') as file:
                            return self.encode(httpResponse.Ok(self.httpVersion, body=file.read(), headers={"Content-Type": "application/octet-stream"}))
                else:
                    return self.encode(httpResponse.NotFound(self.httpVersion))
            elif message.IsPost():
                filepath = os.path.join(self.Dir, fileName)
                try:
                    with open(filepath, 'w') as file:
                        file.write(message.Body) 
                    return self.encode(httpResponse.Created(self.httpVersion))
                except Exception as e:
                    return self.encode(httpResponse.NotFound(httpVersion=self.httpVersion,body=e))
        return self.encode(httpResponse.NotFound(self.httpVersion))
    def encode(self, httpResponse):
        return str(httpResponse).encode(self.defaultEncoding)
    def addRoute(self, path:str, body:str, method:List[str]):
        self.Routes[path] = Route(path=path, methods= method,  content=httpResponse.Ok(body=body))
    def handleEcho(self,Uri):
        return Uri[len("/echo/"):]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server")

    parser.add_argument("--ip", type=str, default="0.0.0.0", help="IP address to bind the server to")
    parser.add_argument("--port", type=int, default=4456, help="Port number to bind the server to")
    parser.add_argument("--directory", default=None, help="Maximum number of threads in the thread pool")

    args = parser.parse_args()
    server = httpServer(dir=args.directory, IP=args.ip, PORT=args.port)

    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        server.stop()
        server.Logger.info("Server stopped.")