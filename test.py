def getLSB(byte, depth):
    """ return the least {depth} significant bit(s) of the argument

    Input: byte
    Output: lsb

        Example: 
            >>> getLSB(0b01010101)
            1
    """
    lsb = byte & (2**depth-1)
    return lsb

print getLSB(0b0101,3)