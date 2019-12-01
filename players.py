import pygame as pg
import core


class PlayerBase(pg.sprite.Sprite):
    images_idle = []
    images_pity = []
    images_thinking = []
    images_excited = []
    images_walk_left = []
    images_walk_right = []
    images_look_right = []
    images_throw = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images_pity[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (320, 420)  # (780, 620) #(581, 588)
        self.frame = 0
        self.action = core.PITY
        self.start_phase = False
        self.speed = 1.0
        self.thinking_repeat_index = 9
        self.walk_x = 1000.0
        self.walk_y = 500.0
        self.walk_speed_x = 4.0
        self.walk_speed_y = 0.1

        self.self_deactivation = 0
        self.x_end = 0
        self.x_start = 0

    def update(self):
        if self.action == core.IDLE:
            self.image = self.images_idle[int(self.frame * self.speed % len(self.images_idle))]
            self.frame += 1
        elif self.action == core.PITY:
            idx = int(self.frame * self.speed)
            # print(idx)
            self.image = self.images_pity[idx]
            if idx < len(self.images_pity) - 1:
                self.frame += 1
            else:
                # relax after 100 frames
                self.self_deactivation += 1
                if self.self_deactivation > 100:
                    self.self_deactivation = 0
                    self.set_action(core.IDLE)

        elif self.action == core.LONG_PITY:
            idx = int(self.frame * self.speed)
            # print(idx)
            self.image = self.images_pity[idx]
            if idx < len(self.images_pity) - 1:
                self.frame += 1

        elif self.action == core.THINKING:
            #if self.start_phase:
            idx = int(self.frame * self.speed)
            if idx > len(self.images_thinking) - 1:
                self.speed = 0.1
                # self.start_phase = False
                self.frame = int(self.thinking_repeat_index / self.speed)
                idx = self.thinking_repeat_index #len(self.images_thinking) - 1
                #print("stop")
            # print(idx)
            self.image = self.images_thinking[idx]
            self.frame += 1
        elif self.action == core.EXCITEMENT:
            idx = int(self.frame * self.speed)
            # print(idx)
            self.image = self.images_excited[idx]
            if idx < len(self.images_excited) - 1:
                self.frame += 1
            else:
                # relax after 1 sec
                self.self_deactivation += 1
                if self.self_deactivation > 40:
                    self.self_deactivation = 0
                    self.set_action(core.IDLE)

        elif self.action == core.WALK_LEFT:
            if self.walk_x > self.x_end:
                self.walk_x -= self.walk_speed_x
                self.walk_y -= self.walk_speed_y
                # print(self.walk_x, self.walk_y)
                self.rect = (self.walk_x, self.walk_y)
            else:
                self.set_action(core.IDLE)
            self.image = self.images_walk_left[int(self.frame * self.speed % len(self.images_walk_left))]
            self.frame += 1

        elif self.action == core.WALK_RIGHT:
            if self.walk_x < self.x_end:
                self.walk_x += self.walk_speed_x
                self.walk_y += self.walk_speed_y
                # print(self.walk_x, self.walk_y)
                self.rect = (self.walk_x, self.walk_y)
            else:
                self.set_action(core.IDLE)
            self.image = self.images_walk_right[int(self.frame * self.speed % len(self.images_walk_right))]
            self.frame += 1

        elif self.action == core.THROW:
            idx = int(self.frame * self.speed)
            self.image = self.images_throw[idx]
            if idx < len(self.images_throw) - 1:
                self.frame += 1

        elif self.action == core.STOP:
            pass

        elif self.action == core.LOOK_RIGHT:
            self.image = self.images_look_right[0]

    def set_action(self, action):
        if action == core.THINKING:
            self.speed = 0.1
        elif action == core.PITY or action == core.LONG_PITY:
            self.speed = 0.2
        elif action == core.EXCITEMENT:
            self.speed = 0.2
        elif action == core.IDLE:
            self.speed = 0.1
        elif action == core.WALK_LEFT or action == core.WALK_RIGHT:
            self.speed = 0.1
        elif action == core.THROW:
            self.speed = 0.2
        # self.start_phase = True
        self.action = action
        self.frame = 0

    def walk_left(self, x_begin, x_end, walk_speed, speed):
        self.walk_x = x_begin
        self.x_start = x_begin
        self.x_end = x_end
        self.action = core.WALK_LEFT
        self.walk_speed_x = walk_speed
        self.walk_speed_y = walk_speed / 10.0
        self.speed = speed

    def walk_right(self, x_begin, x_end, walk_speed, speed):
        self.walk_x = x_begin
        self.x_start = x_begin
        self.x_end = x_end
        self.action = core.WALK_RIGHT
        self.walk_speed_x = walk_speed
        self.walk_speed_y = walk_speed / 10.0
        self.speed = speed


class Player1(PlayerBase):
    def __init__(self):
        PlayerBase.__init__(self)
        self.jump_idx = 4
        self.thinking_repeat_index = 6


class Player2(PlayerBase):
    def __init__(self):
        PlayerBase.__init__(self)
        self.jump_idx = 4
        self.thinking_repeat_index = 8


class Player3(PlayerBase):
    def __init__(self):
        PlayerBase.__init__(self)
        self.jump_idx = 6
        self.thinking_repeat_index = 9


class Fairy(pg.sprite.Sprite):
    images_flight_idle_right = []
    images_flight_idle_left = []
    images_flight_cool_left = []
    images_flight_anx = []
    images_flight_magic = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images_flight_idle_right[0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.action = core.IDLE

        self.walk_x = 1000.0
        self.walk_y = 500.0
        self.walk_speed_x = 2.0
        self.walk_speed_y = 2.0
        self.speed = 1

        self.self_deactivation = 0
        self.x_end = 0
        self.x_start = 0
        self.action = core.IDLE

        self.frameY = 0
        self.heights = [-20, -19, -17, - 15, -12, -9, -5, 0, 5, 9, 12, 15, 17, 19,
                         20, 19,   17,   15,  12,  9,  5, 0, -5, -9, -12, -15, -19]

        self.cool_heights = [-4, -4, -3, - 2, -1, -1, -1, 0, 1, 1, 1, 2, 3, 4,
                        4, 4,   3,   2,  1,  1,  1, 0, 0, -1, -1, -2, -3]

    def update(self):
        if self.frameY >= len(self.heights) - 1:
            self.frameY = 0
        self.frameY += 1
        if self.action == core.COOL:
            self.rect = (self.walk_x, self.walk_y + self.cool_heights[self.frameY])
        else:
            self.rect = (self.walk_x, self.walk_y + self.heights[self.frameY])
        if self.action == core.WALK_RIGHT:
            if self.walk_x < self.x_end:
                self.walk_x += self.walk_speed_x
                # print(self.walk_x, self.walk_y)
                # self.rect = (self.walk_x, self.walk_y)
            #else:
            #    self.set_action(core.IDLE)
            self.image = self.images_flight_idle_right[int(self.frame * self.speed % len(self.images_flight_idle_right))]
            self.frame += 1
        elif self.action == core.WALK_LEFT:
            if self.walk_x > self.x_end:
                self.walk_x -= self.walk_speed_x
                self.walk_y += self.walk_speed_y
            self.image = self.images_flight_idle_left[int(self.frame * self.speed % len(self.images_flight_idle_left))]
            self.frame += 1
        elif self.action == core.WALK_LEFT_BACKWARDS:
            if self.walk_x < self.x_end:
                self.walk_x += self.walk_speed_x
            self.image = self.images_flight_idle_left[int(self.frame * self.speed % len(self.images_flight_idle_left))]
            self.frame += 1
        elif self.action == core.IDLE:
            self.frame += 1
            self.image = self.images_flight_idle_right[self.frame % len(self.images_flight_idle_right)]
        elif self.action == core.ANXIOUS:
            self.frame += 1
            self.image = self.images_flight_anx[self.frame % len(self.images_flight_anx)]
        elif self.action == core.MAGIC:
            self.frame += 1
            self.image = self.images_flight_magic[self.frame % len(self.images_flight_magic)]
        elif self.action == core.COOL:
            self.frame += 1
            self.image = self.images_flight_cool_left[self.frame % len(self.images_flight_cool_left)]

    def fly_right(self, x_begin, x_end, walk_speed, speed):
        self.walk_x = x_begin
        self.x_start = x_begin
        self.x_end = x_end
        self.action = core.WALK_RIGHT
        self.walk_speed_x = walk_speed
        self.speed = speed

    def fly_left(self, x_begin, x_end, walk_speed_x, walk_speed_y, speed):
        self.walk_x = x_begin
        self.x_start = x_begin
        self.x_end = x_end
        self.action = core.WALK_LEFT
        self.walk_speed_x = walk_speed_x
        self.walk_speed_y = walk_speed_y
        self.speed = speed

    def fly_left_backwards(self, x_begin, x_end, walk_speed, speed):
        self.walk_x = x_begin
        self.x_start = x_begin
        self.x_end = x_end
        self.action = core.WALK_LEFT_BACKWARDS
        self.walk_speed_x = walk_speed
        self.speed = speed

