from PIL import Image, ImageCms, ImageOps, ImageFilter
import pytesseract
import numpy as np

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

def apply_corrections(result):
    result = result.strip()
    result = result.replace('/', '7')
    result = result.replace('&','8')
    result = result.replace('S','5')
    result = result.replace(' ', '')
    result = result[:5]
    result = result.lower()

    return result



im = Image.open('captcha.png')

# Convert to L*a*b colorspace is more complex:
rgb = ImageCms.createProfile(colorSpace='sRGB')
lab = ImageCms.createProfile(colorSpace='LAB')
transform = ImageCms.buildTransform(inputProfile=rgb, outputProfile=lab, inMode='RGB', outMode='LAB')
lab_im = ImageCms.applyTransform(im=im, transform=transform)

lab_im = rescale(lab_im)
l, a, b = lab_im.split()

# Convert to numpy array and apply the threshold to remove lines
np_a = np.array(a)

threshold = 180
np_a[np_a < threshold] = 0
np_a[np_a > threshold] = 255

# Invert the image: we want black text on a white background
np_a = 255 - np_a

a = Image.fromarray(np_a)

# Expand image to close up "gaps" in letters, shrink to
# stop letters running together
a_filtered = a.filter(ImageFilter.MinFilter(11))
a_filtered = a_filtered.filter(ImageFilter.MaxFilter(5))
a_filtered.save('a-filtered.png')

# Run OCR and get the result
result = pytesseract.image_to_string(a_filtered)

# strip() helps remove some whitespace (like \n) that the OCR returns
print(result.strip())
