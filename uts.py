from sr.robot import *

import time

R = Robot()

def drive(speed):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed

def turn(speed):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed

FIND, HOME = range(2)
DERAJAT = 5

state = FIND

while True:
    if state == FIND:
        tokens = filter(lambda m: m.info.marker_type == MARKER_TOKEN_C and m.info.offset == 1 ,R.see())
    else:
        tokens = filter(lambda m: m.info.marker_type == MARKER_ARENA and m.info.offset == 21 ,R.see())
    
    if len(tokens) < 1:
        turn(-100)
    else:
        m = tokens[0]
        DIST = .4 if state == FIND else 1
        if m.dist < 0.4 :
            if state == FIND:
                if R.grab():
                    print "yay"
                    drive(0)
                    state = HOME
                    # exit()
            else:
                drive(0)
                exit()
                
        elif -DERAJAT <= m.rot_y <= DERAJAT:
            drive(100)
        elif m.rot_y < -DERAJAT:
            turn(-50)
        elif m.rot_y > DERAJAT:
            turn(50)