from .GeneralOperations import Operations

class Division(Operations):
    '''
    This class inherit the features from Operations class.
    The goal od this class is to divide 2 numbers.
    '''

    '''
    Initializing the variable in memory
    '''
    def __init__(self, n1, n2):
        Operations.__init__(self, n1, n2)

    '''
    This method divide 2 numbers
    '''
    def div(n1, n2):
        return (n1/n2)