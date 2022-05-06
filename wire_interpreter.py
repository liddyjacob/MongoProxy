# this is a set of classes and functions for dissecting requests and packaging requests 
import struct # for decomposing C like byte objects

class UnpackingFunctions:
    def Int(data):
        return (struct.Struct("<i").unpack(data))[0]

class MessageHeader:
    read_amount = 16
    flag_locations = {
        'LENGTH': (0,4),
        'REQUEST_ID': (4,8),
        'OPCODE': (12,16)
    }
    flags = {}

    def __init__(self, reader):
        self.data_reader = reader

    async def process(self):
        
        # Make sure there is data to process
        if self.data_reader.at_eof():
            return False
        
        self.data = await self.data_reader.read(self.read_amount)
        self._decompose_data()

        return True

    def _decompose_data(self):
        # find each flag, extract from data.
        for (f, bounds) in self.flag_locations.items():
            print(f)
            print(bounds)
            self.flags[f] = UnpackingFunctions.Int(self.data[bounds[0]:bounds[1]])

    def __str__(self):
        return str(self.flags)


class ReplyOP:
    def __init__(self):
        pass

    def __str__(self):
        return ("Reply Operation")

class UpdateOP:
    def __init__(self):
        pass

    def __str__(self):
        return ("Update Operation")

class UpdateOP:
    def __init__(self):
        pass

    def __str__(self):
        return ("Update Operation")

class InsertOP:
    def __init__(self):
        pass

    def __str__(self):
        return ("Insert Operation")

class GetMoreOP:
    def __init__(self):
        pass

    def __str__(self):
        return ("GetMore Operation")

class DeleteOP:
    def __init__(self):
        pass

    def __str__(self):
        return ("Delete Operation")

class KillCursorsOP:
    def __init__(self):
        pass

    def __str__(self):
        return ("KillCursors Operation")

class MessageOP:
    def __init__(self):
        pass

    def __str__(self):
        return ("Message Operation")

OPERATION_FROM_CODE = {
    1:      ReplyOP,
    2001:   UpdateOP,
    2004:   InsertOP,
    2005:   GetMoreOP,
    2006:   DeleteOP,
    2007:   KillCursorsOP,
    2013:   MessageOP
}

OP_REPLY = 1
OP_UPDATE = 2001
OP_INSERT = 2002
OP_QUERY = 2004
OP_GET_MORE = 2005
OP_DELETE = 2006
OP_KILL_CURSORS = 2007
OP_MSG = 2013

# The body of the message will depend on the head.
async def make_message_body(message_head):
    pass
