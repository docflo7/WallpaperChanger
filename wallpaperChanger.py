# -*- coding: utf8 -*-
from screeninfo import get_monitors
import conf
import logging
import random
import ctypes
import cv2
import numpy
import io
import os
import sys
from datetime import datetime


def get_random_image_path():
    output_file = io.open(conf.wallpaper_used_list_name, mode="r", encoding="utf-8")
    rd = random.randint(1, filecount)
    print("random ", rd)
    i = 0
    for line in list:
        i += 1
        if i > rd:
            break
    outlist = []
    for wall in output_file:
        outlist.append(wall)
    output_file.close()
    outlist.reverse()
    output = io.open(used_path, mode="w", encoding="utf-8")
    output.write(datetime.now().isoformat(' ') + ' ' + line)
    for i in range(9):
        try:
            pop = outlist.pop()
        except:
            break
        output.write(pop)
    return line[:-1].replace(os.sep, '/')


def get_last_image_path(monitor):
    return "path"


def write_to_path_file(monitor, path):
    return True


def remove_from_path_file(monitor):
    return True


def edit_wallpaper(monitor, path):
    return True


def apply_wallpaper(path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
    return True


def build_file_list():
    return True


def set_logger(logger_name):
    logger = logging.getLogger(logger_name)
    log_path = os.path.join(os.getcwd(), logger_name + ".log")  # TODO: this may not be the right location
    logger.setLevel(20)  # ignore debug
    handler = logging.FileHandler(filename=log_path, encoding='utf-8', mode='a+')
    handler.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    return logger


def get_picture_size(monitors):
    picture_limits = {'xmin': 0, 'xmax': 0, 'ymin': 0, 'ymax': 0}
    for monitor in monitors:
        picture_limits['xmin'] = min(picture_limits['xmin'], monitor.x)
        picture_limits['xmax'] = max(picture_limits['xmax'], monitor.x + monitor.width)
        picture_limits['ymin'] = min(picture_limits['ymin'], monitor.y)
        picture_limits['ymax'] = max(picture_limits['ymax'], monitor.y + monitor.height)
    picture_size = [picture_limits['xmax'] - picture_limits['xmin'], picture_limits['ymax'] - picture_limits['ymin']]
    return picture_size


""" CONF FILE
monitor_count
monitor_sizes
monitor_vert_offset

"""


random.seed()
_monitors = get_monitors()
_picture_size = get_picture_size(_monitors)
_picture_name = conf.wallpaper_base_name.format(width=_picture_size[0], height=_picture_size[1])
_current_wp = cv2.imread(_picture_name)
if _current_wp is None:
    print("No file matching this size, creating it")
    _current_wp = numpy.zeros((_picture_size[1], _picture_size[0], 3), numpy.int8)
    # cv2.imwrite(_picture_name, _current_wp)


