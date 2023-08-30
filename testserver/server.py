import socket
import sys
sys.path.append('..')
import command_list

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
        recvdata, ip_addr = self.sock.recvfrom(1024)
        recvdata_decoded = recvdata.decode()
        addr = (ip_addr[0], self.client_port)
        print("Message from", addr)
        print("from connected user: " + recvdata_decoded)
        if recvdata_decoded in command_list.query_attitude:
          print("sending: " + "pitch:10;roll:20;yaw:30;")
          self.sock.sendto("pitch:10;roll:20;yaw:30;".encode('utf-8'), addr)
        if recvdata_decoded in command_list.query_battery:
          print("sending: " + "battery:100;")
          self.sock.sendto("battery:100;".encode('utf-8'), addr)
        if recvdata_decoded in command_list.query_baro:
          print("sending: " + "baro:0.01;")
          self.sock.sendto("baro:0.01;".encode('utf-8'), addr)
        if recvdata_decoded in command_list.query_tof:
          print("sending: " + "tof:123;")
          self.sock.sendto("tof:123;".encode('utf-8'), addr)
        if recvdata_decoded in command_list.query_height:
          print("sending: " + "height:634;")
          self.sock.sendto("height:634;".encode('utf-8'), addr)
        if recvdata_decoded in command_list.qury_acceleration:
          print("sending: " + "agx:12;agy:22;agz:32;")
          self.sock.sendto("agx:12;agy:22;agz:33;".encode('utf-8'), addr)
        if recvdata_decoded in command_list.query_speed:
          print("sending: " + "vgx:33;vgy:44;vgz:55;")
          self.sock.sendto("vgx:33;vgy:44;vgz:55;".encode('utf-8'), addr)
        if recvdata_decoded in command_list.query_wifi:
          print("sending: " + "wifi:150;")
          self.sock.sendto("wifi:150;".encode('utf-8'), addr)
      except KeyboardInterrupt:
        print("Server stopped")
        self.server_state = "quit"
        self.sock.close()
      if recvdata_decoded in "quit":
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