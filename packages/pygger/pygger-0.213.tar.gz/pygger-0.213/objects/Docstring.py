from objects.Return import Return_Doc
from objects.Arg import Arg_Doc


class Docstring(): 
    """
    
    Attributes:
        content (str): Human readable string describing the exception.
        args (list[str]): Exception error code.
        att (list[str]): Exception error code.
        ret (list[str]): Exception error code.
    """
    def __init__(self, raw: str, name: str):
        self.content = raw
        args = []
        att = []
        self.name = name
        self.args = []
        self.att = []
        if 'Args:' in raw and 'Returns:' not in raw: # only args, no ret
            self.ret = None
            self.desc  = self.clean_string(raw.split('Args:')[0])
            args = raw.split('Args:')[1].replace('\t', '').replace(' ', '').split('\n')
        elif 'Args:' in raw and 'Returns:' in raw: #both ret and args
            self.ret = raw.split('Returns:')[1].replace('\t', '').split(':')[0].split(' ')
            self.desc  = self.clean_string(raw.split('Args:')[0])
            args = raw.split('Args:')[1].split('Returns:')[0].replace('\t', '').replace(' ', '').split('\n')
        elif 'Args:' not in raw and 'Returns:' in raw: #no args only ret
            args = []
            self.desc  = self.clean_string(raw.split('Returns:')[0])
            self.ret = raw.split('Returns:')[1].replace('\t', '').split(':')[0].split(' ')
        else:
            self.desc  = ''
            args = []
            self.ret = []
        if 'Attributes:' in raw:
            att = raw.split('Attributes:')[1].replace('\t', '').replace(' ', '').split('\n')

        for a in att:
            if a != '':
                nam = (a.split('(')[0], a.split('(')[1].split(')')[0])[0]
                typ = (a.split('(')[0], a.split('(')[1].split(')')[0])[1]
                self.att.append(Arg_Doc(nam, typ))
            
        for a in args:
            if a != '':
                nam = (a.split('(')[0], a.split('(')[1].split(')')[0])[0]
                typ = (a.split('(')[0], a.split('(')[1].split(')')[0])[1]
                self.args.append(Arg_Doc(nam, typ))
        if self.ret is not None:
            for r in self.ret:
                if r != '':
                    self.ret = Return_Doc(r)

    def clean_string(self, string: str) -> str:
        cleaned = string.replace('\n', '')
        for i in range(2, 10):
            if ' ' * i in cleaned:
                cleaned = cleaned.replace(' ' * i, ' ')
        return cleaned[:-2]

    def __repr__(self):
        s = f'\n\tname : {self.name}\n'
        s += f'\targs : {self.args}\n'
        s += f'\tatt : {self.att}\n'
        s += f'\tret : {self.ret}\n'
        return s

    
    def vars(self):
        return vars(self)