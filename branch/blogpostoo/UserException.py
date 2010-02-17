

class UserException(Exception):

    '''Base class for User errors by sinojelly.'''

    def __init__(self, msg):
        self.msg  = msg

    def __repr__(self):
        return self.msg

    __str__ = __repr__

class ParamException(UserException):
    def __init__(self):
        UserException.__init__(self, "Parameter exception!")

    def __repr__(self):
        return UserException.msg

    __str__ = UserException.__repr__

class NotFoundException(UserException):
    def __init__(self):
        UserException.__init__(self, "Node not found exception!")

    def __repr__(self):
        return UserException.msg

    __str__ = UserException.__repr__

class TooManyNodeException(UserException):
    def __init__(self):
        UserException.__init__(self, "Too many node found exception!")

    def __repr__(self):
        return UserException.msg

    __str__ = UserException.__repr__

##print("eeeeeee")
##raise ParamException