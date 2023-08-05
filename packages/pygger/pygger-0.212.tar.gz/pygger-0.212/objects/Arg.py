class Arg:
    """
    Attributes:
        name (str): description
        type (str): description
    """
    def __init__(self, raw: str):
        spl = raw.split(':')
        if len(spl) < 2:
            self.name = ''
            self.type = ''
        else :
            self.name = raw.split(':')[0].replace(' ', '')
            self.type = raw.split(':')[1].replace(' ', '')

    def __repr__(self):
        s = f'{self.name}[{self.type}]'
        return s
    
    def vars(self):
        return vars(self)

class Arg_Doc:
    """
    Attributes:
        name (str): description
        type (str): description
        arg (Arg): description
    """
    def __init__(self, name: str, type: type):
        self.name = name
        self.type = type
        self.arg = None
        if 'list' in self.type:
            self.arg = Arg_Doc(self.type, self.type.split('[')[1].split(']')[0])

    def __repr__(self):
        s = f'{self.name} - [{self.type}]'
        return s
    
    def vars(self):
        return vars(self)