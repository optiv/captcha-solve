from PIL import Image, ImageCms, ImageOps, ImageFilter
import pytesseract
import numpy as np

# For direct script evaluation:
from argparse import ArgumentParser

def rescale(im):
	# Assume 72 DPI if we don't know, as this is
	# one of the lowest common DPI values.
	try:
		dpi = im.info['dpi']
	except KeyError:
		dpi = 72

	target_dpi = 300
	factor = target_dpi / dpi

	return ImageOps.scale(im, factor)


def rgb_to_lab(im):
	rgb = ImageCms.createProfile(colorSpace='sRGB')
	lab = ImageCms.createProfile(colorSpace='LAB')
	transform = ImageCms.buildTransform(inputProfile=rgb, outputProfile=lab, inMode='RGB', outMode='LAB')
	
	return ImageCms.applyTransform(im=im, transform=transform)

def threshold(np_array, threshold, min_val, max_val):
	np_array[np_array < threshold] = min_val
	np_array[np_array > threshold] = max_val

	return np_array

def apply_corrections(result):
	# Fixes the most-common mistakes
	# !only correct for this particular captcha!
    result = result.strip()
    result = result.replace('/', '7')
    result = result.replace('&','8')
    result = result.replace('S','5')
    result = result.replace(' ', '')
    result = result[:5]
    result = result.lower()

    return result


def get_text(im):

	lab_im = rgb_to_lab(im)

	lab_im = rescale(lab_im)
	l, a, b = lab_im.split()

	# Convert to numpy array and apply the threshold to remove lines
	np_a = np.array(a)
	np_a = threshold(np_a, 180, 0, 255)

	# Invert the image: we want black text on a white background
	np_a = 255 - np_a

	a = Image.fromarray(np_a)

	# Expand image to close up "gaps" in letters, shrink to
	# stop letters running together
	a_filtered = a.filter(ImageFilter.MinFilter(11))
	a_filtered = a_filtered.filter(ImageFilter.MaxFilter(5))
	
	# It's useful to save this pre-OCR step to identify issues
	a_filtered.save('filtered.png')

	# Run OCR and get the result
	result = pytesseract.image_to_string(a_filtered)
	result = apply_corrections(result)

	return result

# Accept bytes() objects
def text_from_bytes(array):
	im = Image.open(io.BytesIO(array))
	return get_text(im)

# Accept numpy arrays
def text_from_nparray(np_array):
	im = Image.fromarray(np_array)
	return get_text(im)
	
# Accept filenames to load image from
def text_from_file(filename):
	im = Image.open(filename)
	return get_text(im)

if __name__ == "__main__":

	p = ArgumentParser()
	p.add_argument('file', help="captcha image file to solve")

	args = p.parse_args()

	print(text_from_file(args.file))