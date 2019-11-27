import pygame as pg
import core

class SpiderRunDeco(pg.sprite.Sprite):
    speed = 8 #2
    animcycle = 16
    images = []

    def __init__(self, left, top):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.facing = SpiderRunDeco.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = core.WALLS.right
        self.pos = left
        self.limit = 150

    def set_position(self, value):
        if self.pos != value:
            self.pos = value

    def update(self):
        self.rect.move_ip(self.facing, 0)
        spr_offset = self.animcycle
        if self.facing < 0:
            spr_offset = 0

        if self.rect.x < self.pos - self.limit and self.facing < 0:
            self.facing = SpiderRunDeco.speed
        elif self.rect.x > self.pos + self.limit and self.facing > 0:
            self.facing = -SpiderRunDeco.speed
        else:
            pass

        self.frame = self.frame + 1

        # print(self.frame % self.animcycle + spr_offset)
        self.image = self.images[self.frame % self.animcycle + spr_offset]


class SpiderRun(pg.sprite.Sprite):
    speed = 8 #2
    animcycle = 16
    images = []
    waiting = False
    wait_cnt = 0
    age = 0

    def __init__(self, left, top):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.facing = SpiderRun.speed #random.choice((-1,1)) * Alien.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = core.WALLS.right
        self.walls = core.WALLS

    def update(self):
        if not self.waiting:
            self.rect.move_ip(self.facing, 0)
        spr_offset = self.animcycle
        if self.facing < 0:
            spr_offset = 0

        if self.rect.x < self.walls[0]:
            self.waiting = True
            self.wait_cnt += 1
            if self.wait_cnt > 100:
                self.waiting = False
                self.wait_cnt = 0
                self.age += 1

        if not self.waiting:
            if not self.walls.contains(self.rect):
                self.facing = -self.facing
                self.rect = self.rect.clamp(core.WALLS)

        self.frame = self.frame + 1

        # print(self.frame % self.animcycle + spr_offset)
        self.image = self.images[self.frame % self.animcycle + spr_offset]


class SpiderRunAggressive(SpiderRun):

    speed = 8
    animcycle = 8

    def __init__(self, left, top, idx, phase):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (left, top)
        self.frame = phase
        self.pos_x = 0
        self.pos_y = 0
        self.walk_x = left
        self.walk_y = top
        self.walk_speed_x = 0
        self.walk_speed_y = 0
        self.action = core.WALK_LEFT
        self.idx = idx
        self.wait = 0

    def update(self):
        spr_offset = self.animcycle
        self.frame = self.frame + 1
        self.image = self.images[self.frame % self.animcycle + spr_offset]

        self.rect = (self.walk_x, self.walk_y)

        if self.action == core.WALK_LEFT:
            self.rect = (self.walk_x, self.walk_y)
            if self.walk_x > self.pos_x:
                self.walk_x -= self.walk_speed_x
                self.walk_y += self.walk_speed_y
            else:
                if self.idx == 0:
                    self.set_action(core.CLIMB, self.walk_x, self.walk_y - 200, 0, 8)
                if self.idx == 1:
                    self.set_action(core.CLIMB, self.walk_x, self.walk_y - 170, 0, 4)
                if self.idx == 2:
                    self.set_action(core.CLIMB, self.walk_x, self.walk_y - 120, 0, 8)
                if self.idx == 3:
                    self.set_action(core.CLIMB, self.walk_x, self.walk_y - 100, 0, 2)
                if self.idx == 4:
                    self.set_action(core.CLIMB, self.walk_x, self.walk_y - 50, 0, 8)

        elif self.action == core.CLIMB:
            self.image = pg.transform.rotate(self.image, -90)
            if self.idx == 1 or self.idx == 3:
                self.image = pg.transform.flip(self.image, True, False)
            self.rect = (self.walk_x + 180, self.walk_y - 180)
            if self.idx == 1 or self.idx == 3:
                self.rect = (self.walk_x + 100, self.walk_y - 180)
            if self.walk_y > self.pos_y:
                self.walk_y -= self.walk_speed_y
                self.walk_x += self.walk_speed_x

    def set_action(self, action, pos_x, pos_y, walk_speed_x, walk_speed_y):
        self.action = action
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.walk_speed_x = walk_speed_x
        self.walk_speed_y = walk_speed_y


class SpiderAttack(pg.sprite.Sprite):
    speed = 8
    animcycle = 16
    images = []

    def __init__(self, left, top, start_sprite):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.start_sprite = start_sprite
        self.image = self.images[start_sprite]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.facing = SpiderAttack.speed #random.choice((-1,1)) * Alien.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = core.WALLS.right

    def update(self):
        # self.rect.move_ip(self.facing, 0)
        # if not WALLS.contains(self.rect):
        #     self.facing = -self.facing
        #     self.rect = self.rect.clamp(WALLS)
        self.frame = self.frame + 1

        # print(self.frame % self.animcycle + spr_offset)
        self.image = self.images[self.frame % self.animcycle + self.start_sprite]


class SpiderCrawlBig(pg.sprite.Sprite):
    speed = 1
    animcycle = 19
    images = []

    def __init__(self, left):

        pg.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = left
        #self.rect.top = top
        self.frame = 0
        if self.speed < 0:
            self.rect.right = core.WALLS.right
        self.killed = False

    def update(self):
        if not self.killed:
            self.rect.move_ip(0, self.speed)
        # if not WALLS.contains(self.rect):
        #     self.facing = -self.facing
        #     self.rect = self.rect.clamp(WALLS)
        self.frame = self.frame + 1

        # print(self.frame % self.animcycle)
        self.image = self.images[self.frame % self.animcycle]

