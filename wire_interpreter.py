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

# The body of the message will depend on the head.
async def make_message_body(message_head):
    pass
