"""
This function tests the system to make sure the entire program isn't being held-up by hardware.
"""
import NosePoke as NosePoke

def menu():
    options = ["flash", "poke crossed", "deliver functionality"]
    for i, item in options:
        print(str(i + 1), ".", item)
    choice = int(input("please enter a test value: "))
    print("option", choice, "selected")
    return choice

        
        
class CheckPoke:
    def __init__(self, nose_poke):
        self.nose_poke = nose_poke
    
        
    def test_flash(self):
        self.nose_poke.flash()
        
    def is_crossed(self):
        print(self.nose_poke.isCrossed())
        
    def deliver(self):
        print("reading open status", self.nose_poke.isOpen())
        return self.nose_poke.deliver()
        
    
    

nosePoke = CheckPoke(NosePoke)
        