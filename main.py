#!/usr/bin/env python

import gui
import sys

def main():
  args = sys.argv
  mode = ''
  if len(args) > 1 and 'testmode' == args[1]:
    mode = args[1]
    print('run testmode')
  
  controller = gui.TelloController(mode)

if __name__ == "__main__":
  main()