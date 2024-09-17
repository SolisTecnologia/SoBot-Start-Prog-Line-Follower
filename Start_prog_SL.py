#!/usr/bin/python3
"""
Solis Robot - SoBot

Controle_F710_Logitech.py: Programming example to control the "SoBot"
using the Logitech F710 controller once Raspberry is turned on.

Created By   : Vinicius M. Kawakami
Version      : 1.0

Company: Solis Tecnologia

Controller button functions:
BTN_X – Configure LED Strip in Blue color
BTN_Y – Configure LED Strip in Yellow color
BTN_A – Configure LED Strip in Green color
BTN_B – Configure LED Strip in Red color
BTN_START – Enables wheel motors
BTN_BACK – Enable and Disables line follower mode
BTN_R1 – Configure curve mode on the same axis
BTN_L1 – Configure differential curve mode
BTN_R2 – Sets speed 8cm/s
BTN_L2 – Sets speed 4cm/s
BTN_UP – Moves the robot forward
BTN_DOWN – Moves the robot backwards
BTN_LEFT – Moves the robot to the left
BTN_RIGTH – Moves the robot to the right

"""

import inputs
import serial
from time import sleep, time
import threading
import signal
import sys
import pygame
import os
import multiprocessing

'''
###################################
        Global Variables
###################################
'''

flag_init_read_line = 0

flag_BTX_press = 0
flag_BTY_press = 0
flag_pause = 0


'''
###################################
        Auxiliary Functions
###################################
'''

def Timer_BTX_Press ():
    global flag_BTX_press
    flag_BTX_press = 0

def Timer_BTY_Press ():
    global flag_BTY_press
    flag_BTY_press = 0

def Timer_Pause ():
    global flag_pause
    global flag_BTX_press
    global flag_BTY_press
    flag_pause = 0
    if flag_BTY_press == 2:
        usb.write(b"MT0 MP")
        threading.Timer(0.1, Timer_BTY_Press).start()
    elif flag_BTX_press == 2:
        usb.write(b"MT0 MP")
        threading.Timer(0.1, Timer_BTX_Press).start()

# Function to handle script termination signal
def handle_signal(signum, frame):
    usb.write(b"MT0 ME0")   # Disable motors
    usb.write(b"LT E0")     # Turn off Led Tap
    sys.exit(0)             # End the script

def stop_read_line ():
    global flag_init_read_line

    print("stop read line")
    flag_init_read_line = 0

    usb.write(b"LT E1 RD0 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD50 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD0 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD50 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD0 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD50 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD0 GR0 BL0")
    usb.write(b"LT E0")
    sleep(0.5)
    usb.write(b"MT0 MC MD0 AT100 DT100 V8")
    usb.write(b"LT E1 RD0 GR100 BL0")   # Turn on Led Tap


