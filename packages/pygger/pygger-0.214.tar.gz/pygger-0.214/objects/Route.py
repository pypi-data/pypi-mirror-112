class Route:
    def __init__(self, raw: str):
        if raw == '':
            self.path = ''
            self.methods = []
            return
        self.path = raw.split('(')[1].split(')')[0].split(',')[0].replace('\'', '')
        self.methods = raw.split('(')[1].split(')')[0].split('[')[1].split(']')[0].replace('\'', '').replace(' ', '').split(',')

    def __repr__(self):
        s = f'{self.path} - {self.methods}'
        return s
    
    def vars(self):
        return vars(self)