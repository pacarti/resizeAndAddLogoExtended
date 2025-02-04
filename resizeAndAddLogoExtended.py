#! python3
# resizeAndAddLogoExtended.py - Resizes all images in current working directory to fit in a 300x300 square, and adds catlogo.png to the lower-right corner.

import os, re
from PIL import Image

# Returns true if image file extension is valid(case insensitive for .png, ,jpg, .bmp and .gif formats):
def isFilenameExtValid(imageFileName):
    PNGsuffixRegex = re.compile(r'.+(\.png$){1}', re.I)
    JPGsuffixRegex = re.compile(r'.+(\.jpg$){1}', re.I)
    BMPsuffixRegex = re.compile(r'.+(\.bmp$){1}', re.I)
    GIFsuffixRegex = re.compile(r'.+(\.gif$){1}', re.I)
    # ^ and $ used so that entire string is matched from the beginning to the end.
    if PNGsuffixRegex.match(imageFileName) or JPGsuffixRegex.match(imageFileName) or BMPsuffixRegex.match(imageFileName) or GIFsuffixRegex.match(imageFileName):
        return True

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SQUARE_FIT_SIZE = 300
LOGO_FILENAME = 'catlogo.png'
logoIm = Image.open(LOGO_FILENAME)
logoWidth, logoHeight = logoIm.size


os.makedirs('withLogo', exist_ok=True)
# Loop over all files in the working directory.
for filename in os.listdir('.'):
    # if not (filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.gif') or filename.endswith('.bmp') or filename.endswith('.PNG') or filename.endswith('.JPG') or filename.endswith('.GIF') or filename.endswith('.BMP')) or filename == LOGO_FILENAME:
    if not isFilenameExtValid(filename):
        continue    # skip non-image files and the logo file itself
    im = Image.open(filename)
    width, height = im.size

    # Check if the image is not too small for logo
    if im.size < 2 * logoIm.size:
        print('Image %s too small to add the logo. Skipping...' % filename)
        continue

    # Check if image needs to be resized.
    if width > SQUARE_FIT_SIZE and height > SQUARE_FIT_SIZE:
        # Calculate the new width and height to resize to.
        if width > height:
            height = int((SQUARE_FIT_SIZE / width) * height)
            width = SQUARE_FIT_SIZE
        else:
            width = int((SQUARE_FIT_SIZE / height) * width)
            height = SQUARE_FIT_SIZE
        # Resize the image.
        print('Resizing %s...' % (filename))
        im = im.resize((width, height))
    # Add the logo.
    print('Adding logo to %s...' % (filename))
    # 3rd argument also so that transparency pixels are pasted also
    im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
    # Save changes.
    im.save(os.path.join('withLogo', filename))