'''
###################################
Function created to read Logitech control commands
###################################
'''
def Read_Gamepad(ev_read_line, ev_stop_read_line, usb):

    global flag_pause
    global flag_BTX_press
    global flag_BTY_press
    flag_start = 0
    flag_vel = 1
    flag_BT_RZ = 0
    flag_BT_Z = 0

    # Find the Logitech F710 controller ID connected to the Raspberry Pi
    gamepad = inputs.devices.gamepads[0]
    print(gamepad)


    while True:
        
        events = inputs.get_gamepad()   # Checks if there was any control event
        print(f"Eventos: {events}")

        for event in events:
            
            # Checks if it is event of type "KEY"
            if event.ev_type == "Key":
                print(f"Evento code: {event.code}")
                print(f"Evento state: {event.state}")

                # Check if the event code is "BTN_SELECT" in state 1
                if event.code == "BTN_SELECT":
                    if ev_stop_read_line.is_set() == 0 and event.state == 1:
                        print("Botão Select pressionado")
                        usb.write(b"LT E1 RD100 GR100 BL100")       # Turn on Led Tap
                        usb.write(b"MT0 MC MD1 RI20 AT50 DT50 V6")  # Parameter settings for continuous mode
                        usb.write(b"MT0 ME1")                       # Enables wheel motors on mode continuous
                        ev_read_line.set()

                    elif ev_stop_read_line.is_set() and event.state == 1:
                        print("Botão Select pressionado")
                        usb.write(b"MT0 MP")                # Moviment Pause
                        usb.write(b"MT0 ME0")               # Disables wheel motors on mode continuous
                        stop_read_line ()
                        ev_stop_read_line.clear()
                        ev_read_line.clear()

                if ev_stop_read_line.is_set() == 0:
                    # Check if the event code is "BTN_START" in state 1
                    if event.code == "BTN_START" and event.state == 1:
                        print("Botão Start pressionado")
                        if flag_start == 0:
                            flag_start = 1
                            usb.write(b"MT0 ME1")               # Enable motors
                            usb.write(b"LT E1 RD0 GR0 BL100")   # Turn on Led Tap

                        else:
                            flag_start = 0
                            usb.write(b"MT0 ME0")               # Disable motors
                            usb.write(b"LT E1 RD0 GR100 BL0")   # Turn on Led Tap

                    # Check if the event code is "BTN_SOUTH" in state 1
                    if event.code == "BTN_SOUTH" and event.state == 1:
                        print("Botão A pressionado")
                        usb.write(b"LT E1 RD0 GR100 BL0")   # Turn on Led Tap

                    # Check if the event code is "BTN_EAST" in state 1
                    elif event.code == "BTN_EAST" and event.state == 1:
                        print("Botão B pressionado")
                        usb.write(b"LT E1 RD100 GR0 BL0")   # Turn on Led Tap

                    # Check if the event code is "BTN_NORTH" in state 1
                    elif event.code == "BTN_NORTH" and event.state == 1:
                        print("Botão X pressionado")
                        usb.write(b"LT E1 RD0 GR0 BL100")   # Turn on Led Tap

                    # Check if the event code is "BTN_WEST" in state 1
                    elif event.code == "BTN_WEST" and event.state == 1:
                        print("Botão Y pressionado")
                        usb.write(b"LT E1 RD100 GR50 BL0")   # Turn on Led Tap

                    # Check if the event code is "BTN_TR" in state 1
                    elif event.code == "BTN_TR" and event.state == 1:
                        print("Botão RB pressionado")
                        # Configure continuous mode with curve on the same axis
                        if flag_vel:
                            usb.write(b"MT0 MC MD0 AT100 DT100 V8")
                        else:
                            usb.write(b"MT0 MC MD0 AT100 DT100 V4")

                    # Check if the event code is "BTN_TL" in state 1
                    elif event.code == "BTN_TL" and event.state == 1:
                        print("Botão LB pressionado")
                        # Configure continuous mode with differential curve
                        if flag_vel:
                            usb.write(b"MT0 MC MD1 RI100 AT100 DT100 V8")
                        else:
                            usb.write(b"MT0 MC MD1 RI100 AT100 DT100 V4")

            # Checks if it is event of type "Absolute"
            if event.ev_type == "Absolute":
                print(f"Evento code: {event.code}")
                print(f"Evento state: {event.state}")

                if ev_stop_read_line.is_set() == 0:
                    ### Buttons to control the direction ###
                    # Events with the MODE button disabled
                    # Check if the event code is "ABS_HAT0X"
                    if event.code == "ABS_HAT0X":
                        if flag_start:                  # Check if flag_start is enable
                            if flag_BTY_press == 0 and flag_BTX_press == 0:
                                if event.state == -1:       # Check state (left direction) of the button
                                    flag_BTX_press = 1
                                    flag_pause = 1
                                    print("Botão ESQ pressionado")
                                    usb.write(b"MT0 ML")
                                    threading.Timer(0, Timer_Pause).start()

                                elif event.state == 1:      # Check state (right direction) of the button
                                    flag_BTX_press = 1
                                    flag_pause = 1
                                    print("Botão DIR pressionado")
                                    usb.write(b"MT0 MR")
                                    threading.Timer(0, Timer_Pause).start()

                            elif flag_BTX_press == 1:
                                if event.state == 0:
                                    flag_BTX_press = 2
                                    if flag_pause == 0:
                                        usb.write(b"MT0 MP")
                                        threading.Timer(0, Timer_BTX_Press).start()

                    # Check if the event code is "ABS_HAT0Y"
                    if event.code == "ABS_HAT0Y":
                        if flag_start:                  # Check if flag_start is enable
                            if flag_BTX_press == 0 and flag_BTY_press == 0:
                                if event.state == -1:       # Check state (front direction) of the button
                                    flag_BTY_press = 1
                                    flag_pause = 1
                                    print("Botão FRENTE pressionado")
                                    usb.write(b"MT0 MF")
                                    threading.Timer(0, Timer_Pause).start()

                                elif event.state == 1:      # Check state (back direction) of the button
                                    flag_BTY_press = 1
                                    flag_pause = 1
                                    print("Botão TRAS pressionado")
                                    usb.write(b"MT0 MB")
                                    threading.Timer(0, Timer_Pause).start()

                            elif flag_BTY_press == 1:
                                if event.state == 0:
                                    flag_BTY_press = 2
                                    if flag_pause == 0:
                                        usb.write(b"MT0 MP")
                                        threading.Timer(0, Timer_BTY_Press).start()
                    
                    ### Buttons to control the velocity ###
                    # Check if the event code is "ABS_RZ"
                    if event.code == "ABS_RZ":
                        if event.state >= 1:            # Check if state is greater than 1 (button pressed)
                            if flag_BT_RZ == 0:
                                flag_BT_RZ = 1
                                flag_vel = 1
                                print("Botão RZ pressionado")
                                usb.write(b"MT0 MC MD0 AT100 DT100 V8")
                        elif event.state == 0:
                            print("Botão RZ solto")
                            flag_BT_RZ = 0

                    # Check if the event code is "ABS_Z"
                    if event.code == "ABS_Z":
                        if event.state >= 1:            # Check if state is greater than 1 (button pressed)
                            if flag_BT_Z == 0:
                                flag_BT_Z = 1
                                flag_vel = 0
                                print("Botão Z pressionado")
                                usb.write(b"MT0 MC MD0 AT100 DT100 V4")
                        elif event.state == 0:
                            print("Botão Z solto")
                            flag_BT_Z = 0


