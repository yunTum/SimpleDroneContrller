#!/usr/bin/env python

import socket
import time
import threading
import command_list

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
  MY_IP_ADDRESS = '192.168.10.2'
  MY_PORT = 9000
  
  def __init__(self, port, *mode):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.tello_address = (self.TELLO_IP_ADDRESS, port)
    self.my_address = (self.MY_IP_ADDRESS, self.MY_PORT)
    self.mode = mode
    if 'testmode' in self.mode:
      print(self.mode[0])
      self.tello_address = (self.TEST_IP_ADDRESS, 9999)
      self.my_address = (self.TEST_IP_ADDRESS, 9998)
    
    self.socket.bind(self.my_address)
    self.socket.settimeout(2)
    self.udp_bufsize = 1024
    self.state = self.STATE_STR_CONNECTED
    
    self.thead_recv = threading.Thread(target=self.recv_data)
    self.thead_recv.start()

    self.thead_query = threading.Thread(target=self.send_query)
    self.thead_query.start()

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
  
  def send_query(self):
    while self.state != self.STATE_STR_QUIT:
      try:
        self.socket_send(command_list.query_battery)
      except Exception as ex:
        print('fail query', ex)
      time.sleep(0.1)
      try:
        self.socket_send(command_list.query_attitude)
      except Exception as ex:
        print('fail query', ex)
      time.sleep(0.1)
      try:
        self.socket_send(command_list.query_tof)
      except Exception as ex:
        print('fail query', ex)
      time.sleep(0.1)
  
  def change_state(self, state):
    self.state = state
  
  def socket_close(self):
    self.state = self.STATE_STR_QUIT
    if self.mode == 'testmode':
      self.socket.sendto('quit'.encode('utf-8'), self.tello_address)
    self.thead_recv.join()
    self.thead_query.join()
    self.socket.close()

def drone_test():
  tello_port = 8889
  tello = TelloSocket(tello_port, '')
  tello.socket_send(command_list.Command)
  time.sleep(1)
  tello.socket_send(command_list.takeoff)
  time.sleep(5)
  tello.socket_send(command_list.cw + ' 30')
  time.sleep(3)
  tello.socket_send(command_list.land)
  tello.socket_close()
  del tello  

if __name__ == "__main__":
  drone_test()