# main_menu() shows the user the main menu and receives input
def main_menu():
    options = ["clearout a line", "calibrate a line", "hab",
               "exit"]
    print(67 * "-")
    print("MAIN MENU")
    for idx, item in enumerate(options):
        print(str(idx + 1) + ". " + item)
    print(67 * "-")
    choice = int(input("Enter your choice [1-" + str(len(options)) + "]: "))
    print("option "+str(choice) + " selected")
    return choice