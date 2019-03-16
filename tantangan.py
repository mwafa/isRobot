from sr.robot import *

import time

SEARCHING, DRIVING, HOME = range(3)

WAKTU = time.time()

FAKTOR = 1



R = Robot()

MARKER_TOKENS = (MARKER_TOKEN, MARKER_TOKEN_A, MARKER_TOKEN_B, MARKER_TOKEN_C)

# token_filter = lambda m: m.info.marker_type in MARKER_TOKENS

myFilter  = lambda filter,tokens: [token for token in tokens if filter(token)]

tokenKe = 1

kontra = [10,17,24,3,13,20,27,6]

myTokenFilter = lambda x: True if x.info.marker_type == 'token-a' and x.info.offset == tokenKe else False

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

state = SEARCHING

while True:
    if state == SEARCHING:
        print "Searching..."
        # print R.see()
        # exit()
        # tokens = filter(token_filter, R.see())
        tokens = myFilter(myTokenFilter,R.see())
        if len(tokens) > 0:
            m = tokens[0]
            # print "Token sighted. {3}-{0} is {1}m away, bearing {2} degrees. " \
            #       .format(m.info.offset, m.dist, m.rot_y, m.info.marker_type)
            state = DRIVING
            FAKTOR *= -1
            print (m.info.marker_type, m.info.offset, m.dist, m.rot_y)
            print "*"*30
        # print (R.see())

        # else:
        # print "Can't see anything."
        turn(50*FAKTOR, 0.1)
        # time.sleep(0.2)

    elif state == DRIVING:
        # print "Aligning..."
        # tokens = filter(token_filter, R.see())
        tokens = myFilter(myTokenFilter,R.see())
        if len(tokens) == 0:
            state = SEARCHING

        else:
            m = tokens[0]
            if m.dist < 0.4:
                print "Found it!"
                if R.grab():
                    state = HOME
                    # print "Gotcha!"
                    # turn(-50, 0.5)
                    # drive(50, 1)
                    # R.release()
                    # drive(-50, 0.5)
                    # if tokenKe < 8:
                    #     tokenKe += 1
                    # else:
                    #     print(time.time()-WAKTU)
                    #     exit() 
                else:
                    print "Aww, I'm not close enough."
                # exit()

            elif -15 <= m.rot_y <= 15:
                print "Ah, that'll do."
                drive(100, m.dist/2)
                FAKTOR = 1 if m.rot_y > 0 else -1

            elif m.rot_y < -15:
                print "Left a bit..."
                turn(-12.5, 0.1)

            elif m.rot_y > 15:
                print "Right a bit..."
                turn (12.5, 0.1)

    elif state == HOME:
        tokens = myFilter(lambda x: True if x.info.marker_type == "arena" and x.info.offset == kontra[tokenKe-1] else False,R.see())
        if len(tokens) == 0:
            # state = SEARCHING
            turn(50, 0.1)
        else:
            m = tokens[0]
            jarak = 4.5 if tokenKe < 5 else 5.5
            if m.dist < jarak:
                    print "Found it!"
                    if R.release():
                        state = SEARCHING
                        # print "Gotcha!"
                        # turn(-50, 0.5)
                        # drive(50, 1)
                        # R.release()
                        drive(-100, 1)
                        if tokenKe < 8:
                            tokenKe += 1
                        else:
                            print(time.time()-WAKTU)
                            exit() 
                    else:
                        print "Aww, I'm not close enough."
                    # exit()

            elif -10 <= m.rot_y <= 10:
                print "Ah, that'll do."
                drive(100, 0.1)
                FAKTOR = 1 if m.rot_y > 0 else -1

            elif m.rot_y < -10:
                print "Left a bit..."
                turn(-12.5, 0.1)

            elif m.rot_y > 10:
                print "Right a bit..."
                turn (12.5, 0.1)