'''
###################################
Function created to read the line sensor
###################################
'''
def Read_Line(ev_read_line, ev_stop_read_line, usb):

    data_line = [48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48]
    flag_fw = 0
    flag_lt = 0
    flag_rh = 0
    flag_read_line = 0

    count = 0
    count_S1 = 0
    count_S2 = 0
    count_S3 = 0
    pos_S1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    pos_S2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    pos_S3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    pygame.mixer.init()
    start_sound = '/home/pi/Documentos/Projetos/Demo/Start_prog'
    selected_music1 = os.path.join(start_sound, 'Frase_Start-Sobot.mp3')
    selected_music2 = os.path.join(start_sound, 'SL_Ativado.mp3')
    selected_music3 = os.path.join(start_sound, 'SL_Desativado.mp3')
    pygame.mixer.music.load(selected_music1)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass

    while True:

        if ev_read_line.is_set():

            flag_read_line = 1
            if ev_stop_read_line.is_set() == 0:
                ev_stop_read_line.set()
                flag_fw = 0
                flag_lt = 0
                flag_rh = 0
                pygame.mixer.music.load(selected_music2)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pass
                sleep(1)

            usb.write(b"SL")            # Send command to read line sensor
            #sleep(0.1)                 # Wait to return datas
            while(usb.in_waiting == 0):
                pass
            if(usb.in_waiting):
                data_line = usb.readline()  # Read data
                #print(data_line)

                if data_line[0] == 83 and data_line[1] == 76:     # Verifica se é "S" e "L"
                    if count >= 20:
                        count = 0                    

                    #print(str(count))
                    pos_S1[count] = data_line[4] - 48
                    pos_S2[count] = data_line[10] - 48
                    pos_S3[count] = data_line[16] - 48
                    count += 1

                    count_S1 = pos_S1[0]+pos_S1[1]+pos_S1[2]+pos_S1[3]+pos_S1[4]+pos_S1[5]+pos_S1[6]+pos_S1[7]+pos_S1[8]+pos_S1[9]+pos_S1[10]+pos_S1[11]+pos_S1[12]+pos_S1[13]+pos_S1[14]+pos_S1[15]+pos_S1[16]+pos_S1[17]+pos_S1[18]+pos_S1[19]
                    count_S2 = pos_S2[0]+pos_S2[1]+pos_S2[2]+pos_S2[3]+pos_S2[4]+pos_S2[5]+pos_S2[6]+pos_S2[7]+pos_S2[8]+pos_S2[9]+pos_S2[10]+pos_S2[11]+pos_S2[12]+pos_S2[13]+pos_S2[14]+pos_S2[15]+pos_S2[16]+pos_S2[17]+pos_S2[18]+pos_S2[19]
                    count_S3 = pos_S3[0]+pos_S3[1]+pos_S3[2]+pos_S3[3]+pos_S3[4]+pos_S3[5]+pos_S3[6]+pos_S3[7]+pos_S3[8]+pos_S3[9]+pos_S3[10]+pos_S3[11]+pos_S3[12]+pos_S3[13]+pos_S3[14]+pos_S3[15]+pos_S3[16]+pos_S3[17]+pos_S3[18]+pos_S3[19]

                    print("C_S1: " + str(count_S1) + " C_S2: " + str(count_S2) + " C_S3: " + str(count_S3))

                    if count_S1 == 0 and count_S2 > 0 and count_S3 == 0:
                        if(flag_fw == 0):
                            flag_fw = 1
                            flag_lt = 0
                            flag_rh = 0
                            usb.write(b"LT E1 RD20 GR70 BL30")
                            usb.write(b"MT0 MC MD1 RI20 AT50 DT50 V6")
                            usb.write(b"MT0 MF")    # Moving to forward
                            print(time())
                            sleep(0.1)
                            print("forward")

                    elif count_S1 == 0 and count_S2 == 0 and count_S3 == 0:
                        ev_stop_read_line.clear()
                        ev_read_line.clear()
                        usb.write(b"MT0 MP")                # Moviment Pause
                        usb.write(b"MT0 ME0")               # Disables wheel motors on mode continuous
                        stop_read_line ()

                    else:
                        if count_S1 >= 3 and count_S2 > 0 and count_S3 == 0:      # Condição para corrigir virando a esquerda
                            if flag_lt == 0:
                                flag_lt = 1
                                flag_fw = 0
                                flag_rh = 0
                                usb.write(b"MT0 MC MD1 RI20 AT50 DT50 V5")
                                usb.write(b"MT0 ML")        # Turn left
                                print(time())
                                sleep(0.15)
                                print("send left")

                        if count_S1 == 0 and count_S2 > 0 and count_S3 >= 3:      # Condição para corrigir virando a direita
                            if flag_rh == 0:
                                flag_lt = 0
                                flag_fw = 0
                                flag_rh = 1
                                usb.write(b"MT0 MC MD1 RI20 AT50 DT50 V5")
                                usb.write(b"MT0 MR")        # Turn rigth
                                print(time())
                                sleep(0.15)
                                print("send rigth")

                    data_line = [48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48]
        else:
            if flag_read_line:
                flag_read_line = 0
                print("SL_Desativado")
                pygame.mixer.music.load(selected_music3)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pass


