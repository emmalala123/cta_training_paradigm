"""
This class controls the habituation program, this function is pulled from the main.py program.
"""
import time
import multiprocessing as mp
import RPi.GPIO as GPIO
import os
import random
from NosePoke import NosePoke
from TasteLine import TasteLine
from record import record

def hab(wait, crosstime, iti, lines, trig, rew, rewardtrigger):
    anID = input("enter animal ID: ")
    runtime = input("enter runtime in minutes: ")
    starttime = time.time()
    endtime = starttime+float(runtime)*60
    rew.endtime = endtime
    trig.endtime = endtime
    Hz = 3.9

    rewRun = mp.Value("i", 0)
    trigRun = mp.Value("i", 0)

    rewFlash = mp.Process(target=rew.flash, args=(Hz, rewRun,))
    trigFlash = mp.Process(target=trig.flash, args=(Hz, trigRun,))
    recording = mp.Process(target=record, args=(
        rew, trig, lines, starttime, endtime, anID,))

    rewFlash.start()
    trigFlash.start()
    recording.start()

    state = 0
    while time.time() < endtime:
        while state == 0:  # state 0: initialize/prime trigger
            rewKeepOut = mp.Process(target=rew.keep_out, args=(iti,))
            trigKeepOut = mp.Process(target=trig.keep_out, args=(iti,))
            rewKeepOut.start()
            trigKeepOut.start()

        #     line = random.randint(0, 3)  # select random taste
            rewKeepOut.join()
            trigKeepOut.join()
        #   trig.playTone()
            print("new trial")
            trigRun.value = 1
            state = 1

        while state == 1:  # state 1: start trial/trip
            if trig.is_crossed():
                print("state 2")
                # trig.killTone()
                # lines[line].playTone()
                start = time.time()
                state = 2

            while state == 2:  # state 2: trigger trigger/prime reward
                if trig.is_crossed() and time.time() > wait+start:
                    trigRun.value = 0
                    rewRun.value = 1
                    deadline = time.time()+crosstime
                    start = time.time()
                    state = 3
                    if rewardtrigger == 1:
                        lines[1].deliver()
                    print("state 3")
                if not trig.is_crossed():
                    trigRun.value = 0
                #     lines[line].killTone()
                    state = 0
                    print("state 0")

            while state == 3:
                if not rew.is_crossed():
                    start = time.time()
                if rew.is_crossed() and time.time() > start+wait:
                #     lines[line].killTone()
                    rewRun.value = 0
                    lines[0].deliver()
                    print("reward delivered")
                    state = 0
                if time.time() > deadline:
                #     lines[line].killTone()
                    rewRun.value = 0
                    state = 0

#     trig.killTone()
#     lines[line].killTone()
    recording.join()
    rewFlash.join()
    trigFlash.join()
    print("assay completed")