

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