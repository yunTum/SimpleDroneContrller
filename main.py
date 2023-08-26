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
  
  def __init__(self, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    self.address = ('192.168.10.1', port)
    self.socket.bind(('', port))
    self.socket.settimeout(2)
    self.udp_bufsize = 1024
    self.state = self.STATE_STR_CONNECTED
    
    threading.Thread(target=self.recv_data).start()
  
  def __del__(self):
    print('TelloSocket is deleted')
    
  def socket_send(self, command):
      self.socket.sendto(command.encode('utf-8'), self.address)
      
  def socket_receive(self):
      try:
          response, ip_address = self.socket.recvfrom(128)
          print(response)
          return response
      except self.socket.timeout:
          print ('Timeout')
          return None
  
  def recv_data(self):
    while self.state != self.STATE_STR_QUIT:
      try:
          data, server = self.socket.recvfrom(self.udp_bufsize)
          print("recv: %s", data)
      except self.socket.timeout as ex:
          if self.state == self.STATE_STR_CONNECTED:
              print('recv: timeout')
      except Exception as ex:
          print('recv: %s', str(ex))
    print('exit from the recv thread.')
  
  def socket_close(self):
    self.socket.close()

def drone_test():
  tello = TelloSocket(8889)
  tello.socket_send('takeoff')
  time.sleep(5)
  tello.socket_send('land')
  tello.socket_close()
  del tello

def main():
  drone_test()