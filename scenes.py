import pygame as pg
import math
import core

class Glass(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (581, 588)  # (780, 620) #(581, 588)
        self.stage = 0
        self.killing = False
        self.frame = 0

    def update(self):
        self.image = self.images[self.stage]
        if self.killing:
            self.frame += 1
            if self.frame > 20:
                self.kill()

    def kill_later(self):
        self.killing = True


class Cannon(pg.sprite.Sprite):
    animcycle = 16
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (1750, 788) # (1550, 788)
        self.speed = 0
        self.is_firing = False
        self.ready_to_fire = False
        self.loaded = False
        self.frame = 0

    def update(self):
        if self.rect.left < 1550:
            self.speed = 0
            if self.loaded:
                self.ready_to_fire = True
        if self.rect.left > 1750:
            # print(self.rect.left)
            self.speed = 0
        self.rect.move_ip(self.speed, 0)
        if self.speed == 0 and self.is_firing:
            self.loaded = False
            self.frame = self.frame + 1
            self.ready_to_fire = False
            # self.image = self.images[int(self.frame * 0.5) % self.animcycle]
            if self.frame == self.animcycle:
                self.is_firing = False
                self.frame = 0
            self.image = self.images[self.frame]

    def appear(self):
        self.loaded = True
        self.speed = -4
        self.rect.move_ip(self.speed, 0)

    def disappear(self):
        self.loaded = False
        self.speed = 4
        self.rect.move_ip(self.speed, 0)

    def fire(self):
        self.is_firing = True


class Fireball(pg.sprite.Sprite):
    animcycle = 6
    images = []

    def __init__(self, spider_crawling, precision):
        pg.sprite.Sprite.__init__(self, self.containers)
        target = spider_crawling.rect
        self.spider_crawling = spider_crawling
        self.precision = precision

        self.tx = target.centerx - 50
        if spider_crawling.speed == 2:
            # target is lower if spider has double speed
            self.ty = target.centery + 70
        else:
            self.ty = target.centery

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (1700, 870)
        self.x0 = 1700
        self.y0 = 870

        self.speed = int((self.x0 - self.tx) / 80)
        self.frame = 0
        self.x = self.x0
        self.y = self.y0

        self.cx = (self.x0 + self.tx) / 2
        self.cy = self.ty - 200

        if precision == 1:
            self.tx -= 150
            #self.ty += 150
            self.cy += 200
        if precision == -1:
            self.tx -= 150
            self.cy += 400
            self.ty += 400

        x1 = self.tx
        y1 = self.ty
        x2 = self.cx
        y2 = self.cy
        x3 = self.x0
        y3 = self.y0

        # https://www.arndt-bruenner.de/mathe/10/parabeldurchdreipunkte.htm
        self.a = (x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))/((x1-x2)*(x1-x3)*(x3-x2))
        self.b = (x1*x1*(y2-y3)+x2*x2*(y3-y1)+x3*x3*(y1-y2))/((x1-x2)*(x1-x3)*(x2-x3))
        self.c = (x1*x1*(x2*y3-x3*y2)+x1*(x3*x3*y2-x2*x2*y3)+x2*x3*y1*(x2-x3))/((x1-x2)*(x1-x3)*(x2-x3))
        self.deg = 0.0

    def update(self):
        self.frame += 1
        self.image = self.images[self.frame % self.animcycle]
        self.x -= self.speed
        y_old = self.y
        self.y = self.a * self.x * self.x + self.b * self.x + self.c

        self.deg = math.degrees(math.atan2(y_old - self.y, self.speed))
        self.image = pg.transform.rotate(self.image, -self.deg)

        # print(self.x, self.y)
        self.rect = (self.x, self.y)
        if self.x <= self.tx and self.y >= self.ty and self.precision == 0:
            self.kill()
            self.spider_crawling.killed = True

        if self.y > core.SCREENRECT[2]:
            self.kill()


class Explosion(pg.sprite.Sprite):

    def __init__(self, rect):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = (rect.x, rect.y + 30)
        self.frame = 0

    def update(self):
        if self.frame < len(self.images) - 1:
            self.frame += 1
        self.image = self.images[self.frame]
        if self.frame >= len(self.images):
            self.kill()


class Blaze(pg.sprite.Sprite):
    speed = 4

    def __init__(self, rect):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = rect.x
        self.rect.top = rect.y + 30
        self.frame = 0

    def update(self):
        self.rect.move_ip(0, Blaze.speed)
        if self.frame < len(self.images) - 1:
            self.frame += 1
        self.image = self.images[self.frame]
        if self.frame >= len(self.images):
            self.kill()


class SpiderExplosion(pg.sprite.Sprite):

    def __init__(self, rect):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = (rect.x - 75, rect.y - 20)
        self.frame = 0

    def update(self):
        if self.frame < len(self.images) - 1:
            self.frame += 1
        self.image = self.images[int(self.frame)]
        if self.frame >= len(self.images):
            self.kill()


class SpiderExplosion(pg.sprite.Sprite):

    def __init__(self, rect):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = (rect.x - 75, rect.y - 20)
        self.frame = 0

    def update(self):
        if self.frame < len(self.images) - 1:
            self.frame += 1
        self.image = self.images[int(self.frame)]
        if self.frame >= len(self.images):
            self.kill()


