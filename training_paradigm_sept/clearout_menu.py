"""
clearout_menu() runs a submenu of main_menu() for navigating clearouts of taste tubes.
"""
def clearout_menu():
    while True:
        for x in range(1, 5):
            print(str(x) + ". clearout line " + str(x))
        print("5. main menu")
        line = int(input("enter your choice: "))
        if line in range(1, 6):
            print("line "+str(line)+" selected")
            return (line - 1)
        else:
            print("enter a valid menu option")