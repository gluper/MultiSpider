import pygame as pg
import core


class PlayerSelectionBase(pg.sprite.Sprite):
    images = []

    def __init__(self, left, top):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.frame = 0

    def update(self):

        self.frame = self.frame + 1

        # print(self.frame % len(self.images))
        self.image = self.images[int(self.frame * 0.1) % len(self.images)]


class PlayerSelection1(PlayerSelectionBase):
    pass


class PlayerSelection2(PlayerSelectionBase):
    pass


class PlayerSelection3(PlayerSelectionBase):
    pass
