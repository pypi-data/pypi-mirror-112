from objects.Arg import Arg
from objects.Return import Return

class Signature:
    """

    Attributes:
        name (str): description
        args (Arg): description
        ret (Return): description
    """
    def __init__(self, raw: str):
        if raw == '':
            self.name= ''
            self.args: Arg = []
            self.ret = Return('')
            return

        self.name = raw.replace('def ', '').split('(')[0]
        args = []
        for a in raw.split('(')[1].split(')')[0].split(','):
            if a != '':
                args.append(Arg(a))
        self.args = args
        self.ret = Return(raw.split(')')[-1])

    def __repr__(self):
        s = f'{self.name}'
        if len(self.args) > 0:
            s += '('
            for a in self.args:
                if a.type is not None:
                    s += f'{a} '
            s += ')'
            if self.ret.type is not None:
                s += f' -> {self.ret}:'
        return s
    
    def vars(self):
        return vars(self)
