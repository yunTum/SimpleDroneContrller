#!/usr/bin/env python

import tello_manager
import time
import threading
import PySimpleGUI as sg
import re

class TelloController:
  def __init__(self, mode):
    self.state = 'init'
    self.mode = mode
    self.tello = None
    self.window = None
    self.recv_thread = None
    self.query_thread = None
    self.update_thread = None
    self.recv_thread = threading.Thread(target=self.recv_tello)
    self.query_thread = threading.Thread(target=self.query_tello)
    self.update_thread = threading.Thread(target=self.update_window)
    self.create_window()
    self.run()

  def create_window(self):
    sg.theme('DarkGrey5')
    flight_state_frame = sg.Frame('',
      [
        [sg.Text('Fight State')],
        [sg.Text('Battery:'), sg.Text('0%', key='-BATTERY-')],
        [sg.Text('X-Acc:'), sg.Text('0 m/s^2', key='-XACC-')],
        [sg.Text('Y-Acc:'), sg.Text('0 m/s^2', key='-YACC-')],
        [sg.Text('Z-Acc:'), sg.Text('0 m/s^2', key='-ZACC-')],
        [sg.Text('X-Speed:'), sg.Text('0 m/s', key='-XSPEED-')],
        [sg.Text('Y-Speed:'), sg.Text('0 m/s', key='-YSPEED-')],
        [sg.Text('Z-Speed:'), sg.Text('0 m/s', key='-ZSPEED-')],
        [sg.Text('Roll:'), sg.Text('0 rad', key='-ROLL-')],
        [sg.Text('Pitch:'), sg.Text('0 rad', key='-PITCH-')],
        [sg.Text('Yaw:'), sg.Text('0 rad', key='-YAW-')],
        [sg.Text('Barometer:'), sg.Text('0 cm', key='-BAROMETER-')],
        [sg.Text('ToF-Distance:'), sg.Text('0 m', key='-TOF-')],
        [sg.Text('Height:'), sg.Text('0%', key='-HEIGHT-')],
      ], size=(150,350)
    )
    udp_frame = sg.Frame('',
      [
        [sg.Text('Socket State')],
        [sg.Text('Socket:'), sg.Text('disconneted', key='-SOCKET-')],
      ], size=(200,100)
    )
    connect_frame = sg.Frame('',
      [
        [sg.Text('Connect')],
        [sg.Button('Connect', key='-CONNECT-'), sg.Button('Disconnect', key='-DISCONNECT-')],
        [sg.Button('TestCommand', key='-TESTCOMMAND-')]
      ], pad=((20, 0), ( 0, 50))
    )
    flight_flame = sg.Frame('',
      [
        [sg.Text('Flight')],
        [sg.Button('TAKEOFF', key='-TAKEOFF-'), sg.Button('LAND', key='-LAND-')],
      ], size=(200,100), pad=((20, 0), ( 0, 50))
    )
    
    move_frame = sg.Frame('',
      [
        [sg.Button('L', size=(5,2), key='-LEFTROLL-'), sg.Button('↑', size=(5,2), key='-FRONT-'), sg.Button('R', size=(5,2), key='-RIGHTROLL-')],
        [sg.Button('←', size=(5,2), key='-LEFT-'), sg.Button('↓', size=(5,2), key='-BACK-'), sg.Button('→', size=(5,2), key='-RIGHT-')],
      ], size=(200,200)
    )
    
    state_frame = sg.Frame('',
      [
        [flight_state_frame],
        [udp_frame],
      ], relief=sg.RELIEF_FLAT
    )
    
    control_frame = sg.Frame('',
      [
        [connect_frame],
        [flight_flame],
        [move_frame],
      ], relief=sg.RELIEF_FLAT
    )
    
    layout =  [ 
                [state_frame, control_frame],
              ]

    self.window = sg.Window('Tello Controller', layout, resizable=True, finalize=True)
  
  def tello_connect(self):
    try:
      self.tello = tello_manager.TelloSocket(8889, self.mode)
      self.tello.socket_setup()
      self.state = self.tello.get_state()
      self.window['-SOCKET-'].update(self.state)
      if self.state == 'connected':
        self.tello_state = tello_manager.Tello()
        self.window['-CONNECT-'].update(disabled=True)
        self.window['-DISCONNECT-'].update(disabled=False)
        # Tello SDK mode
        self.tello.socket_send('command')
        self.recv_thread.start()
        self.query_thread.start()
        self.update_thread.start()
    except Exception as ex:
      print('TelloController: {0}'.format(str(ex)) )
  
  def tello_disconnect(self):
    self.tello.socket_close()
    self.state = self.tello.get_state()
    self.recv_thread.join()
    self.query_thread.join()
    self.update_thread.join()
    self.window['-CONNECT-'].update(disabled=False)
    self.window['-DISCONNECT-'].update(disabled=True)
    self.window['-SOCKET-'].update(self.state)
  
  def run(self):
    while True:
        event, values = self.window.read()
        if event == sg.WIN_CLOSED:
          break
        if event == '-CONNECT-':
          self.tello_connect()
        if event == '-DISCONNECT-':
          self.tello_disconnect()
        if event == '-TAKEOFF-':
          self.event_takeoff()
        if event == '-LAND-':
          self.event_land()
        if event == '-FRONT-':
          self.event_front()
        if event == '-BACK-':
          self.event_back()
        if event == '-LEFT-':
          self.event_left()
        if event == '-RIGHT-':
          self.event_right()
        if event == '-LEFTROLL-':
          self.event_leftroll()
        if event == '-RIGHTROLL-':
          self.event_rightroll()
        if event == '-TESTCOMMAND-':
          self.event_testcommand()

    self.kill_thread()
    self.window.close()
  
  def kill_thread(self):
    if self.tello:
      self.tello.socket_close()
      self.state = self.tello.get_state()
      self.recv_thread.join()
      self.query_thread.join()
      self.update_thread.join()
  
  def recv_tello(self):
    response = None
    while self.state != 'disconnected':
      response = self.tello.recv_data()
      split_response = re.split('[:;]', response)
      # if 'battery' in split_response:
      #   self.tello_state.set_battery(split_response[1])
      if 'vgx' in split_response:
        self.tello_state.set_speed(split_response[1], split_response[3], split_response[5])
      if 'pitch' in split_response:
        self.tello_state.set_attitude(split_response[1], split_response[3], split_response[5])
      # if 'baro' in split_response:
      #   self.tello_state.set_barometer(split_response[1])
      if 'mm' in split_response[0]:
        self.tello_state.set_tof(split_response[0])
      # if 'height' in split_response:
      #   self.tello_state.set_height(split_response[1])
      if 'agx' in split_response:
        self.tello_state.set_acceleration(split_response[1], split_response[3], split_response[5])

    print('exit from the recv thread.')
    
  def query_tello(self):
    while self.state != 'disconnected':
      self.tello.send_query()

  def update_window(self, ):
    while self.state != 'disconnected':
      self.window['-BATTERY-'].update(self.tello_state.battery)
      self.window['-XACC-'].update(self.tello_state.acceleration['agx'])
      self.window['-YACC-'].update(self.tello_state.acceleration['agy'])
      self.window['-ZACC-'].update(self.tello_state.acceleration['agz'])
      self.window['-XSPEED-'].update(self.tello_state.speed['vgx'])
      self.window['-YSPEED-'].update(self.tello_state.speed['vgy'])
      self.window['-ZSPEED-'].update(self.tello_state.speed['vgz'])
      self.window['-ROLL-'].update(self.tello_state.attitude['roll'])
      self.window['-PITCH-'].update(self.tello_state.attitude['pitch'])
      self.window['-YAW-'].update(self.tello_state.attitude['yaw'])
      self.window['-BAROMETER-'].update(self.tello_state.barometer)
      self.window['-TOF-'].update(self.tello_state.tof)
      self.window['-HEIGHT-'].update(self.tello_state.height)
      time.sleep(0.5)
  
  def event_takeoff(self):
    print('TAKEOFF')
    if self.state == 'connected':
      self.tello.socket_send('takeoff')
  
  def event_land(self):
    print('LAND')
    if self.state == 'connected':
      self.tello.socket_send('land')
  
  def event_front(self):
    print('FRONT')
    if self.state == 'connected':
      self.tello.socket_send('forward 40')
  
  def event_back(self):
    print('BACK')
    if self.state == 'connected':
      self.tello.socket_send('back 40')
  
  def event_left(self):
    print('LEFT')
    if self.state == 'connected':
      self.tello.socket_send('left 40')
  
  def event_right(self):
    print('RIGHT')
    if self.state == 'connected':
      self.tello.socket_send('right 40')
  
  def event_leftroll(self):
    print('LEFTROLL')
    if self.state == 'connected':
      self.tello.socket_send('ccw 50')
  
  def event_rightroll(self):
    print('RIGHTROLL')
    if self.state == 'connected':
      self.tello.socket_send('cw 50')

  def event_testcommand(self):
      print('SEND TEST COMMAND')
      if self.state == 'connected':
        self.tello.socket_send('speed?')

if __name__ == "__main__":
  pass