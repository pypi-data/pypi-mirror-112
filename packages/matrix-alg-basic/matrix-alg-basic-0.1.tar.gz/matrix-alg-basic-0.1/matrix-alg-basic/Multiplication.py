from .GeneralOperations import Operations

class Multiplication(Operations):
    '''
    This class inherit the features from Operations class.
    The goal od this class is to multiply 2 numbers.
    '''

    '''
    Initializing the variable in memory
    '''
    def __init__(self, n1, n2):
        Operations.__init__(self, n1, n2)

    '''
    This method multiply 2 numbers
    '''
    def mul(n1, n2):
        return (n1*n2)