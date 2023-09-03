# -*- coding: utf8 -*-
import screeninfo
from screeninfo import get_monitors
from pynput.keyboard import Key, Listener
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


def handle_key(key):
    VK_0_ROW = 222
    VK_1_ROW = 49
    try:
        if key in [Key.delete, Key.esc] or key.char == 'q':
            # Stop listener
            return False
        if key.vk == VK_0_ROW:
            apply_wallpaper(_picture_name)
        if key.vk in range(VK_1_ROW, VK_1_ROW + len(_monitors)):
            edit_wallpaper(key.vk - VK_1_ROW)
    except AttributeError:
        pass


def get_random_image_path():
    # TODO: move to optimize
    plist = io.open(conf.wallpaper_list_name, mode="r", encoding="utf-8")
    filecount = int(plist.readline())

    output_file = io.open(conf.wallpaper_used_list_name, mode="r", encoding="utf-8")
    rd = random.randint(1, filecount)
    # print("random ", rd)
    i = 0
    for line in plist:
        i += 1
        if i > rd:
            break
    outlist = []
    print(line)
    for wall in output_file:
        outlist.append(wall)
    output_file.close()
    outlist.reverse()
    output = io.open(conf.wallpaper_used_list_name, mode="w", encoding="utf-8")
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


def crop_wallpaper(wp, screen):
    wp_ratio = wp.shape[1] / wp.shape[0]
    screen_ratio = screen[0] / screen[1]
    if screen_ratio <= wp_ratio:
        # print("Crop horizontal")
        resize_factor = wp.shape[0] / screen[1]
        # print(resize_factor)
        resized_wp = cv2.resize(wp, dsize=(0, 0), fx=1 / resize_factor, fy=1 / resize_factor,
                                interpolation=cv2.INTER_AREA)
        crop_value = int((resized_wp.shape[1] - screen[0]) / 2)
        # print(crop_value)
        cropped_wp = resized_wp[0:screen[1], crop_value:crop_value + screen[0]]
    else:
        # print("Crop vertical")
        resize_factor = wp.shape[1] / screen[0]
        # print(resize_factor)
        resized_wp = cv2.resize(wp, dsize=(0, 0), fx=1 / resize_factor, fy=1 / resize_factor,
                                interpolation=cv2.INTER_AREA)
        crop_value = int((resized_wp.shape[0] - screen[1]) / 2)
        # print(crop_value)
        cropped_wp = resized_wp[crop_value:crop_value + screen[1], 0:screen[0]]
    return cropped_wp


def edit_wallpaper(monitor):
    print(monitor)
    img_path = get_random_image_path()
    screen_size = (_monitors[monitor].width, _monitors[monitor].height)
    # Read picture
    base_wp = 0
    try:
        stream = open(img_path, 'rb')
        pbytes = bytearray(stream.read())
        numpyarray = numpy.asarray(pbytes, dtype=numpy.uint8)
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
    cropped_wp = crop_wallpaper(base_wp, screen_size)
    x_pos = _monitors[monitor].x - _picture_size[2]['xmin']
    y_pos = _monitors[monitor].y - _picture_size[2]['ymin']
    _current_wp[y_pos:y_pos+_monitors[monitor].height, x_pos:x_pos+_monitors[monitor].width] = cropped_wp
    cv2.imwrite(_picture_name, _current_wp)
    apply_wallpaper(_picture_name)


def apply_wallpaper(path):
    SPI_SETDESKWALLPAPER = 20
    full_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), path)
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, full_path, 0)
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


def get_picture_size(monitors: list):
    picture_limits = {'xmin': 0, 'xmax': 0, 'ymin': 0, 'ymax': 0}
    for monitor in monitors:
        picture_limits['xmin'] = min(picture_limits['xmin'], monitor.x)
        picture_limits['xmax'] = max(picture_limits['xmax'], monitor.x + monitor.width)
        picture_limits['ymin'] = min(picture_limits['ymin'], monitor.y)
        picture_limits['ymax'] = max(picture_limits['ymax'], monitor.y + monitor.height)
    picture_size = [picture_limits['xmax'] - picture_limits['xmin'], picture_limits['ymax'] - picture_limits['ymin'], picture_limits]
    return picture_size


def order_monitors(monitors: list):
    # Currently only sorting horizontally because that's my setup and I'm lazy
    monitors.sort(key=lambda el: el.x)


""" CONF FILE
monitor_count
monitor_sizes
monitor_vert_offset

"""

# 2 modes :
# - interactif : lance une fenêtre ou on saisi le num de l'écran à changer, en while(true) qui se ferme si echap
# - "classique" : appel avec l'ID de l'écran pour 1 changement

log = set_logger("wallpaperChanger")
random.seed()
_monitors = get_monitors()
print(_monitors)
order_monitors(_monitors)
_picture_size = get_picture_size(_monitors)
print(_picture_size)

_picture_name = conf.wallpaper_base_name.format(width=_picture_size[0], height=_picture_size[1])
_current_wp = cv2.imread(_picture_name)
if _current_wp is None:
    print("No file matching this size, creating it")
    _current_wp = numpy.zeros((_picture_size[1], _picture_size[0], 3), numpy.int8)
    cv2.imwrite(_picture_name, _current_wp)

# Collect all event until released
with Listener(on_press = handle_key) as listener:
    listener.join()

