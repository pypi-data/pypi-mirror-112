import struct
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)

import numpy as np
import cv2


def convert(file_path: str, width: int, height: int, depth: int=1, 
        img_type: str='tiff', save_name: str=None, check_pixels: bool=False):
    """Converts uint16 files to images

    You must provide the accurate width, height and depth dimensions of the 
    file.

    Args:
        file_path (str):
            Path to file
        width (int):
            Width of uint16 images
        height (int):
            Height of uint16 images
        depth (int):
            Depth of uint16 images
        img_type (str):
            Optional. Type of image to create. Default is tiff.
        save_name (str):
            Optional. If None added, files save as the same name as the
            file_path, but as .tiff (or png, etc...) instead.
        check_pixels (bool):
            Optional. If True, compare pixels of uint16 file and image and
            give warning if they mismatch. Won't work if 
            logging turned off. Default is False.
    """
    available_formats = ['png', 'tiff', 'jpg']
    if not img_type in available_formats:
        logging.warning('Only {} images supported currently, '.format(
            available_formats) + 'changing image type to tiff.')
        img_type = 'tiff'

    # Get save name for different formats
    if save_name is None:
        save_name = os.path.splitext(file_path)[0]
    names = {form: (save_name + '.' + form) for form in available_formats}

    tot = width*height*depth
    curr = 0
    fin = open(file_path, "rb")
    data = []
    try:
        while(True):
            data.append(struct.unpack('H', fin.read(2)))
            prog = 100*round(curr/tot, 3)
            curr += 1
            sys.stdout.write("\r%d%% done loading file" % prog)
            sys.stdout.flush()
            if curr > tot:
                print()
                logging.warning('Returning, as file larger than expected. '
                         + 'Check to ensure image width, height and depth are '
                         + 'correct.')
                return
    except Exception as e:
        print()
        if curr < tot:
            logging.warning('Returning, as file smaller than expected. '
                     + 'Check to ensure image width, height and depth are '
                     + 'correct.')
            return
    fin.close()
    # unpack always creates a tuple
    data = [c[0] for c in data]
    img = np.uint16(np.array(data).reshape(height, width, depth))
    cv2.imwrite(names[img_type], img)
    logging.info('Saved {}'.format(names[img_type]))

    if check_pixels:
        compare_file_to_img(file_path, names[img_type], width, height, depth)

def compare_file_to_img(file_path: str, img_path: str, width: int, 
        height: int, depth: int=1):
    """Compares pixels of image to original file to ensure no pixel change
    
    Prints whether pixel change occurred or not.

    Args:
        file_path (str):
            Path to uint16 file
        img_path (str):
            Path to image file
        width (int):
            Width of image
        height (int):
            Height of image
        depth (int):
            Depth of image, default is 1
    """
    logging.info('Checking for pixel alterations between {} and {}'.format(
        file_path, img_path)
    )
    fin = open(file_path, "rb")
    data = []
    tot = width*height*depth
    curr = 0
    try:
        while(True):
            data.append(struct.unpack('H', fin.read(2)))
            prog = 100*round(curr/tot, 3)
            curr += 1
            sys.stdout.write("\r%d%% done loading file" % prog)
            sys.stdout.flush()
            if curr > tot:
                print()
                logging.warning('Returning, as file larger than expected. '
                         + 'Check to ensure image width, height and depth are '
                         + 'correct.')
                return
    except Exception as e:
        print()
        if curr < tot:
            logging.warning('Returning, as file smaller than expected. '
                     + 'Check to ensure image width, height and depth are '
                     + 'correct.')
            return
    fin.close()
    # unpack always creates a tuple
    data = [c[0] for c in data]
    img = np.array(data).reshape(height, width, depth)
    image = np.uint16(cv2.imread(img_path, cv2.IMREAD_UNCHANGED))

    pixel_loss = False
    curr = 0
    try:
        if depth == 1:
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    prog = 100*round(curr/tot, 3)
                    curr += 1
                    sys.stdout.write("\r%d%% done comparing file to image" % prog)
                    sys.stdout.flush()
                    if img[i][j][0] != image[i][j]:
                        pixel_loss = True
        else:
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    for k in range(img.shape[2]):
                        if img[i][j][k] != image[i][j][k]:
                            prog = 100*round(curr/tot, 3)
                            curr += 1
                            sys.stdout.write("\r%d%% done comparing file to image" % prog)
                            sys.stdout.flush()
                            pixel_loss = True
    except Exception as e:
        print()
        logging.warning('Error: {}'.format(e))
    if pixel_loss:
        print()
        logging.warning("Pixel alteration occurred")
    print()
    logging.info("No pixel alteration occurred")
