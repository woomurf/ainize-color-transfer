# USAGE
# python example.py --source images/ocean_sunset.jpg --target images/ocean_day.jpg

# import the necessary packages
from color_transfer import color_transfer
import numpy as np
import cv2

def runTransfer(source, target, output=None):

	# load the images
	source = cv2.imread(source)
	target = cv2.imread(target)


	# transfer the color distribution from the source image
	# to the target image
	transfer = color_transfer(source, target)
	
	width = 400
	r = width / float(transfer.shape[1])
	dim = (width, int(transfer.shape[0] * r))
	resized = cv2.resize(transfer, dim, interpolation = cv2.INTER_AREA)

	# BGR to RGB
	img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
	
	return img