'''
###################################
        Main function
###################################
'''
if __name__ == '__main__':
    # Configure the serial port
    usb = serial.Serial('/dev/ttyACM0', 57600, timeout=0, dsrdtr=False)
    usb.flush()

    # Function registration for handling "SIGTERM" signal
    signal.signal(signal.SIGTERM, handle_signal)

    # Configure wheel parametres
    usb.write(b"WP MT1 WD100,06")
    usb.write(b"WP MT2 WD100,09")
    usb.write(b"WP DW270,13")

    # Set the motion proportional gain
    #usb.write(b"PG SO2,3 CA3,22 DF6,11 RI-6")

    # Configure operating parametres in continuous mode
    usb.write(b"MT0 MC MD0 AT100 DT100 V8")

    usb.write(b"LT E1 RD0 GR100 BL0")   # Turn on Led Tap

    ev_read_line = multiprocessing.Event()          # Event to indicate line reading
    ev_stop_read_line = multiprocessing.Event()     # Event to indicate pause in line reading

    app_Read_Gamepad = multiprocessing.Process(target=Read_Gamepad,args=(ev_read_line, ev_stop_read_line, usb))
    app_Read_Line = multiprocessing.Process(target=Read_Line,args=(ev_read_line, ev_stop_read_line, usb))

    app_Read_Gamepad.start()
    app_Read_Line.start()

# Let CTRL+C actually exit