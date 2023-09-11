#!/usr/bin/env python

import socket
import time
import command_list
import cv2

'''
# Bind the socket to the port
# address = 192.168.10.1 UDP PORT 8889
'''
class TelloStateSocket:
  TELLO_IP_ADDRESS = '192.168.10.1'
  TEST_IP_ADDRESS = 'localhost'
  MY_IP_ADDRESS = '192.168.10.2'
  MY_PORT = 9000
  
  def __init__(self, port, *mode):
    self.mode = mode
    self.port = port
    self.udp_bufsize = 1024
    self.state = 'disconnected'
    self.response = None
    self.socket = None

  def __del__(self):
    print('TelloStateSocket is deleted')
  
  def socket_setup(self):
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.tello_address = (self.TELLO_IP_ADDRESS, self.port)
      self.my_address = (self.MY_IP_ADDRESS, self.MY_PORT)
      if 'testmode' in self.mode:
        print(self.mode[0])
        self.mode = self.mode[0]
        self.tello_address = (self.TEST_IP_ADDRESS, 9999)
        self.my_address = (self.TEST_IP_ADDRESS, 9998)
      
      self.socket.bind(self.my_address)
      self.state = 'connected'
      self.socket.settimeout(2)
    except Exception as ex:
      print('socket failed: {0}'.format(str(ex)) )
      self.state = 'failed'
  
  def socket_send(self, command):
      self.socket.sendto(command.encode('utf-8'), self.tello_address)
  
  def recv_data(self):
    try:
        response, ip_address = self.socket.recvfrom(self.udp_bufsize)
        response = response.decode('utf-8')
        if response:
          self.response = response
    except Exception as ex:
        print('recv: {0}'.format(str(ex)) )
        self.response = ""
        self.state = 'failed'
    return response
  
  def send_query(self):
      # self.socket_send(command_list.query_battery)
      # time.sleep(0.1)
      self.socket_send(command_list.query_attitude)
      time.sleep(0.1)
      self.socket_send(command_list.query_tof)
      time.sleep(0.1)
      # self.socket_send(command_list.query_baro)
      # time.sleep(0.1)
      # self.socket_send(command_list.query_height)
      # time.sleep(0.1)
      self.socket_send(command_list.qury_acceleration)
      time.sleep(0.1)
      self.socket_send(command_list.query_speed)
      time.sleep(0.1)
      
  def get_response(self):
    return self.response
  
  def set_state(self, state):
    self.state = state
  
  def get_state(self):
    return self.state
  
  def socket_close(self):
    if self.mode == 'testmode':
      self.socket.sendto('quit'.encode('utf-8'), self.tello_address)
    self.socket.close()
    self.state = 'disconnected'

def drone_test():
  tello_port = 8889
  tello = TelloStateSocket(tello_port, '')
  tello.socket_setup()
  tello.socket_send(command_list.Command)
  time.sleep(1)
  tello.socket_send(command_list.takeoff)
  time.sleep(5)
  tello.socket_send(command_list.cw + ' 30')
  time.sleep(3)
  tello.socket_send(command_list.land)
  tello.socket_close()
  del tello  

class Tello:
  def __init__(self):
    self.battery = 0
    self.attitude = {'pitch':0, 'roll':0, 'yaw':0}
    self.tof = 0
    self.height = 0
    self.acceleration = {'agx':0, 'agy':0, 'agz':0}
    self.speed = {'vgx':0, 'vgy':0, 'vgz':0}
    self.barometer = 0
  
  def set_battery(self, battery):
    self.battery = battery

  def set_attitude(self, pitch, roll, yaw):
    self.attitude['pitch'] = pitch
    self.attitude['roll'] = roll
    self.attitude['yaw'] = yaw
  
  def set_tof(self, tof):
    self.tof = tof
  
  def set_height(self, height):
    self.height = height
  
  def set_acceleration(self, agx, agy, agz):
    self.acceleration['agx'] = agx
    self.acceleration['agy'] = agy
    self.acceleration['agz'] = agz
  
  def set_speed(self, vgx, vgy, vgz):
    self.speed['vgx'] = vgx
    self.speed['vgy'] = vgy
    self.speed['vgz'] = vgz
    
  def set_barometer(self, baro):
    self.barometer = baro

  def get_state(self):
    return self.battery, self.attitude, self.tof, self.height, self.acceleration, self.speed

class TelloVideoSocket:
  TELLO_IP_ADDRESS = '0.0.0.0'
  TELLO_IP_PORT = 11111
  TELLI_VIDEO_ADDRESS = 'udp://@' + TELLO_IP_ADDRESS + ':' + str(TELLO_IP_PORT)
  
  def __init__(self):
    self.cap = cv2.VideoCapture(self.TELLI_VIDEO_ADDRESS)
    self.frame = None
    
  def __del__(self):
    self.cap.release()
    cv2.destroyAllWindows()
  
  def get_frame(self):
    ret, frame = self.cap.read()
    if ret:
      self.frame = frame

if __name__ == "__main__":
  drone_test()