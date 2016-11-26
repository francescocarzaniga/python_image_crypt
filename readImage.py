'''
This program needs the packages PIL and pillow to be loaded
MAC Users with terminal (just copy-paste in sequence): 
sudo easy_install pip
sudo pip install pillow
'''
import sys
import os
from PIL import Image
class imageCrypt(object):
		
	def importImage(self, imagePath):
		inputImage = Image.open(imagePath).convert("L")
		inputImage.show()

#Main method
if __name__ == '__main__':
	imagePath = "img/univers.png"
	imageCrypt().importImage(imagePath)

'''
#coordinates pixels within an image: 
#(left, upper, right, lower)
Image.open(imagePath).convert("L") : black and white
'''

