import os
import sys
import pygame as pg

# https://nerdparadise.com/programming/pygame/part5
# https://realpython.com/pygame-a-primer


main_dir = getattr(sys, '_MEIPASS', os.path.split(os.path.abspath(__file__))[0])


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert_alpha()


def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


def load_sheet(sheet_file, size, img_x, img_y, image_count=0):
    sheet_file = os.path.join(main_dir, 'data', sheet_file)
    #sheet = load_image(sheet_file)
    try:
        sheet = pg.image.load(sheet_file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (sheet_file, pg.get_error()))
    sheet = sheet.convert_alpha()

    imgs = []
    cnt = 0

    if image_count == 0 or image_count > img_x * img_y:
        image_count = img_x * img_y
    for y in range(img_y):
        for x in range(img_x):
            rectangle = (size[0] + size[2] * x, size[1] + size[3] * y, size[2], size[3])

            rect = pg.Rect(rectangle)
            image = pg.Surface(rect.size, pg.SRCALPHA)
            image.blit(source=sheet, dest=(0, 0), area=rect)
            image = image.convert_alpha()
            #colorkey = image.get_at((0,0))
            #image.set_colorkey(colorkey, pg.RLEACCEL)
            imgs.append(image)
            cnt += 1
            if cnt == image_count:
                return imgs


def queue_sound(channel, sound):
    channel.queue(sound)


class DummySound:
    def play(self): pass


def load_sound(file):
    if not pg.mixer:
        return DummySound()
    file = os.path.join(main_dir, 'data', file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print('Warning, unable to load, %s' % file)
    return DummySound()


