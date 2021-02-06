'''

opt 1: take an input and use google api to recognize it as italian/english
opt 2: make a general Language class X

'''

class Language():
    # english command -> id
    DEFAULT_COMMANDS = {"search":0, 
                        "google": 1, 
                        'music': 2, 
                        'playlist': 3,
                        'pause':4,
                        'resume':5,
                        'skip':6,
                        'volume':7,
                        'screenshot':8}

    DEFAULT_ACTIVATORS = ["friday", "activate"]
    DEFAULT_DEACTIVATORS = ["deactivate", "sleep"]

    def __init__(self):
        self.commands = {} # translated -> english
        self.name = "English"
        self.rec_id = 'en-US' # id of the language to recognize the voice (ex: 'en-US')
        self.speech_id = 'en' # id of the language to speak (ex: 'it')
        self.activators = []
        self.deactivators = []
    
    def load(self, filename):
        with open("languages\\" + filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # remove empty lines and clean '\n' at the end
        rem = []
        for idx in range(len(lines)):
            if lines[idx] == '\n':
                rem.append(lines[idx])
            else:
                lines[idx] = lines[idx].replace('\n', '')
            
        for line in rem:
            lines.remove(line)
    
        '''
            0 -> reading the default name and properties of the language
            1 -> reading commands
            2 -> reading activators
            3 -> reading deactivators
        ''' 
        state = 0

        self.name = lines[0]
        self.rec_id = lines[1]
        self.speech_id = lines[2]

        for line in lines[3:]:
            words = line.lower().split()
            if words[0][0] == '[':
                section = words[0][1:-1]
                if section == 'commands':
                    state = 1
                elif section == 'activators':
                    state = 2
                elif section == 'deactivators':
                    state = 3
                continue

            translation = words[0]
            try:
                eng = words[1] 
            except IndexError:
                pass

            if state == 1:
                self.commands[translation] = self.DEFAULT_COMMANDS[eng]
            elif state == 2:
                self.activators.append(translation)
            elif state == 3:
                self.deactivators.append(translation)
    
    # (to the command in english)
    def get_translation(self, command):
        return self.DEFAULT_COMMANDS[self.commands[command]]

    # to the id of the command
    def get_command_id(self, command):
        try:
            return self.commands[command]
        except KeyError:
            return "Not a valid command!"

    def is_command(self, word):
        return word in self.commands

    def is_activator(self, word):
        return word in self.activators

    def is_deactivator(self, word):
        return word in self.deactivators

    def __str__(self):
        res = "Name: " + self.name + "\nRecognition Id: " + str(self.rec_id) + "\n" + "Speaking id: " + self.speech_id + "\n"
        res += "\nCommands:\n" + '\n'.join(self.commands)
        res += "\n\nActivators:\n" + '\n'.join(self.activators)
        res += "\n\nDeactivators:\n" + '\n'.join(self.deactivators)
        return res