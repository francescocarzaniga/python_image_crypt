#!/usr/bin/env python
# -*- coding: utf-8 -*-—

from PIL import Image
import re
import base64

# file access
# ---------------------------------------------------

def openimage(filename):
    """ Open the image (only lossless images are supported) given by the filename specified in the
    filename string and return the image object.

    Input: filename (the filename of an image with format PNG)
    Output: open the image
            "Please select a valid image." (if the image is not PNG)
    """
    
    img = Image.open(filename)
    if img.format == 'PNG':
        return img
    else:
        print 'Please select a valid image.'
        return

def saveimage(image, name):
    """ Save the modified image under the specified name.

    Input: image, name (new name for the image)
    Output: save the image with the new name
    """
   
    image.save('{}.png'.format(name))

# -----------------------------------------------

def showimage(image):
    """ Show the image on the screen.
    """
    
    image.show()

# ------------------------------------------------

# binary data functions
# ------------------------------------------------

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

def setLSB(byte, bit, depth):
    """ return byte modified such that the least {depth} significant
        bit(s) have the value given by bit.

    Input: byte, bit(new bit)
    Output: new_byte (old byte with the lsb modified with new bit)

        Example: 
            >>> setLSB(0b01010101,0)
            0b01010100
    """
    
    new_byte = (byte & ~(2**depth-1)) | bit
    return new_byte

def messagetobitlist(message):
    """ Convert each letter in the message first into
        the character code using the ord(c) function.
        Then return a list containing each bit of the resulting 8-bit numbers
        starting from the most significant bit and ending at the lsb.

    Input: message (str)
    Output: bitlist

        Example:

        >>> msg = messagetobitlist("AB")
        >>> msg
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        
    """
   
    bitlist = []
    #message = base64.b64encode(message)
    
    for i in message:
        for x in (format(ord(i), '08b')):
            bitlist.append(int(x))
    return bitlist

def bitlisttobyte(bits):
    """ Convert a list of length 8, containing
        the bits of a byte in order from MSB to LSB
        into a byte.

    Input: bits
    Output: byte

        Example:
        >>> bitlisttobyte([0,1,0,1,0,0,0,1])
        81    
    """
    i = len(bits)
    byte = 0 
    for k in range (0,i):
        byte = byte + 2**k*bits[i-1-k]         
    return byte

def bytetobitlist(byte):
    """ convert a byte into a list of bits
        Example:

    Input: byte
    Output: bits (list of bits)

        Example:
            >>> bytetobitlist(4)
            [0,0,0,0,0,1,0,0]    
    """
    byte = bin(byte)[2:]
    str(byte)
    bits = []
    for i in byte: 
        bits.append(i)
    bits = map(int, bits)
    return bits
    

def bitlisttostring(bitlist):
    """ The input is a list containing
        the bits of a message. Take 8 bit pieces
        and convert them to characters. Return the resulting
        string.

    Input: bitlist
    Output: string
    """

    string = ""
    
    for i in range(0, len(bitlist), 8):
        bl = bitlist[i:i+8]
        if len(bl) < 8:
            break
        # bl is a list of length 8
        # containing the bits of a byte
        # in order from the msb to the lsb
        
        byte = bitlisttobyte(bl)
        c = chr(byte) #get character from bytecode
        string += c
    
    #string = base64.b64decode(string)

    return string

def isprintable(string):
    """ Check if a string consists only of printable characters.
    """
    from string import printable
    return all(c in printable for c in string)

def addmagicstring(message):
    """ Adds some special string at the beginning and end of
        the message so it can be recognised by the programm later.

    Input: message(str)
    Output: message with specialString 

        Example:
        >>> addmagicstring('Hello')
        'MAGICSTRINGSTARTHelloMAGICSTRINGEND'
    """
    #specialString = "יום טוב"
    #specialStringEnd = "לילה טוב"
    specialString = "testtestbegin"
    specialStringEnd = "testtestend"

    message = specialString + message + specialStringEnd
    return message

def checkmagic(string):
    """ Check if the string contains a magic string marker.
        If it does, then return the message in between.

    Input: string
    Output: string without magicstrings
            None (if the string does not contain magicstrings)
    """
    
    MAGICSTART = "testtestbegin"
    MAGICEND   = "testtestend"

    result = re.search(MAGICSTART + '([\s\S.]*)' + MAGICEND, string)
    if result:
        return result.group(1)
    else:
        return None
    
