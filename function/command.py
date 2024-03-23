from .ping import ping
from .translate import translate
__func__ = {'ping': ping,'translate':translate}

def command(**kwargs) -> str | None:
    if 'cmd' not in kwargs:
        return None
    cmd = kwargs['cmd']
    if type(cmd) == str and cmd.startswith("!"):
        cmd = cmd.lower()[1:]
        option = ""
        msg = ""
        if 'msg' in kwargs and type(kwargs['msg']) == str :
            msg = kwargs['msg']
            parsing = msg.split(maxsplit=1)
            parsing = [text.strip() for text in parsing]

            if len(parsing) == 1:
                msg = parsing[0]
            elif len(parsing) == 2:
                option = parsing[0]
                msg = parsing[1]
        if cmd in __func__:
            return __func__[cmd](option=option,msg=msg)
        else:
            return None

