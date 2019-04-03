from sr.robot import * #mengimport semua fungsi student robot

import time         #menimport library time untuk membuat delay dan penghitungan waktu
TIME = time.time()  #menyimpan waktu saat robot belum berjalan
R = Robot()

def drive(speed): #definisi fungsi untuk gerak maju
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed

def turn(speed): #definisi fungsi untuk berputar
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed

FIND, HOME = range(2)   #state FIND = mencari token, HOME = kembale ke tempat awal
DERAJAT = 5             #Konstanta cakupan pandangan untuk menentukan maju atau berputar

state = FIND    #Dimulai dengan mencari token

while True:
    FAKTOR = 0 if state == FIND else -12    #Faktor koreksi, 0 = benda tepat di depan robot ketika maju, -12 = benda 12 derajat sebelah kanan robot 

    marker,offset = (MARKER_TOKEN_C,1) if state == FIND else (MARKER_ARENA,21)  # Menentukan benda yang dituju. FIND -> TOKEN_C_1 dan HOME -> ARENA_21
    tokens = filter(lambda m: m.info.marker_type == marker and 
                        m.info.offset == offset ,R.see())   #Melakukan filter terhadap apa yang dilihat apakah sesuai dengan marker yang dicari.
    
    if len(tokens) < 1: #Jika tidak melihat token atau arena yang dicari maka berputar
        turn(-100)
    else:
        m = tokens[0]                       #Jika ditemukan, maka m = benda pertama yang sesuai.
        DIST = .4 if state == FIND else 1   #DIST = jarak antara benda yang dicari dan robot. FIND -> 0,4 dan HOME -> 1
        if m.dist < DIST:
            if state == FIND:               #Jarak lebih dekat dari DIST dan state FIND maka tangkap token (R.grab())
                if R.grab():
                    state = HOME            #State berubah menjadi HOME = kembali ke tempat semula.
            else:                           #Jika dekat dengan ARENA 21 maka lakukan ini (agar tepat di tempat semula)
                drive(0)
                turn(-100)
                time.sleep(.1)
                drive(75)
                time.sleep(1)
                drive(0)                    #Berhenti di tempat semula
                print time.time()-TIME      #Menampilkan waktu yang digunakan sampai kembali ke tempat awal
                exit()                      #Selesai
 
        elif -DERAJAT <= m.rot_y+FAKTOR <= DERAJAT: #Jika dalam rentang derajat maka maju
            drive(100)
        elif m.rot_y +FAKTOR < -DERAJAT:    #Jika disebelah kiri maka putar ke kenan
            turn(-50)
        elif m.rot_y +FAKTOR > DERAJAT:     #Jika disebelah kanan maka putar ke kiri
            turn(50)