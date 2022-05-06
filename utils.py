

# Read through some binary, length bits at a time.
from turtle import position


class BinaryReader:
    def __init__(self, binary):
        self.data = binary
        self.position = 0

    def read(self, length):
        start = self.position
        end = self.position + length

        if (end > len(self.data)):
            raise Exception("No more bits to read! Did you read too many?")

        self.position = end

        return self.data[start:end]

    def remainder(self):
        return (len(self.data) - self.position)

    def remaining_data(self):
        return self.data[self.position:]

    def rollback(self, length):
        self.position = self.position - length

