"""
This class controls the taste line valves (31, 33, 35, 37), functions include bool value readings, calibration, clearout, deliver, and kill
"""
import RPi.GPIO as GPIO
import time

class TasteLine:
    def __init__(self, valve, intan_out, opentime, taste):
        self.valve = valve  # GPIO pin number corresponding to the valve controlling taste delivery
        self.intan_out = intan_out  # GPIO pin number used to send a signal to our intan neural recording system
        # whenever a taste is delivered.
        self.opentime = opentime  # how long the valve stays open for one single delivery
        self.taste = taste  # string containing name of the corresponding taste, used for datalogging in record()

        # generating a tasteLine object automatically sets up the GPIO pins:
        GPIO.setup(self.valve, GPIO.OUT)
        GPIO.setup(self.intan_out, GPIO.OUT)

    def clearout(self):  # when starting up the rig, we need to clear the air from the tubes leading to the taste
        # delivery system, and clean out the tubes when we are done. clearout() prompts user to input how long the
        # valve should be open to clear the tube, and then clears out the tube for that duration.
        dur = float(input("enter a clearout time to start clearout, or enter '0' to cancel: "))
        print("clearout = " + str(dur) + "s")
        if dur == 0:
            print("clearout canceled")
            return
        print("clearout started")
        GPIO.output(self.valve, 1)
        time.sleep(dur)
        GPIO.output(self.valve, 0)
        print("clearout complete")

    def calibrate(self):  # when starting the rig, we need to calibrate how long valves should stay open for each
        # delivery, to ensure amount of liquid delivered is consistent from session to session. calibrate() prompts
        # user to input a calibration time, and then opens the valve 5 times for that time, so the user can weigh out
        # how much liquid is dispensed per delivery.
        opentime = float(input("enter an opentime (like 0.05) to start calibration: "))
        while True:
            # Open ports
            for rep in range(5):
                GPIO.output(self.valve, 1)
                time.sleep(opentime)
                GPIO.output(self.valve, 0)
                time.sleep(3)
            ans = input('keep this calibration? (y/n): ')
            if ans == 'y':
                self.opentime = opentime
                print("opentime saved")
                break
            else:
                opentime = int(input('enter new opentime: '))

    def deliver(self):  # deliver() is used in the context of a task to open the valve for the saved opentime to
        # deliver liquid through the line
        print("taste "+str(self.valve)+" open")
        GPIO.output(self.valve, 1)
        GPIO.output(self.intan_out, 1)
        time.sleep(self.opentime)
        GPIO.output(self.valve, 0)
        GPIO.output(self.intan_out, 0)
        print("taste "+str(self.valve)+" closed")

    def kill(self):
        GPIO.output(self.valve, 0)
        GPIO.output(self.intan_out, 0)

    @property                                                             # what is property doing here? (comment this out and test it)
    def is_open(self):  # reports if valve is open
        if GPIO.input(self.valve):
            return True
        else:
            return False
