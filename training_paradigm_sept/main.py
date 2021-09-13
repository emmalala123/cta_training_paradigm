"""
This is the main program that integrates all the classes and functions to control the training paradigm.
"""
import os
import RPi.GPIO as GPIO
import configparser
import json
from system_report import system_report
from main_menu import main_menu
from calibration_menu import calibration_menu
from clearout_menu import clearout_menu
from hab import hab
from TasteLine import TasteLine
from NosePoke import NosePoke

if __name__=="__main__":
    # set up raspi GPIO board.
    GPIO.setwarnings(False)
    GPIO.cleanup() #turn off any GPIO pins that might be on
    GPIO.setmode(GPIO.BOARD)

    # load configs
    config = configparser.ConfigParser()  # initialize configparser to read config file
    config.read("hab_config.ini")  # read config file
    opentimes = json.loads(config.get("tastelines", "opentimes"))  # load into array times to open valves when taste delivered
    tastes = json.loads(config.get("tastelines", "tastes"))  # load taste labels into list

    ## initialize objects used in task:
    # initialize tastelines w/tones
    tasteouts = [31, 33, 35, 37]  # GPIO pin outputs to taste valves. Opens the valve while "1" is emitted from GPIO,
    # closes automatically with no voltage/ "0"
    intanouts = [24, 26, 19, 21]  # GPIO pin outputs to intan board (for marking taste deliveries in neural data). Sends
    # signal to separate device while "1" is emitted.
    #tones = ["1000hz_sine.wav", "3000hz_square.wav", "5000hz_saw.wav", "7000hz_unalias.wav"]  # filenames of tones
    # initialize taste-tone objects:
    lines = [TasteLine(tasteouts[i], intanouts[i], opentimes[i], tastes[i]) for i in range(4)]

    # initialize nosepokes:
    rew = NosePoke(36, 11)  # initialize "reward" nosepoke. "Rew" uses GPIO pins 38 as output for the light, and 11 as
    # input for the IR sensor. For the light, 1 = On, 0 = off. For the sensor, 1 = uncrossed, 0 = crossed.
    trig = NosePoke(38, 13)  # initialize "trigger" trigger-class nosepoke. GPIO pin 38 = light output,
    # 13 = IR sensor input. Trigger is a special NosePoke class with added methods to control a tone.
    rew.flash_off()  # for some reason these lights come on by accident sometimes, so this turns off preemptively
    trig.flash_off()  # for some reason these lights come on by accident sometimes, so this turns off preemptively

    # This loop executes the main menu and menu-options
    while True:
        ## While loop which will keep going until loop = False
        system_report(lines)  # Displays valve opentimes and taste-line assignments
        choice = main_menu()  # Displays menu options
        try:
            if choice == 1:  # run clearout menu & clearout programs
                while True:
                    line = clearout_menu()
                    if line in range(4):
                        lines[line].clearout()
                    elif line == 4:
                        break
            elif choice == 2:  # run calibration menu & calibration programs
                while True:
                    line = calibration_menu()
                    if line in range(4):
                        lines[line].calibrate()
                    elif line == 4:
                        break
                    else:
                        print("input a valid line number")
                        break

                    opentimes[line] = lines[line].opentime
                    config.set('tastelines', 'opentimes', str(opentimes))
                    with open('cuedtaste_config.ini',
                            'w') as configfile:  # in python 3+, 'w' follows filename, while in python 2+ it's 'wb'
                        config.write(configfile)

            elif choice == 3:  # run the actual program
                    print("starting hab1")
                    wait = float(input("please enter wait period: "))
                    crosstime = float(input("please enter time for crossing: "))
                    iti = input("please enter iti: ")
                    rewardtrigger = 1
                    hab(wait, crosstime, iti, lines, trig, rew, rewardtrigger)
            elif choice == 4:
                    print("program exit")
                    GPIO.cleanup()
                    #pygame.mixer.quit()
                    os.system('killall omxplayer.bin')
                    break
                        
        except ValueError:
                print("please enter a number: ")
                
