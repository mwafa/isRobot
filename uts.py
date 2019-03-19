from sr.robot import *

import time
TIME = time.time()
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
    FAKTOR = 0 if state == FIND else -12

    marker,offset = (MARKER_TOKEN_C,1) if state == FIND else (MARKER_ARENA,21)
    tokens = filter(lambda m: m.info.marker_type == marker and 
                        m.info.offset == offset ,R.see())
    
    if len(tokens) < 1:
        turn(-100)
    else:
        m = tokens[0]
        DIST = .4 if state == FIND else 1
        if m.dist < DIST:
            if state == FIND:
                if R.grab():
                    print "yay"
                    state = HOME
                    # exit()
            else:
                drive(0)
                turn(-100)
                time.sleep(.1)
                drive(75)
                time.sleep(1)
                drive(0)
                print time.time()-TIME
                exit()
 
        elif -DERAJAT <= m.rot_y+FAKTOR <= DERAJAT:
            drive(100)
        elif m.rot_y < -DERAJAT:
            turn(-50)
        elif m.rot_y > DERAJAT:
            turn(50)