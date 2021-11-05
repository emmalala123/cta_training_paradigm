# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 09:00:21 2021

@author: hgerm
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 14:15:36 2019

@author: dsvedberg
"""
import time
import multiprocessing as mp
import RPi.GPIO as GPIO
import os
import datetime
import random
#import pygame

class nosePoke:
        def __init__(self,light, beam, name):
                self.light = light
                self.beam = beam
                self.name = name
                self.endtime = time.time()+1200
                GPIO.setup(self.light,GPIO.OUT)
                GPIO.setup(self.beam,GPIO.IN)

        def shutdown(self):
                print("blink shutdown")
                self.exit.set()
                
        def flashOn(self):
                GPIO.output(self.light,1)
                
        def flashOff(self):
                GPIO.output(self.light,0)
                
        #def flash(self, Hz, run):
        #        while time.time() < self.endtime:
        #                if run.value == 1:
        #                        GPIO.output(self.light,1)
        #                if run.value == 1:
        #                        time.sleep(2/Hz)
        #                        GPIO.output(self.light,0)
        #                if run.value == 1:
        #                        time.sleep(2/Hz)
        #                if run.value == 0:
        #                        GPIO.output(self.light,0)
        #                if run.value == 2:
        #                        GPIO.output(self.light,1)
        
        def isCrossed(self):
                if GPIO.input(self.beam) == 0: return True
                else: return False
                                
        def keepOut(self,wait):
                start = time.time()
                while True and time.time() < self.endtime:         
                        if self.isCrossed():
                                start = time.time()
                        elif time.time()-start > wait:
                                break                
        def kill(self):
                GPIO.output(self.light,0)
                
class trigger(nosePoke):
        def __init__(self, light, beam, name):
                nosePoke.__init__(self, light, beam, name)
                GPIO.add_event_detect(self.beam, GPIO.FALLING)
                #self.tone = pygame.mixer.Sound('pink_noise.wav')
        #def playTone(self):
        #        os.system('omxplayer --loop pink_noise.mp3 &')
        #def killTone(self):
        #        os.system('killall omxplayer.bin')

class tasteLine:
        def __init__(self,valve,intanOut,tone):
                self.valve = valve
                self.intanOut = intanOut
                #self.tone = pygame.mixer.Sound(tone)
                self.tone = tone
                self.opentime = 0.05  
                self.endtime = time.time()+1200
                GPIO.setup(self.valve,GPIO.OUT)
                GPIO.setup(self.intanOut,GPIO.OUT)
                
        #def playTone(self):
        #        #self.tone.play(-1)
        #        os.system('omxplayer --loop '+self.tone+' &')
        #def killTone(self):
        #        os.system('killall omxplayer.bin')
        def clearout(self):
                dur = input("enter a clearout time to start clearout, or enter '0' to cancel: ")
                dur = float(dur)
                if dur == 0.0:
                        print("clearout canceled")
                        return
                GPIO.output(self.valve, 1)
                time.sleep(dur)
                GPIO.output(self.valve, 0)
                print('Tastant line clearing complete.')
                
        def calibrate(self):
                opentime = input("enter an opentime (like 0.05) to start calibration: ")
                opentime = float(opentime)
                while True:
                        # Open ports  
                        for rep in range(5):
                                GPIO.output(self.valve, 1)
                                time.sleep(opentime)
                                GPIO.output(self.valve, 0)
                                time.sleep(3)
        
                        ans = input('keep this calibration? (y/n)')
                        if ans == 'y':
                                self.opentime = opentime
                                print("opentime saved")
                                break
                        else:
                                opentime = input('enter new opentime:')
                                opentime = float(opentime)
        def deliver(self):
                GPIO.output(self.valve, 1)
                GPIO.output(self.intanOut, 1)
                time.sleep(self.opentime)
                GPIO.output(self.valve, 0)
                GPIO.output(self.intanOut, 0)
        
        def kill(self):
                GPIO.output(self.valve, 0)
                GPIO.output(self.intanOut, 0)
                
        def isOpen(self):
                return GPIO.input(self.valve) == 1

def openpoke(anID,runtime):
	starttime = time.time()
	endtime = starttime+runtime*60
	rew.endtime = endtime
	trig.endtime = endtime
	ti = 5
	wait = 1
	rewRun = mp.Value("i", 0)
	trigRun = mp.Value("i", 0)
	rew.flashOn()
	trig.flashOn()
	recording = mp.Process(target = record, args = (rew,trig,lines,starttime,endtime,anID,))
	recording.start()
	state_t = 0 #keeps track of if last timepoint was triggered
	state_r = 0
	while time.time() < endtime:
		if trig.isCrossed() and state_t == 0:
			state_t = 1
			start = time.time()
			trigRun.value = 1
			lines[0].deliver()
			print("Line 0 - Delivered")
		elif not(trig.isCrossed() and state_t == 1):
			state_t = 0
			trigRun.value = 0
		if rew.isCrossed() and state_r == 0:
			state_r = 1
			rewRun.value = 1
			lines[1].deliver()
			print("Line 1 - delivered")
		elif not(rew.isCrossed() and state_r == 1):
			state_r = 0
			rewRun.value = 0

def alternate(alttime,altnum,anID):
	start_side = random.randint(0,1) #side to begin alternation
	rewRun = mp.Value("i", 0)
	trigRun = mp.Value("i", 0)
	for i in range(altnum):
		starttime = time.time()
		endtime = starttime + (alttime*60)
		if start_side == 0:
			side = "rew"
		elif start_side == 1:
			side = "trig"
		eval(side).endtime = endtime
		eval(side+"Run").value = 0
		eval(side).flashOn()
		recording = mp.Process(target = record, args = (rew,trig,lines,starttime,endtime,anID,))
		recording.start()
		state = 0 #keeps track of last timepoint state
		while time.time() < endtime:
			if eval(side).isCrossed() and state == 0:
				state = 1
				start = time.time()
				eval(side+"Run").value = 1
				lines[start_side].deliver()
				print("Line "+str(start_side)+" - Delivered")
			elif not(eval(side).isCrossed() and state == 1):
				state = 0
				eval(side + "Run").value = 0
		#side done, now to switch sides
		start_side = abs(start_side - 1)
		#reset trackers
		eval(side).flashOff()
		eval(side + "Run").value = 0
		state = 0

def hab1():
	anID = input("enter animal ID: ")
	runtime = input("enter open poke runtime in minutes: ")
	runtime = int(runtime)
	openpoke(anID,runtime)
	print("Done Hab 1")

def hab2():
	anID = input("enter animal ID: ")
	alttime = input("enter alternation time per side in minutes: ")
	alttime = int(alttime)
	altnum = input("enter number of alternations in total: ")
	altnum = int(altnum)
	print("Begin Alternate")
	alternate(alttime,altnum,anID)
	rest_start = time.time()
	end_rest = rest_start + 60
	wait = 1
	print("Begin Wait")
	while time.time() < end_rest:
		wait = 1
	print("Wait Over")
	print("Begin Alternate")
	alternate(alttime,altnum,anID)
	print("Done Hab 2")

def hab3():
	anID = input("enter animal ID: ")
	alttime = input("enter alternation time per side in minutes: ")
	alttime = int(alttime)
	altnum = input("enter number of alternations in total: ")
	altnum = int(altnum)
	print("Begin Alternate")
	alternate(alttime,altnum,anID)
	rest_start = time.time()
	end_rest = rest_start + 60
	wait = 1
	print("Begin Wait")
	while time.time() < end_rest:
		wait = 1
	print("Wait Over")
	print("Begin Alternate")
	alternate(alttime,altnum,anID)
	print("Done Hab 3")

def hab4():
	anID = input("enter animal ID: ")
	alttime = input("enter alternation time per side in minutes: ")
	alttime = int(alttime)
	altnum = input("enter number of alternations in total: ")
	altnum = int(altnum)
	runtime = input("enter open poke runtime in minutes: ")
	runtime = int(runtime)
	print("Begin Alternate")
	alternate(alttime,altnum,anID)
	rest_start = time.time()
	end_rest = rest_start + 60
	wait = 1
	print("Begin Wait")
	while time.time() < end_rest:
		wait = 1
	print("Wait Over")
	print("Begin Open Period")
	openpoke(anID,runtime)
	print("Done Hab 4")

def test():
	anID = input("enter animal ID: ")
	alttime = input("enter alternation time per side in minutes: ")
	alttime = int(alttime)
	altnum = input("enter number of alternations in total: ")
	altnum = int(altnum)
	runtime = input("enter open poke runtime in minutes: ")
	runtime = int(runtime)
	print("Begin Alternate")
	alternate(alttime,altnum,anID)
	rest_start = time.time()
	end_rest = rest_start + 60
	wait = 1
	print("Begin Wait")
	while time.time() < end_rest:
		wait = 1
	print("Wait Over")
	print("Begin Open Period")
	openpoke(anID,runtime)
	print("Done CTA Test")

def record(poke1,poke2,lines,starttime,endtime,anID):
        now = datetime.datetime.now()
        d = now.strftime("%m%d%y") #all same-day same-animal concatenated to 1 file
        localpath = os.getcwd()
        filepath = localpath+"/"+anID+"_"+d+".csv"
        file = open(filepath,"a")
        if os.stat(filepath).st_size == 0:
                file.write("Time,Poke1,Poke2,Line1,Line2,Line3,Line4\n")
        while time.time() < endtime:
                t = round(time.time()-starttime,2)
                file.write(str(t)+","+str(poke1.isCrossed())+","+str(poke2.isCrossed())+","+str(lines[0].isOpen())+","+str(lines[1].isOpen())+","+str(lines[2].isOpen())+","+str(lines[3].isOpen())+"\n")
                file.flush()
                time.sleep(0.1)
        file.close()

def killAll():
	GPIO.cleanup()
	#os.system("killall omxplayer.bin")
        
def main_menu():       ## Your menu design here
        options = ["clearout a line","calibrate a line","hab1","hab2","hab3","hab4","test","exit"]
        print(30 * "-" , "MENU" , 30 * "-")
        for idx,item in enumerate(options):
                print(str(idx+1)+". "+item)
        print(67 * "-")
        choice = input("Enter your choice [1-"+str(len(options))+"]: ")
        choice = int(choice)
        return choice

def clearout_menu():
        while True:
                for x in range(1,5):
                        print(str(x)+". clearout line "+str(x))
                print("5. main menu")
                line = input("enter your choice")
                line = int(line)
                if line in range(1,6):
                        return(line-1)
                else:
                        print("enter a valid menu option")
                        
def calibration_menu():
        while True:
                for x in range(1,5):
                        print(str(x)+". calibrate line "+str(x))
                print("5. main menu")
                line = input("enter your choice")
                line = int(line)
                if line in range(1,6):
                        return(line-1)
                else:
                        print("enter a valid menu option")

##main##

#pygame.mixer.pre_init(22100, -16, 2, 512)
#pygame.mixer.init()  
#pygame.init()
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
tasteouts = [31,33,35,37]
intanouts = [24,26,19,21]
rew = nosePoke(36,11,'reward')
trig = trigger(38,13,'trigger')
rew.flashOff()
trig.flashOff()
tones = ['1000hz_sine.mp3','3000hz_saw.mp3','5000hz_square.mp3','7000hz_unalias.mp3']
lines = [tasteLine(tasteouts[i],intanouts[i],tones[i]) for i in range(4)]

while True:     
        ## While loop which will keep going until loop = False
        choice = main_menu()    ## Displays menu
        choice = int(choice)
        if choice > 0 and choice < 9:
                if choice ==1:
                        while True:
                                line = clearout_menu()
                                if line in range(4):
                                        lines[line].clearout()
                                elif line == 4:
                                        break
                elif choice==2:     
                        while True:
                                line = calibration_menu()
                                if line in range(4):
                                        lines[line].calibrate()
                                elif line == 4:
                                        break               
                elif choice==3:
                        print("starting hab1")
                        hab1()
                elif choice == 4:
                        print("starting hab2")
                        hab2()
                elif choice == 5:
                        print("starting hab3")
                        hab3()
                elif choice == 6:
                        print("starting hab4")
                        hab4()
                elif choice == 7:
                        print("starting test")
                        test()
                elif choice == 8:
                        print("program exit")
                        GPIO.cleanup()
                        #pygame.mixer.quit()
                        #os.system('killall omxplayer.bin')
                        break
                        
        else:
                print("please enter a number: ")
                
		
