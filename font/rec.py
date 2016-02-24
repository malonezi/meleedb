from sys import argv
from PIL import Image
from pytesseract import image_to_string
from Levenshtein import jaro_winkler

import glob

states = open("states.txt").read().split("\n")[:-1]

for infile in sorted(glob.iglob(argv[1])):
    im = Image.open(infile)

    # rect = (444, 63, 661, 116)
    rect = (383, 58, 686, 110)

    im = im.crop(rect).point(lambda p: p > 111)
    im.convert("1")

#    print(image_to_string(im, config="--user-words states.txt --user-patterns states.txt -c load_system_dawg=0 -c load_freq_dawg=0"))
    text = image_to_string(im, config="-l states -c tessdata_char_blacklist='0123456789' bazaar").split("\n")[0]
    if text:
        match = text if text in states else max(states, key=lambda s: jaro_winkler(text, s))
        print(infile, match, text, jaro_winkler(text, match))
