"""
calibration_menu() runs a submenu of main_menu() for navigating calibration of taste valves.
"""
def calibration_menu():
    while True:
        for x in range(1, 5):
            print(str(x) + ". calibrate line " + str(x))
        print("5. main menu")
        line = int(input("enter your choice: "))
        if line in range(1, 6):
            return line - 1
        else:
            print("enter a valid menu option")