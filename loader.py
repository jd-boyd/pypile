import sexpdata
from sexpdata import Symbol

class Function:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = tuple(body) if isinstance(body, list) else body
    def __repr__(self):
        body_text = repr(self.body)
        proto =  [Symbol(self.name)] + self.args
        proto_text = " ".join([repr(a) for a in proto])
        return "(define (" + proto_text +  ")\n\t" + body_text + "\n)"

class ScmFile:
    def __init__(self):
        self.functions = {}

    def add(self, name, args, fcn):
        if len(args) > 6:
            assert False, "6 max args"
        self.functions[name] = Function(name, args, fcn)

def load_file(file_str):
    file_fcns = ScmFile()
    statements = sexpdata.parse(file_str)
    
    for statement in statements:
#        if statement[0] != Symbol("define"):
#            print("Only define statements handled: ", repr(statement[0]))
        proto = statement[1]
        file_fcns.add(proto[0].tosexp(), proto[1:], statement[2])
    return file_fcns

