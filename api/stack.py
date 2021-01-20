

class Stack:
    def __init__(self, entries=[]):
        self.entries = entries


    def add(self, name):
        entry = {name: {
            "type": "",
            "label": "",
            "shift": 0,
            "param_count": 0,
            "param_type": [],
            "return_type": ""
        }}

        if type(entry) == list:
            self.entries += list(reversed(entry))
        else:
            self.entries.append(entry)


    def pop(self):
        return self.entries.pop()

    
    def find(self, key):
        for entry in reversed(self.entries):
            key_ = list(entry.keys())[0]
            
            if key_ == key:
                return entry[key_]

        return False

    
    def set(self, name, attr, value):
        self.find(name)[attr] = value


    def copy(self):
        return Stack(self.entries.copy())

    
    def get_element(self, index):
        return list(self.entries[-index].keys())[0]