def writelsbtoimage(image, bl):
    """ Change each LSB in each color component of each pixel
        in the image with the binary representation of the message.

    Input: image, bl
    Output: image_output(image modified)
    """
    
    import numpy as np
    import random
    
    img_array = np.array(image)
    ins_point = random.randrange(0, img_array.size-len(bl), 8)
    img_array.ravel()[ins_point:ins_point+len(bl)] = setLSB(img_array.ravel()[ins_point:ins_point+len(bl)], bl, 1)
    image_output = Image.fromarray(img_array)
    
    return image_output

def getlsbfromimage(image):
    """ Return the least significant bits in the image
        as a list

    Input: image
    Output: lsblist(list LSB of the image)
    """
    
    import numpy as np
    
    img_array = np.array(image)
    lsblist = getLSB(img_array.ravel(), 1).tolist()
    
    return lsblist

    
def embed(message, image):
    """ Embed the string in the image as a secret message.

    Input: message, image
    Output: image with hidden string
    """
    # add some string at the beginning and end of the message
    # such that it is later possible to identify if a message
    # has been hidden.
    message = addmagicstring(message)
    
    # Convert the message into a list of bits
    bl = messagetobitlist(message)

    img_out = writelsbtoimage(image,bl)
    return img_out

def extract(image):
    """ check if the given image contains any hidden message
        and return the message as a string if there is any.

    Input: image
    Output: string (hidden string)
            "Nothing found" (if the image does not contain any hidden message)
    """
    bits = getlsbfromimage(image)
    string = bitlisttostring(bits)
    if checkmagic(string) == None:
        print("Nothing found")
    else:
        string = checkmagic(string)
    
    return string

def findimage(image, depth):
    """ This function finds the hidden image.

    Input: image, depth (depth of the target image)
    Output: img_new (target image)
    """
    import numpy as np
    
    img_array = np.array(image)
    lsb_array = getLSB(img_array, depth)
    lsb_array = lsb_array*(255/(2**depth-1))
    img_new = Image.fromarray(lsb_array)
    
    return img_new

def putimage(image_origin, image_target, depth):
    """ This function puts an image into the original image, with your choosen depth of colour.

    Input: image_origin (original), image_target, depth
    Output: img_new (original image with the hidden image inside)
    """
    import numpy as np
    import math
    
    img_origin_array = np.array(image_origin)
    img_target_array = np.array(image_target)
    img_target_array = img_target_array/int(math.ceil(255/float((2**depth))))
    img_new_array = setLSB(img_origin_array, img_target_array, depth)
    img_new = Image.fromarray(img_new_array.astype('uint8'))
    
    return img_new

def encripting(string,key):
    """ This function receives a string and encrypts it with a stream cipher.

    Input: string, key
    Output: cipher_text
    """
    import Crypto
    from Crypto.Cipher import ARC4

    string = base64.b64encode(string)
    obj1 = ARC4.new(key)
    cipher_text = obj1.encrypt(string)
    return cipher_text

def decripting(string,key):
    """ This function receives an encrypted string and returns it decrypted.

    Input: string, key
    Output: cipher_text
    """
    import Crypto
    from Crypto.Cipher import ARC4
    
    obj2 = ARC4.new(key)
    cipher_text = obj2.decrypt(string)
    cipher_text = base64.b64decode(cipher_text)
    return cipher_text

# Testing functions
#------------------------------------------------------------------
import unittest

class TEST(unittest.TestCase):

    # 1. check if embedding and extraction of messages works
    def test_embedextract(self):
        """ Test if we can open an image, embed a string in it,
            and then save it under a new file name.
        """
        import string
        import random

        string = ''.join(random.choice(string.letters) for _ in range(10))
        string = 'helloüèü'
        key = string # accept user input
        img = openimage('face.png')
        img_out = embed(encripting(string, key), img)
        saveimage(img_out, 'TEST2')
        img = openimage('TEST2.png')
        m = decripting(extract(img), key)
        print repr(m)
        print m
        self.assertEqual(string, m)

def main():
    unittest.main()

if __name__ == "__main__":
    main()