class Sparkle(pg.sprite.Sprite):
    path1 = [(1050, 210), (1062, 222), (1072, 235), (1079, 254), (1086, 273), (1091, 316), (1091, 363), (1087, 403),
             (1086, 455), (1078, 502), (1048, 565), (1012, 603), (972, 640), (932, 670), (877, 715), (811, 766),
             (725, 816), (659, 853), (578, 891)]

    path2 = [(1331, 189), (1340, 166), (1357, 150), (1377, 135), (1410, 118), (1445, 101), (1487, 91), (1532, 87),
             (1580, 88), (1622, 100), (1649, 135), (1674, 182), (1694, 239), (1698, 300), (1694, 396), (1680, 442),
             (1641, 509), (1567, 563), (1484, 574), (1414, 559), (1359, 511), (1357, 430), (1392, 352), (1440, 305),
             (1519, 283), (1602, 280), (1662, 297), (1735, 359), (1752, 420), (1753, 493), (1718, 569), (1668, 644),
             (1588, 717), (1496, 766), (1401, 805), (1297, 819), (1179, 823), (1067, 798), (965, 766), (863, 724),
             (741, 677), (679, 624), (608, 576), (550, 540), (481, 509), (404, 517), (330, 558), (283, 615),
             (298, 712), (371, 765), (470, 787), (552, 783), (623, 768), (689, 729), (736, 666), (741, 587),
             (717, 494), (651, 434), (580, 396), (481, 369), (470, 358), (462, 393), (436, 424), (319, 472), (252, 553)]

    path3 = [(165, 670), (256, 618), (388, 559)]

    path4 = [(875, 607), (829, 611), (775, 621), (730, 651), (693, 698), (669, 752), (652, 814), (683, 890), (744, 910),
             (806, 888), (842, 845), (854, 790), (823, 749), (783, 731)]

    path5 = [(927, 142), (969, 98), (1042, 74), (1125, 83), (1184, 129), (1215, 188), (1227, 274), (1198, 346),
             (1112, 395), (1046, 400), (985, 377), (942, 317), (938, 247), (968, 188), (1023, 163), (1086, 155),
             (1146, 190), (1187, 242), (1217, 305), (1249, 358), (1280, 434), (1314, 523), (1353, 656), (1389, 760),
             (1456, 874), (1553, 956), (1654, 1007), (1770, 1029), (1813, 1032)]

    path6 = [(1484, 637), (1588, 618), (1681, 619), (1766, 632), (1841, 672), (1896, 734), (1909, 811), (1884, 880),
             (1868, 900), (1858, 911)]

    # path2 = [(1050, 210), (1062, 222), (1072, 235), (1079, 254), (1086, 273), (1091, 316), (1091, 363), (1087, 403),
    #          (1086, 455), (1078, 502), (1048, 565), (1012, 603), (972, 640), (932, 670), (877, 715), (811, 766),
    #          (725, 816), (659, 853), (578, 891)]

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (-200, -200) # hide
        self.path = [()]
        self.frame = 0
        self.idx = 0.0
        self.posA = (0, 0)
        self.interp = 5
        self.interp_x = 0

    def update(self):
        if self.idx == 0:
            pos = self.path[int(self.idx)]
            self.posA = self.rect.topleft = (pos[0], pos[1])

        posB = self.path[int(self.idx) + 1]

        d = ((posB[0] - self.posA[0]) / self.interp, (posB[1] - self.posA[1]) / self.interp)
        self.rect.topleft = int(self.posA[0] + d[0] * self.interp_x - 128), int(self.posA[1] + d[1] * self.interp_x - 128)
        self.interp_x += 1
        #print(self.rect.topleft, self.interp_x)

        if self.interp_x == self.interp:
            self.interp_x = 0
            self.idx += 1
            self.posA = posB

        self.image = self.images[self.frame % len(self.images)]
        self.frame += 1
        #print(self.idx)
        if self.idx >= len(self.path) - 1:
            self.kill()


class BoardText(pg.sprite.Sprite):

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.frame = 0

    def set_board_image(self, num):
        self.image = self.images[num]


class Digits(pg.sprite.Sprite):

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.Surface((360, 84), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.frame = 0

    def set_text(self, text):
        # print(text)
        self.image = pg.Surface((360, 84), pg.SRCALPHA)

        idx = 0
        for s in text:
            if s == '*':
                i = 10
            elif s == '=':
                i = 11
            else:
                i = int(s)
            self.image.blit(self.images[i], (60 * idx, 0))
            idx += 1
        self.image = pg.transform.rotate(self.image, 33)


class Marks(pg.sprite.Sprite):

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.frame = 0

    def check_mark(self):
        self.image = pg.transform.rotate(self.images[0], 33)

    def strikeout(self):
        self.image = pg.transform.rotate(self.images[1], 33)


class Scroll(pg.sprite.Sprite):

    def __init__(self, icon):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (350, -700)
        self.speed = 0
        self.icon = icon
        self.frame = 0
        self.origin = self.images[0].copy()

    def update(self):
        if self.rect.top < -700:
            self.speed = 0
        if self.rect.top > -230:
            self.speed = 0
        self.rect.move_ip(0, self.speed)

    def appear(self):
        self.speed = 5
        self.rect.move_ip(0, self.speed)

    def disappear(self):
        self.speed = -5
        self.rect.move_ip(0, self.speed)

    def set_matrix(self, a, b):
        self.image = self.origin.copy()
        for x in range(0, a):
            if x > 3:
                offset_x = 110
            else:
                offset_x = 90
            for y in range(0, b):
                if y > 3:
                    offset_y = 260
                else:
                    offset_y = 240
                self.image.blit(self.icon, (x * 40 + offset_x, 780 - y * 40 - offset_y))

