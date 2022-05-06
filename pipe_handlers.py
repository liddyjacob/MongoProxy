# These are the functions that deal with the pipes

from wire_interpreter import MessageHeader, make_message_body

class RevealTransfer:
    def __init__(self):
        pass

    async def transfer(self, reader, writer):
        message_head = MessageHeader(reader)
        
        while message_head.process():
        
            await message_head.process()
            
            print(message_head)
            message_body = make_message_body(message_head)

            print(message_head)

            #while not self.reader.at_eof():
            #    writer.write(await reader.read(512))

            message_head = MessageHeader(reader)
