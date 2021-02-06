import speech

class Activator:

    def __init__(self, lang):
        self.active = True
        self.activators = lang.activators
        self.deactivators = lang.deactivators

    # determines whether what has been said activates friday
    # returns the index of the activating word, so what's following can be
    # interpreted as a command
    def process(self, text):
        activator_idx = 0
        for idx in range(len(text)):
            if text[idx] in self.activators:
                self.active = True
                activator_idx = idx
                print("Activated")
                break
            elif text[idx] in self.deactivators:
                self.active = False
                print("Deactivated")
                break
        return activator_idx
        
                
