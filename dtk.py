#!/usr/local/bin/python
''' Dark Throne Clicker - set mouse on THE point and start program '''
import time
import os
import pyautogui
import threading
from pymouse import PyMouseEvent

# setup:
exitFlag = 0        # while 0 threads are working
max_clicks = 400    # how many clicks
clicks = 0          # count of clicks
screen_size = pyautogui.size()
mouse_pos = pyautogui.position()

print('{screen:>15}({0:4d}, {1:4d})'.format(screen = 'Screen size', *screen_size))
print('{mouse:>15}({0:4d}, {1:4d})'.format(mouse = 'Mouse position', *mouse_pos))

pyautogui.click(mouse_pos) # make sure target is on top

def ctrlTab():
    pyautogui.keyDown('ctrlleft')
    pyautogui.press('tab')
    pyautogui.keyUp('ctrlleft')

class ClickerThread(threading.Thread):
    ''' Thread for clicking action '''
    def __init__(self):
        super().__init__()
        self.clicks = clicks

    def run(self):
        print('Clicker started!')
        global exitFlag
        while not exitFlag:
            self.clicks += 1
            pyautogui.click(mouse_pos)
            print(self.clicks)
            time.sleep(0.2)
            ctrlTab()
            time.sleep(0.5)
            if self.clicks >= max_clicks:
                print('Exiting Cliker!')
                exitFlag = 1
                time.sleep(0.2)
                os._exit(1)

class Cacher(PyMouseEvent):
    ''' cach mouse btn 2 click event and stop threads/program  '''
    def __init__(self):
        super().__init__()

    def click(self, x, y, button, press):
        global exitFlag
        if button == 2:
            if press:
                pyautogui.keyUp('ctrlleft') # make sure Ctrl is Up
                print('Right button pressed!')
                print('Exiting Watcher!')
                exitFlag = 1
                time.sleep(0.2)
                os._exit(1)

class Watcher(threading.Thread):
    ''' Uses Cacher to get mouse event and stop executing  '''
    def __init__(self):
        super().__init__()
        self.cacher = Cacher()
        
    def run(self):
        print('Watcher started!')
        global exitFlag
        while not exitFlag:
            print("Press 'Right mouse button' to stop!")
            self.cacher.run()

if __name__ == "__main__":
    w = Watcher()
    c = ClickerThread()
    w.start()
    c.start()
    w.join()
    c.join()
    exitFlag = 1
    print("Exiting Main Thread!")
    main()
