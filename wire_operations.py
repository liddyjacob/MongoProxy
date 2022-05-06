import struct # for decomposing C like byte objects
import asyncio

class UnpackingFunctions:
    def Int(data):
        return (struct.Struct("<i").unpack(data))[0]

#    def c_string(data):

class MessageHeader:
    read_amount = 16
    component_locations = {
        'LENGTH': (0,4),
        'REQUEST_ID': (4,8),
        'OPCODE': (12,16)
    }
    components = {}

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
        for (f, bounds) in self.component_locations.items():
            print(f)
            print(bounds)
            self.components[f] = UnpackingFunctions.Int(self.data[bounds[0]:bounds[1]])

        # Set the body length up so i dont compute in the operation.
        print("hey")
        self.body_length = self.components['LENGTH'] - self.read_amount

    def __str__(self):
        return str(self.components)



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


class InsertOP:
    def __init__(self):
        pass

    def __str__(self):
        return ("Insert Operation")

class QueryOP:
    def __init__(self, message_header):
        self.message_header = message_header
        self.read_amount = message_header.body_length
        self.data_reader = message_header.data_reader
        pass

    async def process(self):
        self.data = await self.data_reader.read(self.read_amount)

        pass
        #asyncio.

    def __str__(self):
        return ("QueryOP Operation: " + str(self.data))

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
    2002:   InsertOP,
    2004:   QueryOP,
    2005:   GetMoreOP,
    2006:   DeleteOP,
    2007:   KillCursorsOP,
    2013:   MessageOP
}

CODE_FROP_OPERATION = {
    ReplyOP:        1,
    UpdateOP:       2001,
    InsertOP:       2002,
    QueryOP:        2004,
    GetMoreOP:      2005,
    DeleteOP:       2006,
    KillCursorsOP:  2007,
    MessageOP:      2013      
}