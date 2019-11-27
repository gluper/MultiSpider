import pygame as pg
from pygame.locals import *


class Score(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.SysFont("Arial", 30)
        self.font.set_italic(0)
        self.font.set_bold(1)
        self.color = Color('white')
        self.lastscore = -1
        self.score = 0
        self.update()
        self.rect = self.image.get_rect().move(10, 1040)

    def update(self):
        if self.score != self.lastscore:
            self.lastscore = self.score
            msg = "Score %d" % self.score
            self.image = self.font.render(msg, 1, self.color)

    def set_score(self, value):
        self.score = value

