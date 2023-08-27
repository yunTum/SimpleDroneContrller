#!/usr/bin/env python

import socket
import time
import threading

'''
# Bind the socket to the port
# address = 192.168.10.1 UDP PORT 8889
'''
class TelloSocket:
  STATE_STR_DISCONNECTED = 'disconnected'
  STATE_STR_CONNECTED = 'connected'
  STATE_STR_CONNECTING = 'connecting'
  STATE_STR_QUIT = 'quit'
  TELLO_IP_ADDRESS = '192.168.10.1'
  TEST_IP_ADDRESS = 'localhost'
  MY_IP_ADDRESS = 'localhost'
  MY_PORT = 9000
  
  def __init__(self, port, *mode):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.tello_address = (self.TELLO_IP_ADDRESS, port)
    self.my_address = (self.MY_IP_ADDRESS, self.MY_PORT)
    if 'testmode' in mode:
      print(mode[0])
      self.tello_address = (self.TEST_IP_ADDRESS, 9999)
      self.my_address = (self.TEST_IP_ADDRESS, 9998)
    
    self.socket.bind(self.my_address)
    self.socket.settimeout(2)
    self.udp_bufsize = 1024
    self.state = self.STATE_STR_CONNECTED
    
    self.thead = threading.Thread(target=self.recv_data)
    self.thead.start()

  def __del__(self):
    print('TelloSocket is deleted')
    
  def socket_send(self, command):
      self.socket.sendto(command.encode('utf-8'), self.tello_address)
  
  def recv_data(self):
    timeout_count = 0
    while self.state != self.STATE_STR_QUIT:
      try:
          response, ip_address = self.socket.recvfrom(self.udp_bufsize)
          response = response.decode('utf-8')
          print("recv: {0}".format(response) )
          if response:
            timeout_count = 0
      except Exception as ex:
          print('recv: {0}'.format(str(ex)) )
          timeout_count += 1
          if timeout_count > 5:
            print('over timeout count')
            break
    print('exit from the recv thread.')
  
  def change_state(self, state):
    self.state = state
  
  def socket_close(self):
    self.state = self.STATE_STR_QUIT
    self.socket.sendto('quit'.encode('utf-8'), self.tello_address)
    self.thead.join()
    #self.socket.close()

def drone_test():
  tello_port = 8889
  tello = TelloSocket(tello_port, 'testmode')
  tello.socket_send('command')
  time.sleep(1)
  tello.socket_send('takeoff')
  time.sleep(5)
  tello.socket_send('land')
  tello.socket_close()
  del tello  

if __name__ == "__main__":
  drone_test()