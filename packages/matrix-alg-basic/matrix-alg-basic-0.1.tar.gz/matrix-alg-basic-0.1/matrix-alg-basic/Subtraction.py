from .GeneralOperations import Operations

class Subtraction(Operations):
    '''
    This class inherit the features from Operations class.
    The goal od this class is to subtract 2 numbers.
    '''

    '''
    Initializing the variable in memory
    '''
    def __init__(self, n1, n2):
        Operations.__init__(self, n1, n2)

    '''
    This method subtract 2 numbers
    '''
    def sub(n1, n2):
        if (n1<n2):
         return (n2-n1)
        else:
         return (n1-n2)