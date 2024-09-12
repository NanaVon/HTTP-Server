import socket
from dataclasses import dataclass
import logging
import asyncio

class TCPserver:
	def __init__(self, IP:str="0.0.0.0", PORT:int=4456, Logger=logging ):
		self.IP= IP
		self.PORT = PORT
		self.Logger =self.initLogger()
		self.ShouldStop = False
	async def start(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
			print(self.IP, "que es esto")
			server.bind((self.IP, self.PORT))
			server.listen(5)
			server.setblocking(False)
			ipLocal = socket.gethostbyname(socket.gethostname())
			self.Logger.info("Server started on {}:{}. Awaiting connections...".format(ipLocal,self.PORT))
			
			while not self.ShouldStop:
				connection, address = await asyncio.get_event_loop().sock_accept(server)
				self.Logger.info("Accepted connection from {}:{}".format(address[0], address[1]))
				asyncio.create_task(self.handleClient(connection, address))
	def stop(self):
		self.ShouldStop = True
	def processRequest(self):
		pass
	async def handleClient(self, connection,address):
		try:
			while not self.ShouldStop:
				data = await asyncio.get_event_loop().sock_recv(connection, 1024)
				if not data:
					break
				response = await self.processRequest(data)
				await asyncio.get_event_loop().sock_sendall(connection, response)
				connection.close()
				
		except Exception as error:
			pass

	def initLogger(self, nivel: int = logging.DEBUG, archivo_log: str = None) -> logging.Logger:
		logger = logging.getLogger()
		logger.setLevel(nivel)
		
		formateador = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		consoleHandler = logging.StreamHandler()
		consoleHandler.setLevel(nivel)
		consoleHandler.setFormatter(formateador)
		logger.addHandler(consoleHandler)

		return logger