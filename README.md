# Detecting Homoglyph Attacks with a Siamese Neural Network
This is sample code for training the siamese neural network and comparing it to edit distance based techniques.  

This was tested with 1.2.2 version of keras and python 2.7.  We recommend having a GPU to speed up processing.

## Prereq
You will need a copy of Arial.ttf to put in the code directory before running.  This file should be in the same directory of the python code.  If not, you will see an error similar to this:

```
Traceback (most recent call last):
  File "run_siamese.py", line 144, in <module>
    X1_train = generate_imgs([x[0] for x in data['train']], font_location, font_size, image_size, text_location)
  File "run_siamese.py", line 47, in generate_imgs
    font = ImageFont.truetype(font_location, font_size)
  File "/home/<user>/anaconda2/lib/python2.7/site-packages/PIL/ImageFont.py", line 239, in truetype
    return FreeTypeFont(font, size, index, encoding)
  File "/home/<user>/anaconda2/lib/python2.7/site-packages/PIL/ImageFont.py", line 128, in __init__
    self.font = core.getfont(font, size, index, encoding)
IOError: cannot open resource
```

### Mac

You can view this for getting Arial.ttf: https://support.apple.com/guide/font-book/install-and-validate-fonts-fntbk1000/mac

### Ubuntu

You can install ttf-mscorefonts-installer

### Windows

Look in `c:\Windows\Fonts`

## Code params
The code is very simple and has a couple parameters that can be changed inline.  The first is data type.  For running the code on process data, set the `dataset_type` to `"process"`:

```
dataset_type = 'process'
```

For domains:

```
dataset_type = 'domain'
```

The second parameter allows the code to run on a subset of the data to get results faster.  Note that a smaller dataset will get worse results.  To set this parameter to a subset set `isFast` to `True`:

```
isFast = True
```

Too set to the full dataset do:

```
isFast = False
```

## Run code

Simply run the python code like:

```
python run_siamese.py
```
