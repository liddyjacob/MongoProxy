HOST = '127.0.0.1'
PORT = 65432

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

BUFFER_SIZE = 256

import asyncio
from pipe_handlers import RevealTransfer

class DirectTransfer:
    def __init__(self):
        pass
    
    async def transfer(self, reader, writer):
        while not reader.at_eof():
            data = await reader.read(BUFFER_SIZE)
            writer.write(data)

async def proxy_pipe(reader, writer, pipe_handler):
    try:
        # THIS IS CONTINUOUS AND NEVER ENDS
        # SO WE SHOULD HAVE THE WIRE
        # ACCEPT THE WRITER AND THE READER.
        await pipe_handler.transfer(reader, writer)

    finally:
        writer.close()

# Connects to the Mongo Client
async def open_mongo_connection():
    return await asyncio.open_connection(
            MONGO_HOST, MONGO_PORT)
    
class ClientContext():
    # Provides a common environment for clients
    def __init__(self, sender = DirectTransfer(), receiver = DirectTransfer()):
        self.sender = sender
        self.receiver = receiver

    # Handles incoming clients
    async def handle_client(self, local_reader, local_writer):
        mongo_reader, mongo_writer = await open_mongo_connection()
        try:
            # For sending from client to mongo
            proxy_send = proxy_pipe(local_reader, mongo_writer, self.sender)

            # For sending from mongo to client
            proxy_recv = proxy_pipe(mongo_reader, local_writer, self.receiver)

            # async on these pipes
            await asyncio.gather(proxy_send, proxy_recv)

        finally:
            local_writer.close()



# Create the server
loop = asyncio.get_event_loop()
context = ClientContext(sender = RevealTransfer(), receiver = DirectTransfer())
coro = asyncio.start_server(context.handle_client, HOST, PORT)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()