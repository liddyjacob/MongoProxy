import struct # for decomposing C like byte objects
from codecs import utf_8_decode
import asyncio
import functools
from utils import BinaryReader
from collections import OrderedDict
import operator
import bson

# for reading the bson
CODEC_OPTIONS = bson.codec_options.CodecOptions(document_class=OrderedDict)

class UnpackingFunctions:
    def Int(data):
        return (struct.Struct("<i").unpack(data))[0]

    # unsigned int
    def UInt(data):
        return (struct.Struct("<I").unpack(data)[0])

    # Byte
    def Byte(data):
        return (struct.Struct("<b").unpack(data)[0])

    def CString(data):
        return utf_8_decode(data)

    
def get_c_string_length(reader):
    remaining_data = reader.remaining_data()
    return remaining_data.index(b"\x00", 0)

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
            self.components[f] = UnpackingFunctions.Int(self.data[bounds[0]:bounds[1]])

        # Set the body length up so i dont compute in the operation.
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
    def __init__(self, message_header):
        self.message_header = message_header
        self.read_amount = message_header.body_length
        self.data_reader = message_header.data_reader
        pass

    async def process(self):
        self.data = await self.data_reader.read(self.read_amount)
        self.data_reader = None # do not read more data than needed

        self.datafeed = BinaryReader(self.data)

        self.flags = UnpackingFunctions.UInt(self.datafeed.read(4))

        # Check to see if flags are reserved
        self._check_flags_and_checksum()

        # buffer for checksum if it exists at
        # the end of the message
        checksum_buffer = 0
        if self.checksum_present:
            checksum_buffer = 4

        payload_document = OrderedDict()

        # each message is an ordered set of bson objects,
        # or stings.
        while (self.datafeed.remainder() - checksum_buffer > 0):
            payload_type = UnpackingFunctions.Byte(self.datafeed.read(1))
            payload_size = UnpackingFunctions.Int(self.datafeed.read(4))
            
            # BSON to decode:
            if payload_type == 0:
                self.datafeed.rollback(4) # rollback because this number is useful to bson
                doc = bson.decode_all(self.datafeed.read(payload_size),
                                      CODEC_OPTIONS)[0]
                payload_document.update(doc)

            elif payload_type == 1:
                # Section starts w/ 4-byte size prefix, identifier ends w/ nil.
                i_len = get_c_string_length(self.datafeed)

                identifier = UnpackingFunctions.CString(self.datafeed.read(i_len))

                documents_len = payload_size - len(identifier) - 1 - 4
                docs = bson.decode_all(self.datafeed.read(documents_len),
                                      CODEC_OPTIONS)[0]
                payload_document[identifier] = docs

        self.document = payload_document
            # String to decode:

        if self.checksum_present:
            if self.datafeed.remainder() != 4:
                raise ValueError(
                    'OP_MSG has checksumPresent flag set, expected 4 bytes'
                    ' remaining but have %d bytes remaining' % (remaining,))

            self.checksum = UnpackingFunctions.UInt(self.datafeed.read(4))
        else:
            if self.datafeed.remainder() != 0:
                raise ValueError(
                    'OP_MSG has no checksumPresent flag, expected 0 bytes'
                    ' remaining but have %d bytes remaining' % (remaining,))
            # Read A bunch a data here

    # see of self.flags is valid:
    def _check_flags_and_checksum(self):
        # This code brought to you by:
        # https://github.com/mongodb-labs/mongo-mockup-db/blob/master/mockupdb/__init__.py

        OP_MSG_FLAGS = OrderedDict([
            ('checksumPresent', 1 << 0),
            ('moreToCome', 1 << 1),
            ('exhaustAllowed', 1 << 16)])

        _ALL_OP_MSG_FLAGS = functools.reduce(operator.or_, OP_MSG_FLAGS.values())

        if self.flags & ~_ALL_OP_MSG_FLAGS:
            raise ValueError(
                'OP_MSG flags has reserved bits set.'
                ' Allowed flags: 0x%x. Provided flags: 0x%x' % (
                    _ALL_OP_MSG_FLAGS, self.flags))

        self.checksum_present = self.flags & OP_MSG_FLAGS['checksumPresent']
 

    def __str__(self):
        return ("Message Operation: " + str(self.document))

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