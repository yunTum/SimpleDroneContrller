#!/usr/bin/env python

import tello_manager
import time
import threading
import PySimpleGUI as sg

class TelloController:
  def __init__(self, mode):
    self.tello = tello_manager.TelloSocket(8889, mode)
    # Tello SDK mode
    self.tello.socket_send('command')
    self.window = None

  def create_window(self):
    sg.theme('DarkGrey5')
    flight_state_frame = sg.Frame('',
      [
        [sg.Text('Fight State')],
        [sg.Text('Battery:'), sg.Text('0%', key='-BATTERY-')],
        [sg.Text('X-Speed:'), sg.Text('0 m/s', key='-XSPEED-')],
        [sg.Text('Y-Speed:'), sg.Text('0 m/s', key='-YSPEED-')],
        [sg.Text('Z-Speed:'), sg.Text('0 m/s', key='-ZSPEED-')],
        [sg.Text('Roll:'), sg.Text('0 rad', key='-ROLL-')],
        [sg.Text('Pitch:'), sg.Text('0 rad', key='-PITCH-')],
        [sg.Text('Barometer:'), sg.Text('0 cm', key='-BAROMETER-')],
        [sg.Text('ToF-Distance:'), sg.Text('0 m', key='-TOF-')],
        [sg.Text('Height:'), sg.Text('0%', key='-HEIGHT-')],
      ], size=(100,100)
    )
    udp_frame = sg.Frame('',
      [
        [sg.Text('Socket State')],
        [sg.Text('Socket:'), sg.Text('disconneted', key='-SOCKET-')],
      ], size=(100,100)
    )
    flight_flame = sg.Frame('',
      [
        [sg.Text('Flight')],
        [sg.Button('TAKEOFF', key='-TAKEOFF-'), sg.Button('LAND', key='-LAND-')],
      ], size=(200,200), pad=((20, 0), ( 0, 50))
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
        [flight_flame],
        [move_frame],
      ], relief=sg.RELIEF_FLAT
    )
    
    layout =  [ 
                [state_frame, control_frame],
              ]

    self.window = sg.Window('Tello Controller', layout, resizable=True)
  
  def run(self):
  
    while True:
        event, values = self.window.read()
        if event == sg.WIN_CLOSED:
          self.tello.socket_send('quit')
          self.tello.change_state(self.tello.STATE_STR_QUIT)
          break
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

    self.window.close()
  
  def event_takeoff(self):
    print('TAKEOFF')
    self.tello.socket_send('takeoff')
  
  def event_land(self):
    print('LAND')
    self.tello.socket_send('land')
  
  def event_front(self):
    print('FRONT')
    self.tello.socket_send('forward 20')
  
  def event_back(self):
    print('BACK')
    self.tello.socket_send('back 20')
  
  def event_left(self):
    print('LEFT')
    self.tello.socket_send('left 20')
  
  def event_right(self):
    print('RIGHT')
    self.tello.socket_send('right 20')
  
  def event_leftroll(self):
    print('LEFTROLL')
    self.tello.socket_send('ccw 20')
  
  def event_rightroll(self):
    print('RIGHTROLL')
    self.tello.socket_send('cw 20')

if __name__ == "__main__":
  pass