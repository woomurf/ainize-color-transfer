# USAGE
# python example.py --source images/ocean_sunset.jpg --target images/ocean_day.jpg

# import the necessary packages
from color_transfer import color_transfer
import numpy as np
import cv2

def runExample(source, target, output=None):

	# load the images
	source = cv2.imread(source)
	target = cv2.imread(target)

	# transfer the color distribution from the source image
	# to the target image
	transfer = color_transfer(source, target)
	
	width = 300
	r = width / float(transfer.shape[1])
	dim = (width, int(transfer.shape[0] * r))
	resized = cv2.resize(transfer, dim, interpolation = cv2.INTER_AREA)

	# check to see if the output image should be saved
	if output is not None:
		cv2.imwrite("./static/"+output, transfer)
		return output
	else:
		cv2.imwrite('./static/result.jpg', transfer)
		return 'result.jpg'