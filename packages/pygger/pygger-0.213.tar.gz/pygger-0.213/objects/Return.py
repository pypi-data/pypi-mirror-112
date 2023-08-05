class Return:
    """
    Attributes:
        type (str): description
    """
    def __init__(self, raw: str):
        spl = raw.split('->')
        if len(spl) < 2:
            self.type = ''
        else :
            self.type = raw.split('->')[-1].replace(' ', '').replace(':', '')

    def __repr__(self):
        s = f'[{self.type}]'
        return s
    
    def vars(self):
        return vars(self)

class Return_Doc:
    """
    Attributes:
        type (str): description
    """
    def __init__(self, type:str):
        self.type = type        
        self.arg = None
        if 'list' in self.type:
            self.arg = Return_Doc(self.type.split('[')[1].split(']')[0])

        
    def __repr__(self):
        s = f'-> {self.type}\t[{self.arg}]'
        return s