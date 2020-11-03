
class Token:
    def __init__(self, type, attribute):
        self.type = type
        self.attribute = attribute

    def to_string(self):
        return "<" + self.type + ", " + str(self.attribute) + ">"