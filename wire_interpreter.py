# this is a set of classes and functions for dissecting requests and packaging requests 
from wire_operations import OPERATION_FROM_CODE

# The body of the message will depend on the head.
async def make_message_body(message_head):

    operation_maker = OPERATION_FROM_CODE[message_head.components['OPCODE']]
    operation = operation_maker(message_head)

    # Process everything in here so user does not have to
    await operation.process()

    return operation
