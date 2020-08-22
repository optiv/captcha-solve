from PIL import Image, ImageCms

im = Image.open('captcha.png')
(red, blue, green) = im.split()

red.save('red.png')
green.save('green.png')
blue.save('blue.png')

hsv = im.convert('HSV')
(hue, sat, val) = hsv.split()
hue.save('hue.png')
sat.save('sat.png')
val.save('val.png')

cmyk = im.convert('CMYK')
(cyan, magenta, yellow) = im.split()
cyan.save('cyan.png')
magenta.save('magenta.png')
yellow.save('yellow.png')

# Convert to L*a*b colorspace is more complex:
rgb = ImageCms.createProfile(colorSpace='sRGB')
lab = ImageCms.createProfile(colorSpace='LAB')
transform = ImageCms.buildTransform(inputProfile=rgb, outputProfile=lab, inMode='RGB', outMode='LAB')
lab_im = ImageCms.applyTransform(im=im, transform=transform)
l, a, b = lab_im.split()
l.save("l.png")
a.save("a.png")
b.save("b.png")
