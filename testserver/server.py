import socket

class TestServer:
  def __init__(self):
    self.server_state = "init"
    self.host = "localhost"
    self.server_port = 9999
    self.client_port = 9998

  def setup(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind((self.host, self.server_port))
    print("Server started at port", self.server_port)
    self.server_state = "connected"
  
  def recv(self):
    while self.server_state == "connected":
      try:
        data, ip_addr = self.sock.recvfrom(1024)
        addr = (ip_addr[0], self.client_port)
        print("Message from", addr)
        print("from connected user: " + str(data))
        print("sending: " + str("OK"))
        self.sock.sendto("SEND OK".encode('utf-8'), addr)
      except KeyboardInterrupt:
        print("Server stopped")
        self.server_state = "quit"
        self.sock.close()
      if data.decode() in "quit":
        print("Client is requesting to quit")
        self.server_state = "quit"
        self.sock.close()
        break

def main():
  server = TestServer()
  server.setup()
  server.recv()
  
if __name__ == '__main__':
  main()