# -*- coding: utf8 -*-
import logging
import random
import ctypes
import cv2
import numpy
import io
import os
import sys
from datetime import datetime


def edit_wallpaper(side, path):
    if side == "left":
        print("Change left wallpaper")
        screen_size = (1280, 1024)
    elif side == 'right':
        print("Change right wallpaper")
        screen_size = (1920, 1080)
    else:
        print("Error")
        return
    # Open file (support Unicode)
    base_wp = 0
    try:
        stream = open(path, 'rb')
        bytes = bytearray(stream.read())
        numpyarray = numpy.asarray(bytes, dtype=numpy.uint8)
        base_wp = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
    except cv2.error as err:
        log.warning(err)
        return
    except IOError as err:
        log.warning(err)
        return
    if base_wp.shape[2] == 4:
        # remove png alpha
        base_wp = cv2.cvtColor(base_wp, cv2.COLOR_BGRA2BGR)
    wp_ratio = base_wp.shape[1] / base_wp.shape[0]
    screen_ratio = screen_size[0] / screen_size[1]

    if screen_ratio <= wp_ratio:
        print("Crop horizontal")
        resize_factor = base_wp.shape[0] / screen_size[1]
        print(resize_factor)
        resized_wp = cv2.resize(base_wp, dsize=(0, 0), fx=1 / resize_factor, fy=1 / resize_factor,
                                interpolation=cv2.INTER_AREA)
        crop_value = int((resized_wp.shape[1] - screen_size[0]) / 2)
        print(crop_value)
        cropped_wp = resized_wp[0:screen_size[1], crop_value:crop_value + screen_size[0]]
    else:
        print("Crop vertical")
        resize_factor = base_wp.shape[1] / screen_size[0]
        print(resize_factor)
        resized_wp = cv2.resize(base_wp, dsize=(0, 0), fx=1 / resize_factor, fy=1 / resize_factor,
                                interpolation=cv2.INTER_AREA)
        crop_value = int((resized_wp.shape[0] - screen_size[1]) / 2)
        print(crop_value)
        cropped_wp = resized_wp[crop_value:crop_value + screen_size[1], 0:screen_size[0]]
    if side == 'left':
        currentwp[56:1080, 0:1280] = cropped_wp
    if side == 'right':
        currentwp[0:1080, 1280:3200] = cropped_wp


def setLogger(name):
    logger = logging.getLogger(name)
    log_path = os.path.join(os.getcwd(), name + ".log")
    logger.setLevel(20)  # ignore debug
    handler = logging.FileHandler(filename=log_path, encoding='utf-8', mode='a+')
    handler.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    return logger


"""MAIN"""
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
log = setLogger("set_as")
if len(sys.argv) > 2:
    mode = sys.argv[1]
    path = sys.argv[2]
    print(mode, ": ", path)
    if mode != 'left' and mode != 'right':
        print("Error")
        exit(1)
else:
    print("Error")
    exit(1)

random.seed()
currentwp = cv2.imread("wallpaper.jpg")

edit_wallpaper(mode, path)
cv2.imwrite("wallpaper.jpg", currentwp)

SPI_SETDESKWALLPAPER = 20
ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, "D:\Developement\WallpaperChanger\wallpaper.jpg", 0)
