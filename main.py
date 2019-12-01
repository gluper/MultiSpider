import os
import random
import json
import logging
import pygame as pg
import datetime
import core
from pygame.locals import *

from spider import SpiderRun, SpiderAttack, SpiderCrawlBig, SpiderRunDeco, SpiderRunAggressive
from scenes import Glass, Cannon, Fireball, Explosion, Blaze, SpiderExplosion, Sparkle, BoardText, Digits, Marks, Scroll, Joker
from intro import PlayerSelection1, PlayerSelection2, PlayerSelection3
from fonts import Score
from players import Player1, Player2, Player3, Fairy
from utils import load_sound, load_image, load_images, load_sheet, main_dir


def main(winstyle = 0):

    # Initialize pygame
    pg.init()

    if os.path.isfile("fullscreen"):
        win = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
        p = pg.display.list_modes(depth=0, flags=pg.FULLSCREEN)
    else:
        win = pg.display.set_mode((1920, 1080))
        p = pg.display.list_modes(depth=0)

    #decorate the game window
    #icon = pg.transform.scale(Alien.images[0], (32, 32))
    #pg.display.set_icon(icon)
    pg.display.set_caption('MultiSpider')
    pg.mouse.set_visible(0)

    logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(message)s')
    logging.info('-----------------------------------------------------------')
    logging.info('Application started ' + str(datetime.datetime.now()))

    players = load_players_data()

    while play(players, win):
        pass

    logging.info('Application closed ' + str(datetime.datetime.now()))


def load_players_data():
    with open(os.path.join("data", "players.json"), "r") as read_file:
        p_data = json.load(read_file)
        players = p_data['players']
        return players


def save_players_data(players):
    with open(os.path.join("data", "players.json"), "w") as write_file:
        json.dump({'players': players}, write_file)


def play(players, win):
    brick = load_image('brick-wall.jpg')
    win.blit(brick, (0, 0))
    pg.display.flip()

    last_tick = pg.time.get_ticks()

    font_loading = pg.font.SysFont("comicsansms", 72)
    ren = font_loading.render("Loading...", 1, Color('white'))
    win.blit(ren, (600, 400))
    pg.display.flip()

    bg = load_image('bg2.jpg')
    snd_snake = load_sound('snake.wav')

    music_monsters = os.path.join(main_dir, 'data', 'monsters.mp3')
    if pg.mixer:
        pg.mixer.music.load(music_monsters)
        pg.mixer.music.play(-1)

    player_selection_scene = pg.sprite.RenderUpdates()
    intro_scene = pg.sprite.RenderUpdates()
    main_scene = pg.sprite.RenderUpdates()
    game_over_scene = pg.sprite.RenderUpdates()

    PlayerSelection1.images = load_images(*['ga' + str(i).zfill(2) + '.png' for i in range(1, 21)])
    PlayerSelection2.images = load_images(*['gl' + str(i).zfill(2) + '.png' for i in range(1, 22)])
    PlayerSelection3.images = load_images(*['gn' + str(i).zfill(2) + '.png' for i in range(1, 16)])

    PlayerSelection1.containers = player_selection_scene
    PlayerSelection2.containers = player_selection_scene
    PlayerSelection3.containers = player_selection_scene

    player_selection1 = PlayerSelection1(100, 93)
    player_selection2 = PlayerSelection2(680, 93)
    player_selection3 = PlayerSelection3(1200, 93)

    SpiderRunDeco.images = load_images('w0.png', 'w1.png', 'w2.png', 'w3.png', 'w4.png',
                                   'w5.png', 'w6.png', 'w7.png', 'w8.png', 'w9.png',
                                   'w10.png', 'w11.png', 'w12.png', 'w13.png', 'w14.png', 'w15.png')
    for i in range(0, 16):
        SpiderRunDeco.images.append(pg.transform.flip(SpiderRunDeco.images[15-i], True, False))

    SpiderRunDeco.containers = player_selection_scene, game_over_scene

    font_player = pg.font.SysFont("comicsansms", 72)
    text_select_player = font_player.render("Select player", 1, Color('white'))
    font_score = pg.font.SysFont("comicsansms", 36)
    font_hint = pg.font.SysFont("arial", 24)
    text_hint = font_hint.render('Use <Arrow> keys and <Enter>. <Esc> to exit', 1, Color('white'))
    # font_score.set_bold(1)
    text_highscores = font_score.render("High scores", 1, Color('white'))
    text_awards = font_score.render("Awards", 1, Color('white'))
    text_score0 = font_score.render(str(players[0]['high_score']), 1, Color("white"))
    text_score1 = font_score.render(str(players[1]['high_score']), 1, Color("white"))
    text_score2 = font_score.render(str(players[2]['high_score']), 1, Color("white"))
    awards0 = players[0]['awards']
    awards1 = players[1]['awards']
    awards2 = players[2]['awards']

    star = load_image('star.png')

    win.blit(brick, (0, 0))
    pg.display.flip()

    clock = pg.time.Clock()

    selected = False
    spider_deco = SpiderRunDeco(300, 780)
    spider_deco.set_position(300)
    selection = 0

    while not selected:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                return False

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            pg.quit()
            logging.info('Aborted ' + str(datetime.datetime.now()))
            return False

        if keys[pg.K_RIGHT]:
            now_tick = pg.time.get_ticks()
            if now_tick - last_tick > 2000:
                last_tick = now_tick
                selection = min(2, selection + 1)
        if keys[pg.K_LEFT]:
            now_tick = pg.time.get_ticks()
            if now_tick - last_tick > 2000:
                last_tick = now_tick
                selection = max(0, selection - 1)

        if selection == 0 and spider_deco.pos != 300:
            spider_deco.set_position(300)
            pg.mixer.Channel(0).play(snd_snake)
        elif selection == 1 and spider_deco.pos != 900:
            spider_deco.set_position(900)
            pg.mixer.Channel(0).play(snd_snake)
        elif selection == 2 and spider_deco.pos != 1500:
            spider_deco.set_position(1500)
            pg.mixer.Channel(0).play(snd_snake)

        if keys[pg.K_RETURN] or keys[pg.K_SPACE]:
            break

        player_selection_scene.clear(win, brick)
        player_selection_scene.update()

        win.blit(text_select_player, (400, 50))
        win.blit(text_highscores, (20, 950))
        win.blit(text_awards, (20, 1000))
        win.blit(text_score0, (350, 950))
        win.blit(text_score1, (950, 950))
        win.blit(text_score2, (1550, 950))
        win.blit(text_hint, (1500, 1050))

        for i in range(0, min(awards0, 15)):
            win.blit(star, (350 + i * 35, 1010))
        for i in range(0, min(awards1, 15)):
            win.blit(star, (950 + i * 35, 1010))
        for i in range(0, min(awards2, 15)):
            win.blit(star, (1550 + i * 35, 1010))

        # draw the scene
        dirty = player_selection_scene.draw(win)
        #pg.display.update(dirty)
        pg.display.flip()

        # cap the framerate
        clock.tick(40)

    ####################################################################
    logging.info('Player: ' + players[selection].get('name', '?'))
    if pg.mixer:
        pg.mixer.music.fadeout(1000)
    spider_deco.kill()
    win.blit(bg, (0, 0))
    time_start_game = datetime.datetime.now()

    ren = font_loading.render("Loading...", 1, Color('white'))
    win.blit(ren, (600, 600))
    board = load_image('board.png')
    bg3 = load_image('bg3.jpg')
    game_over_txt = load_image('game_over.png')
    text_hint = font_hint.render('<Esc> to skip intro', 1, Color('black'))
    icon = load_image('spider_small.png')
    win.blit(text_hint, (1600, 1050))
    pg.display.flip()

    # clear no more need sprites
    player_selection1.kill()
    player_selection2.kill()
    player_selection3.kill()

    level = max(min(players[selection].get('level', 1), 2), 0)
    multiplier = max(min(players[selection].get('multiplier', 9), 9), 2) + 1
    logging.info('Level ' + str(level) + '. Multiplier ' + str(multiplier - 1))

    table = []
    for method in range(0, 3):
        for i in range(2, multiplier):
            for j in range(2, multiplier):
                # limit matrix method to 8x8
                if method == core.MATRIX and i > 8 or j > 8:
                    continue
                table.append((i, j, method))
    random.shuffle(table)
    random.shuffle(table)
    random.shuffle(table)
    # pool of wrong answers
    pool = []

    Player1.images_idle = load_images(*['aid' + str(i).zfill(2) + '.png' for i in range(1, 9)])
    Player1.images_pity = load_images(*['apt0' + str(i) + '.png' for i in range(1, 10)])
    Player1.images_thinking = load_images(*['ath' + str(i).zfill(2) + '.png' for i in range(1, 11)])
    Player1.images_excited = load_images(*['aex' + str(i).zfill(2) + '.png' for i in range(1, 10)])
    Player1.images_walk_right = load_images(*['awl' + str(i).zfill(2) + '.png' for i in range(1, 10)])
    Player1.images_walk_left = [pg.transform.flip(Player1.images_walk_right[i], True, False) for i in range(0, 6)]
    Player1.images_look_right = load_images('alr0.png')
    Player1.images_throw = load_images(*['atr' + str(i).zfill(2) + '.png' for i in range(1, 19)])

    Player2.images_idle = load_images(*['lid' + str(i).zfill(2) + '.png' for i in range(1, 7)])
    Player2.images_pity = load_images(*['lpt0' + str(i) + '.png' for i in range(1, 10)])
    Player2.images_thinking = load_images(*['lth' + str(i).zfill(2) + '.png' for i in range(1, 12)])
    Player2.images_excited = load_images(*['lex' + str(i).zfill(2) + '.png' for i in range(1, 9)])
    Player2.images_walk_right = load_images(*['lwl' + str(i).zfill(2) + '.png' for i in range(1, 7)])
    Player2.images_walk_left = [pg.transform.flip(Player2.images_walk_right[i], True, False) for i in range(0, 6)]
    Player2.images_look_right = load_images('llr0.png')
    Player2.images_throw = load_images(*['ltr' + str(i).zfill(2) + '.png' for i in range(1, 16)])

    Player3.images_idle = load_images(*['nid' + str(i).zfill(2) + '.png' for i in range(1, 8)])
    Player3.images_pity = load_images(*['npt0' + str(i) + '.png' for i in range(1, 9)])
    Player3.images_thinking = load_images(*['nth' + str(i).zfill(2) + '.png' for i in range(1, 14)])
    Player3.images_excited = load_images(*['nex' + str(i).zfill(2) + '.png' for i in range(1, 11)])
    Player3.images_walk_right = load_images(*['nwl' + str(i).zfill(2) + '.png' for i in range(1, 7)])
    Player3.images_walk_left = [pg.transform.flip(Player3.images_walk_right[i], True, False) for i in range(0, 6)]
    Player3.images_look_right = load_images('nlr0.png')
    Player3.images_throw = load_images(*['ntr' + str(i).zfill(2) + '.png' for i in range(1, 16)])

    Fairy.images_flight_idle_right = load_images(*['tb' + str(i).zfill(2) + '.png' for i in range(1, 13)])
    Fairy.images_flight_idle_left = load_images(*['tbl' + str(i).zfill(2) + '.png' for i in range(1, 13)])
    Fairy.images_flight_cool_left = load_images(*['tbt' + str(i).zfill(2) + '.png' for i in range(1, 13)])
    Fairy.images_flight_anx = load_images(*['tba' + str(i).zfill(2) + '.png' for i in range(1, 13)])
    Fairy.images_flight_magic = load_images(*['tbm' + str(i).zfill(2) + '.png' for i in range(1, 13)])

    Sparkle.images = load_sheet('sparkles.png', (0, 0, 256, 256), 4, 4, 16)

    SpiderRun.images = load_images('w0.png', 'w1.png', 'w2.png', 'w3.png', 'w4.png',
                                   'w5.png', 'w6.png', 'w7.png', 'w8.png', 'w9.png',
                                   'w10.png', 'w11.png', 'w12.png', 'w13.png', 'w14.png', 'w15.png')
    for i in range(0, 16):
        SpiderRun.images.append(pg.transform.flip(SpiderRun.images[15-i], True, False))

    SpiderAttack.images = load_images('a0.png', 'a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png', 'a6.png', 'a7.png',
                                'a8.png', 'a9.png', 'a10.png', 'a11.png', 'a12.png', 'a13.png', 'a14.png', 'a15.png')

    for i in range(0, 16):
        SpiderAttack.images.append(pg.transform.rotate(SpiderAttack.images[i], 270))

    SpiderCrawlBig.images = load_sheet('spider_crawl.png', (0, 0, 120, 148), 4, 5, 19)
    Glass.images = load_images('g1.png', 'g2.png', 'g3.png', 'g4.png', 'g5.png')

    Cannon.images = load_images('c1.png', 'c2.png', 'c3.png', 'c4.png', 'c5.png', 'c6.png', 'c7.png', 'c8.png',
                                'c9.png', 'c10.png', 'c11.png', 'c12.png', 'c13.png', 'c14.png', 'c15.png', 'c16.png')

    Fireball.images = load_images('b1.png', 'b2.png', 'b3.png', 'b4.png', 'b5.png', 'b6.png')

    Explosion.images = load_images(*['ex' + str(i) + '.png' for i in range(1, 25)])
    SpiderExplosion.images = load_images(*['spex' + str(i).zfill(2) + '.png' for i in range(1, 12)])

    Blaze.images = load_images(*[os.path.join('br', 'br' + str(i) + '.png') for i in range(1, 217)])

    BoardText.images = load_images('txt_clear.png', 'txt_angst.png', 'txt_helfen.png', 'txt_wand.png', 'txt_cannon.png',
                                   'txt_reload.png', 'txt_tasks.png', 'txt_luck.png', 'txt_count.png', 'txt_listen.png')

    Digits.images = load_images('d0.png', 'd1.png', 'd2.png', 'd3.png', 'd4.png', 'd5.png', 'd6.png', 'd7.png',
                                'd8.png', 'd9.png', 'dx.png', 'de.png')

    Marks.images = load_images('check.png', 'error.png')

    Scroll.images = load_images('scroll.png')

    Joker.images = load_images(*['j' + str(i).zfill(2) + '.png' for i in range(1, 10)])

    #load the sound effects
    snd_numbers = []
    for i in range(0, 10):
        snd_numbers.append(load_sound('d' + str(i) + '.ogg'))
    snd_mal = load_sound('mal.ogg')
    snd_bang = load_sound('banging.wav')
    snd_break = load_sound('breaking.wav')
    snd_shot = load_sound('shot.wav')
    snd_burning = load_sound('burning.wav')
    snd_explosion = load_sound('explosion.wav')
    snd_door = load_sound('lidcreak.wav')
    snd_wicked_laugh = load_sound('bah.wav')
    snd_scream = load_sound('scream.wav')
    snd_magic = load_sound('magic_spell.wav')
    snd_dundundun = load_sound('dundundun.wav')
    snd_knocking = load_sound('knocking.wav')
    snd_joker = load_sound('laugh.wav')
    snd_thunder = load_sound('thunder.wav')
    snd_fireball = load_sound('fireball.wav')
    snd_shutter = load_sound('shutter.wav')

    if pg.mixer:
        music = os.path.join(main_dir, 'data', 'Halloween.mp3')
        music_chase = os.path.join(main_dir, 'data', 'chase.mp3')
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1) # music

    SOUND_END = pg.USEREVENT + 1
    chn0 = pg.mixer.Channel(0)
    chn0.set_endevent(SOUND_END)
    chn1 = pg.mixer.Channel(1)
    chn2 = pg.mixer.Channel(2)

    NEW_ROUND = pg.USEREVENT + 2
    NEW_POOL_TASK = pg.USEREVENT + 3

    # Initialize Game Groups
    group_all_spiders = pg.sprite.Group()
    group_running_spiders = pg.sprite.Group()
    group_attacking_spiders = pg.sprite.Group()

    #assign default groups to each sprite class
    SpiderAttack.containers = group_attacking_spiders, group_all_spiders, main_scene
    SpiderRun.containers = group_all_spiders, group_running_spiders, main_scene, intro_scene
    SpiderCrawlBig.containers = group_all_spiders, main_scene, intro_scene
    SpiderRunAggressive.containers = group_all_spiders, main_scene
    Glass.containers = main_scene, intro_scene
    Cannon.containers = main_scene, intro_scene
    Fireball.containers = main_scene, intro_scene
    Explosion.containers = main_scene, intro_scene
    Blaze.containers = main_scene
    SpiderExplosion.containers = main_scene
    Score.containers = main_scene
    Digits.containers = main_scene
    Marks.containers = main_scene

    Player1.containers = intro_scene
    Player2.containers = intro_scene
    Player3.containers = intro_scene

    Fairy.containers = intro_scene
    Sparkle.containers = intro_scene, main_scene
    BoardText.containers = intro_scene, main_scene
    Scroll.containers = main_scene
    Joker.containers = main_scene

    win.blit(bg, (0, 0))

    pg.display.flip()

    pg.time.wait(200)
    chn1.play(snd_door)
    pg.time.wait(2000)

    # add boardText before player to make it behind
    board_text = BoardText((0, 333))
    board_text.set_board_image(core.TXT_CLEAR)

    if selection == 0:
        player = Player1()
        player_other_a = Player2()
        player_other_b = Player3()
    elif selection == 1:
        player = Player2()
        player_other_a = Player1()
        player_other_b = Player3()
    else:
        player = Player3()
        player_other_a = Player1()
        player_other_b = Player2()

    player.add(main_scene)

    player.walk_y = 580
    # 50% higher framerate for player1 because of worse photos
    player.walk_left(1900, 320, 4, 0.15 if selection == 0 else 0.1)

    player_other_a.walk_y = 600
    player_other_a.walk_left(2000, 320, 2.0, 0.1)

    player_other_b.walk_y = 650
    player_other_b.walk_left(2200, 320, 2.0, 0.1)

    spider_crawling_deco = None
    spider_crawling_deco2 = None
    spider_running_deco = None
    stage = 0
    fairy = None
    sparkle = None
    # board_text = None
    cannon = None
    glass = None

    quick = False  # True # for debug to skip part of long intro
    if quick:
        stage = 12
        sparkle = Sparkle()
        sparkle.path = Sparkle.path3

    # ------- intro scene -----

    while True:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                return False

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            # for quick skip the intro
            # debounce
            while keys[pg.K_ESCAPE]:
                for event in pg.event.get():
                    keys = pg.key.get_pressed()
            logging.info('Intro skipped.')
            break

        intro_scene.clear(win, bg)
        intro_scene.update()

        if player.walk_x < 1200 and stage < 1:
            chn1.play(snd_snake)
            stage = 1

        if player.walk_x < 1000 and spider_crawling_deco is None:
            chn2.play(snd_wicked_laugh)
            spider_crawling_deco = SpiderCrawlBig(1000)
            spider_crawling_deco.speed = 1
            stage = 2

        if spider_crawling_deco and spider_crawling_deco.rect.y > 280 and stage < 3:
            player_other_a.set_action(core.STOP)
            player_other_b.set_action(core.STOP)
            chn2.play(snd_scream)
            stage = 3

        if spider_crawling_deco and spider_crawling_deco.rect.y > 300 and stage < 4:
            player_other_a.walk_right(player_other_a.walk_x, 2000, 20, 1.0)
            player_other_b.walk_right(player_other_b.walk_x, 2000, 20, 1.0)
            player.set_action(core.LONG_PITY)
            stage = 4

        # transform crawling -> running
        if spider_crawling_deco and spider_crawling_deco.alive():
            if spider_crawling_deco.rect.y > 850:
                spider_crawling_deco.kill()
                # the web-line is drawn on win, so we must clean whole win
                win.blit(bg, (0, 0))
                spider_running_deco = SpiderRun(1000 - 50, 850)
                spider_running_deco.speed = 4
                spider_running_deco.walls = pg.Rect(400, 700, 1920 - 650, 1080)
                spider_running_deco.facing = -4
                if pg.mixer:
                    pg.mixer.music.fadeout(3000)
                stage = 5
            else:
                pg.draw.line(win, (255, 255, 255), (1000 + 60, 0), (1000 + 60, spider_crawling_deco.rect.y + 50))

        if spider_crawling_deco and spider_crawling_deco.alive() and spider_crawling_deco.rect.y > 600 and fairy is None:
            fairy = Fairy()
            fairy.walk_x = -200
            fairy.walk_y = 50
            fairy.fly_right(-200, 600, 5, 1)
            stage = 6

        if spider_running_deco and spider_running_deco.alive() and spider_running_deco.rect.x < 800 and \
                fairy and fairy.walk_x > 550 and fairy.action == core.WALK_RIGHT:
            fairy.action = core.ANXIOUS
            stage = 7

        if spider_running_deco and spider_running_deco.alive() and spider_running_deco.rect.x < 600 and \
                fairy and fairy.action == core.ANXIOUS:
            fairy.action = core.MAGIC
            chn1.play(snd_magic)
            sparkle = Sparkle()
            sparkle.interp = 4
            sparkle.path = Sparkle.path1
            stage = 8

        if stage == 8 and sparkle and not sparkle.alive() and spider_running_deco.alive():
            Explosion(spider_running_deco.rect.move(130, -45))
            chn2.play(snd_explosion)
            last_tick = pg.time.get_ticks()
            stage = 9

        now_tick = pg.time.get_ticks()

        if stage == 9 and now_tick - last_tick > 200:
            spider_running_deco.kill()
            stage = 10

        if stage == 10 and now_tick - last_tick > 2000:
            player.set_action(core.IDLE)
            fairy.walk_x = 600
            fairy.walk_y = 50
            fairy.fly_right(600, 900, 5, 1)
            stage = 11

        if stage == 11 and fairy.walk_x == 900:
            fairy.action = core.MAGIC
            chn1.play(snd_magic)
            sparkle = Sparkle()
            # sparkle.interp = 4
            sparkle.path = Sparkle.path2
            stage = 12

        if stage == 12 and not sparkle.alive():
            chn1.play(snd_magic)
            last_tick = pg.time.get_ticks()
            stage = 13

        if stage == 13 and now_tick - last_tick > 250:
            bg.blit(board, (0, 333))
            win.blit(bg, (0, 0))
            stage = 14

        if stage == 14 and quick:
            # =========== quick activation =============
            player.rect = (320, 422)
            player.speed = 0.1
            player.action = 0
            player_other_a.walk_x = 2000
            player_other_a.action = 0
            player_other_b.walk_x = 2000
            player_other_b.action = 0
            fairy = Fairy()
            fairy.action = 2
            fairy.speed = 1
            fairy.walk_speed_x = 5
            fairy.walk_x = 900
            fairy.walk_y = 50
            quick = False

        if stage == 14 and not quick and now_tick - last_tick > 2000:
            fairy.walk_x = 900
            fairy.walk_y = 30
            fairy.fly_left(900, 420, 5.0, 3.0, 1)
            #player.set_action(core.STOP)
            stage = 15

        if stage == 15 and fairy.walk_x <= 420:
            fairy.action = core.COOL
            # position corrections to match the fairy's hand with player's head
            corrections = [(-6, -3), (4, -3), (11, 25)]
            fairy.walk_x = 420 + corrections[selection][0]
            fairy.walk_y = 343 + corrections[selection][1]
            last_tick = pg.time.get_ticks()
            player.set_action(core.LOOK_RIGHT)
            stage = 16

        if stage == 16 and now_tick - last_tick > 2000:
            chn1.play(snd_magic)
            sparkle = Sparkle()
            sparkle.path = Sparkle.path3
            sparkle.interp = 20
            stage = 17

        if stage == 17 and now_tick - last_tick > 3000:
            board_text.set_board_image(core.TXT_ANGST)
            stage = 18

        if stage == 18 and now_tick - last_tick > 5000:
            chn1.play(snd_magic)
            sparkle = Sparkle()
            sparkle.path = Sparkle.path3
            sparkle.interp = 20
            stage = 19

        if stage == 19 and now_tick - last_tick > 6000:
            board_text.set_board_image(core.TXT_HELP)
            stage = 20

        if stage == 20 and now_tick - last_tick > 8000:
            fairy.walk_x = 420
            fairy.walk_y = 350
            fairy.fly_left_backwards(420, 800, 5, 1)
            player.set_action(core.IDLE)
            stage = 21

        if stage == 21 and fairy and fairy.walk_x >= 800:
            last_tick = pg.time.get_ticks()
            stage = 22

        if stage == 22 and now_tick - last_tick > 1000:
            chn1.play(snd_magic)
            sparkle = Sparkle()
            sparkle.path = Sparkle.path4
            sparkle.interp = 10
            stage = 23

        if stage == 23 and not sparkle.alive():
            glass = Glass()
            last_tick = pg.time.get_ticks()
            stage = 24

        if stage == 24 and now_tick - last_tick > 1000:
            chn1.play(snd_magic)
            sparkle = Sparkle()
            sparkle.path = Sparkle.path3
            sparkle.interp = 20
            stage = 25

        if stage == 25 and now_tick - last_tick > 2000:
            board_text.set_board_image(core.TXT_WAND)
            stage = 26

        if stage == 26 and now_tick - last_tick > 6000:
            chn1.play(snd_snake)
            spider_crawling_deco2 = SpiderCrawlBig(1000)
            spider_crawling_deco2.speed = 1
            stage = 27

        if stage >= 27 and spider_crawling_deco2 and spider_crawling_deco2.alive():
            if spider_crawling_deco2.rect.y > 50 and stage == 27:
                fairy.walk_x = 800
                fairy.walk_y = 350
                fairy.fly_left(800, 500, 5, -5, 1)
                stage = 28
            pg.draw.line(win, (255, 255, 255), (1000 + 60, 0), (1000 + 60, spider_crawling_deco2.rect.y + 50))

            if fairy.walk_x <= 500 and stage == 28:
                fairy.action = core.MAGIC
                chn1.play(snd_magic)
                sparkle = Sparkle()
                sparkle.path = Sparkle.path5
                stage = 29

            if stage == 29 and not sparkle.alive():
                #chn1.play(snd_magic)
                cannon = Cannon()
                cannon.rect.topleft = (1550, 788)
                last_tick = pg.time.get_ticks()
                stage = 30

            if stage == 30 and now_tick - last_tick > 2000:
                chn1.play(snd_magic)
                sparkle = Sparkle()
                sparkle.path = Sparkle.path3
                sparkle.interp = 20
                stage = 31

            if stage == 31 and now_tick - last_tick > 3000:
                board_text.set_board_image(core.TXT_CANNON)
                stage = 32

            if stage == 32 and now_tick - last_tick > 7000:
                sparkle = Sparkle()
                sparkle.path = Sparkle.path6
                sparkle.interp = 10
                stage = 33

            if stage == 33 and not sparkle.alive():
                chn2.play(snd_shot)
                # spider_crawling_deco2.speed = 1

                cannon.fire()
                fireball = Fireball(spider_crawling_deco2, 0)
                fireball.ty -= 270
                stage = 34

            # crawling is shot
            if stage == 34 and spider_crawling_deco2.killed:
                Explosion(spider_crawling_deco2.rect)
                chn2.play(snd_explosion)
                spider_crawling_deco2.kill()
                stage = 35

        if stage == 35:
            # the web-line is drawn on win, so we must clean whole win
            win.blit(bg, (0, 0))
            last_tick = pg.time.get_ticks()
            stage = 36

        if stage == 36 and now_tick - last_tick > 3000:
            chn1.play(snd_magic)
            sparkle = Sparkle()
            sparkle.path = Sparkle.path3
            sparkle.interp = 20
            stage = 37

        if stage == 37 and now_tick - last_tick > 4000:
            board_text.set_board_image(core.TXT_RELOAD)
            stage = 38

        if stage == 38 and now_tick - last_tick > 8000:
            cannon.disappear()
            stage = 39

        if stage == 39 and now_tick - last_tick > 10000:
            chn1.play(snd_magic)
            sparkle = Sparkle()
            sparkle.path = Sparkle.path3
            sparkle.interp = 20
            stage = 40

        if stage == 40 and now_tick - last_tick > 11000:
            board_text.set_board_image(core.TXT_TASKS)
            stage = 41

        if stage == 41 and now_tick - last_tick > 15000:
            chn1.play(snd_magic)
            sparkle = Sparkle()
            sparkle.path = Sparkle.path3
            sparkle.interp = 20
            stage = 42

        if stage == 42 and now_tick - last_tick > 16000:
            board_text.set_board_image(core.TXT_LUCK)
            stage = 43

        if stage == 43 and now_tick - last_tick > 18000:
            fairy.fly_right(500, 2200, 5, 1)
            stage = 44

        if stage == 44 and fairy.walk_x > 1950:
            chn1.play(snd_dundundun)
            last_tick = pg.time.get_ticks()
            stage = 45

        if stage == 45 and now_tick - last_tick > 3000:
            break

        # draw the scene
        dirty = intro_scene.draw(win)
        #pg.display.update(dirty)
        pg.display.flip()

        # cap the framerate
        clock.tick(40)

    ####################################################################

    pg.mixer.music.play(-1)  # music

    win.blit(bg, (0, 0))
    if stage < 14:
        bg.blit(board, (0, 333))
    pg.display.flip()

    board_text.set_board_image(core.TXT_CLEAR)

    # kill all unneeded sprites
    player.rect = (320, 420)
    player.set_action(core.IDLE)
    if spider_crawling_deco and spider_crawling_deco.alive():
        spider_crawling_deco.kill()
    if spider_running_deco and spider_running_deco.alive():
        spider_running_deco.kill()
    # if player_other_a:
    #     player_other_a.kill()
    # if player_other_b:
    #     player_other_b.kill()
    if fairy:
        fairy.kill()
    # if intro has been aborted create objects especially
    if glass is None:
        glass = Glass()
    if cannon is None:
        cannon = Cannon()

    youngest_spider_running = None
    youngest_attacker = None
    #sp_x = random.choice((1100, 1200, 1300, 1400, 1500))#(1100, 1200, 1450, 1700))
    #sp_y = 850
    fireball = None
    spider_crawling = None # SpiderCrawlBig(sp_x)
    #spider_crawling.speed = 2

    # whether the spider will attack in horizontal or vertical position
    hrz = False
    run = True

    channel = None
    table_index = 0
    snd_cycle = 0

    is_asking = False
    is_editing = False

    task_text = ''
    # changed = False
    wait_for_release = False
    delayed_task = False
    delayed_new_round = False
    make_throw_trick = False

    counter_correct = 0 # length of correct answer's sequence
    score_value = 0
    score = Score()
    main_scene.add(score)
    digits = None
    marks = None
    marks2 = None
    correction = None
    sparkle = None
    one_attacker = None
    joker = None

    scroll = Scroll(icon)

    ma = 1  # multipliers
    mb = 1
    mm = 0  # task method:  0 = ask, 1 = written, 2 = matrix

    chn0.set_volume(0.99)
    game_over = False
    pg.key.set_repeat()
    pg.event.post(pg.event.Event(NEW_ROUND))

    stage_throwing = 0
    pool_task = False

    while table_index < len(table):

        now_tick = pg.time.get_ticks()

        if game_over and player.action != core.LONG_PITY:
            player.set_action(core.LONG_PITY)

        for event in pg.event.get():

            # ----- start event loop ---------------
            if event.type == pg.QUIT:
                pg.quit()
                return False

            if (event.type == NEW_ROUND or event.type == NEW_POOL_TASK) and not game_over:
                if event.type == NEW_POOL_TASK:
                    (ma, mb, mm) = pool.pop(0)
                    pool_task = True
                    chn2.play(snd_joker)
                    logging.info('Task from pool: ' + str(ma) + ' * ' + str(mb) + '. Method ' + ['Ask', 'Write', 'Matrix'][mm])
                else:
                    (ma, mb, mm) = table[table_index]
                    pool_task = False

                mmstr = ['Ask', 'Write', 'Matrix'][mm]
                print(table[table_index])
                difficulty = max(ma, mb)
                penalty = 0

                if digits and digits.alive():
                    digits.kill()
                if marks and marks.alive():
                    marks.kill()
                if marks2 and marks2.alive():
                    marks2.kill()
                if correction and correction.alive():
                    correction.kill()

                last_tick = pg.time.get_ticks()
                delay = 1000

                if mm == core.ASK:
                    board_text.set_board_image(core.TXT_LISTEN)
                    if pool_task:
                        delay = 2200  # 'cause Joker laughs somethat too long
                    delayed_task = True
                elif mm == core.WRITE:
                    chn0.play(snd_knocking)
                    delayed_task = True
                    # changed = False
                else:
                    board_text.set_board_image(core.TXT_COUNT)
                    delay = 2000  # 2 seconds to read the text "Count small spiders"
                    delayed_task = True

            if is_asking and event.type == SOUND_END and \
                    (spider_crawling and spider_crawling.alive() or joker and joker.alive()):
                if snd_cycle == 0:
                    is_editing = False
                    pg.mixer.music.set_volume(0.2)  # mute music
                    chn1.set_volume(0.2)  # mute knocking sounds
                    chn0.play(snd_numbers[ma])
                    snd_cycle += 1
                elif snd_cycle == 1:
                    chn0.play(snd_mal)
                    snd_cycle += 1
                elif snd_cycle == 2:
                    chn0.play(snd_numbers[mb])
                    snd_cycle += 1
                    if penalty == 0:  # if repeat, do not appear again
                        cannon.appear()
                    player.set_action(core.THINKING)
                else:
                    board_text.set_board_image(core.TXT_CLEAR)
                    if not pool_task:
                        spider_crawling.speed = level  # after dictation speed up climbing (1 or 2)
                    snd_cycle = 0
                    pg.mixer.music.set_volume(0.99)  # unmute
                    chn1.set_volume(0.99)
                    last_tick = pg.time.get_ticks()
                    is_asking = False
                    is_editing = True

            if is_editing:
                if event.type == pg.KEYDOWN and not wait_for_release:
                    if event.key == pg.K_0:
                        enter += '0'
                        changed = True
                    elif event.key == pg.K_1:
                        enter += '1'
                        changed = True
                    elif event.key == pg.K_2:
                        enter += '2'
                        changed = True
                    elif event.key == pg.K_3:
                        enter += '3'
                        changed = True
                    elif event.key == pg.K_4:
                        enter += '4'
                        changed = True
                    elif event.key == pg.K_5:
                        enter += '5'
                        changed = True
                    elif event.key == pg.K_6:
                        enter += '6'
                        changed = True
                    elif event.key == pg.K_7:
                        enter += '7'
                        changed = True
                    elif event.key == pg.K_8:
                        enter += '8'
                        changed = True
                    elif event.key == pg.K_9:
                        enter += '9'
                        changed = True
                    elif event.key == pg.K_BACKSPACE:
                        enter = enter[:-1]
                        changed = True
                    elif event.key == pg.K_RETURN:
                        changed = False
                        wait_for_release = True
                    elif event.key == pg.K_SPACE:
                        changed = False
                        wait_for_release = True
                    else:
                        changed = False

                    if changed:
                        # do not allow more than two symbols in answer
                        if len(enter) > 2:
                            enter = enter[:2]
                        else:
                            digits.set_text(task_text + enter)
                        wait_for_release = True

                elif wait_for_release and event.type == KEYUP:
                    wait_for_release = False
                    if len(enter) > 0 and event.key == pg.K_RETURN:
                        is_editing = False
                        if int(enter) == ma * mb:
                            precision = 0
                        elif int(enter) > ma * mb:
                            precision = 1
                        else:
                            precision = 2

                        chn2.play(snd_shot)
                        cannon.fire()
                        if pool_task:
                            fireball = Fireball(joker, precision)
                        else:
                            fireball = Fireball(spider_crawling, precision)
                        if precision:
                            pool.append(table[table_index])
                            logging.info('Incorrect ' + str(ma) + ' * ' + str(mb) + '. Answered ' + enter + '. Method ' + mmstr)

                    if len(enter) == 0 and event.key == pg.K_SPACE and mm == core.ASK:
                        # please repeat!
                        is_asking = True
                        pg.event.post(pg.event.Event(SOUND_END))
                        penalty = 2
                        logging.info('Repeat used for ' + str(ma) + ' * ' + str(mb))

        # ----- end of event loop ---------------

        if delayed_task and now_tick - last_tick > delay and not game_over:
            if pool_task:
                joker = Joker()
                joker.rect.topleft = (950, -50)
            else:
                sp_x = random.choice((900, 950, 1000, 1050, 1100, 1150))#, 1700))
                sp_y = 850 + len(group_running_spiders)
                spider_crawling = SpiderCrawlBig(sp_x)

            if mm == core.ASK:
                is_asking = True
                # hack: new crawling spider is descending, simulate sound event
                pg.event.post(pg.event.Event(SOUND_END))
                digits = Digits((262, 307))
                task_text = ''
                digits.set_text(task_text)
                enter = ''
                is_editing = True
                # changed = False
            elif mm == core.WRITE:
                cannon.appear()
                player.set_action(core.THINKING)
                digits = Digits((60, 440))
                task_text = str(ma) + '*' + str(mb) + '='
                digits.set_text(task_text)
                enter = ''
                is_editing = True
            else:
                board_text.set_board_image(core.TXT_CLEAR)
                cannon.appear()
                scroll.set_matrix(ma, mb)
                scroll.appear()
                player.set_action(core.THINKING)
                digits = Digits((262, 307))
                task_text = ''
                digits.set_text(task_text)
                enter = ''
                is_editing = True

            delayed_task = False

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE] and not game_over:
            # pause or exit
            # debounce
            while keys[pg.K_ESCAPE]:
                for event in pg.event.get():
                    keys = pg.key.get_pressed()

            blackout = pg.Surface((1920, 1080))
            blackout.fill((0, 0, 0))
            for alpha in range(0, 30):
                blackout.set_alpha(alpha)
                win.blit(blackout, (0, 0))
                pg.display.update()
                #pg.time.delay(1)

            font_pause = pg.font.SysFont("comicsansms", 72)
            text_pause = font_pause.render("Pause", 1, Color('white'))
            font_hint = pg.font.SysFont("arial", 24)
            text_hint = font_hint.render('<Esc> Continue, <q> Quit', 1, Color('white'))

            win.blit(text_pause, (400, 50))
            win.blit(text_hint, (1600, 1050))
            pg.display.flip()
            logging.info('Game paused.')

            while True:
                for event in pg.event.get():
                    keys = pg.key.get_pressed()

                if keys[pg.K_q] or event.type == pg.QUIT:
                    logging.info('Exit from pause.')
                    return False

                if keys[pg.K_ESCAPE]:
                    while keys[pg.K_ESCAPE]:
                        for event in pg.event.get():
                            keys = pg.key.get_pressed()

                    # clear/erase the last drawn sprites
                    win.blit(bg, (0, 0))
                    pg.display.flip()

                    break

        # clear/erase the last drawn sprites
        main_scene.clear(win, bg)

        #update all the sprites
        main_scene.update()

        # transform crawling -> running
        if spider_crawling and spider_crawling.alive():
            if player.action != core.PITY and fireball and fireball.alive() and fireball.precision != 0 and fireball.deg < -10:
                counter_correct = 0
                player.set_action(core.PITY)
                spider_crawling.speed = 2  # after missed shop increase speed
                sh = -15 if len(enter) < 2 else 0
                marks = Marks((260 + sh, 437 - sh))
                marks.strikeout()
                if mm == core.WRITE:
                    correction = Digits((310, 390))
                    correction.set_text(str(ma * mb))
                else:
                    correction = Digits((120, 520))
                    correction.set_text(str(ma) + '*' + str(mb) + '=' + str(ma * mb))

            # crawling is shot
            if spider_crawling.killed:
                counter_correct += 1
                # various deaths, depending on difficulty
                if difficulty <= 5:
                    SpiderExplosion(spider_crawling.rect)
                    chn2.play(snd_explosion)
                    score_value += 2 - penalty
                elif difficulty <= 7:
                    Blaze(spider_crawling.rect)
                    chn2.play(snd_burning)
                    score_value += 4 - penalty
                else:
                    Explosion(spider_crawling.rect)
                    chn2.play(snd_explosion)
                    score_value += 6 - penalty
                spider_crawling.kill()
                cannon.disappear()
                if mm == core.MATRIX:
                    scroll.disappear()
                player.set_action(core.EXCITEMENT)
                score.set_score(score_value)
                marks2 = Marks((220, 570))
                marks2.check_mark()

                # the web-line is drawn on win, so we must clean whole win
                win.blit(bg, (0, 0))
                pg.display.flip()
                delayed_new_round = True
                last_tick = pg.time.get_ticks()
            elif spider_crawling.rect.y > sp_y:
                counter_correct = 0
                spider_crawling.kill()
                cannon.disappear()
                if mm == core.MATRIX:
                    scroll.disappear()
                # the web-line is drawn on win, so we must clean whole win
                win.blit(bg, (0, 0))
                pg.display.flip()
                youngest_spider_running = SpiderRun(sp_x - 50, sp_y)
                # player made no answer, make a correction
                if correction and not correction.alive():
                    is_editing = False
                    correction = Digits((120, 520))
                    correction.set_text(str(ma) + '*' + str(mb) + '=' + str(ma * mb))
                    pool.append(table[table_index])
                    logging.info('No answer ' + str(ma) + ' * ' + str(mb) + '. Method ' + mmstr)
                delayed_new_round = True
                last_tick = pg.time.get_ticks()
            else:
                pg.draw.line(win, (255, 255, 255), (sp_x + 60, 0), (sp_x + 60, spider_crawling.rect.y + 50))

        # joker
        if joker and joker.alive():
            if player.action != core.PITY and fireball and fireball.alive() and fireball.precision != 0 and fireball.deg < -10:
                player.set_action(core.PITY)
                sh = -15 if len(enter) < 2 else 0
                marks = Marks((260 + sh, 437 - sh))
                marks.strikeout()
                if mm == core.WRITE:
                    correction = Digits((310, 390))
                    correction.set_text(str(ma * mb))
                else:
                    correction = Digits((120, 520))
                    correction.set_text(str(ma) + '*' + str(mb) + '=' + str(ma * mb))

            # joker is shot
            if joker.killed:
                Explosion(joker.rect.move(100, 60))
                Explosion(joker.rect.move(150, 50))
                Explosion(joker.rect.move(200, 60))
                chn2.play(snd_explosion)
                joker.kill()
                cannon.disappear()
                if mm == core.MATRIX:
                    scroll.disappear()
                player.set_action(core.EXCITEMENT)
                marks2 = Marks((220, 570))
                marks2.check_mark()
                last_tick = pg.time.get_ticks()
                make_throw_trick = True
            elif joker.rect.y > 850:
                joker.kill()
                cannon.disappear()
                if mm == core.MATRIX:
                    scroll.disappear()
                # player made no answer, make a correction
                if correction and not correction.alive():
                    correction = Digits((120, 520))
                    correction.set_text(str(ma) + '*' + str(mb) + '=' + str(ma * mb))
                    pool.append(table[table_index])
                    logging.info('No answer for pool task ' + str(ma) + ' * ' + str(mb) + '. Method ' + mmstr)
                    is_editing = False
                delayed_new_round = True
                last_tick = pg.time.get_ticks()

        if delayed_new_round and now_tick - last_tick > 2000:
            delayed_new_round = False

            # check the pool
            if len(group_attacking_spiders) > 0 and counter_correct >= 2 and len(pool) > 0:
                counter_correct = 0
                pg.event.post(pg.event.Event(NEW_POOL_TASK))
            else:
                table_index += 1
                pg.event.post(pg.event.Event(NEW_ROUND))

        if make_throw_trick:
            # the helper waits till at most one running spider exist and its on safe distance and is going away;
            # or now active running spider exists
            if stage_throwing == 0:
                last_tick = pg.time.get_ticks()
                stage_throwing = 1

            if stage_throwing == 1 and now_tick - last_tick > 1000:
                stage_throwing = 2

            if stage_throwing == 2 and \
                    ((len(group_running_spiders) == 1 and youngest_spider_running.facing < 0 and youngest_spider_running.rect.x < 1800) \
                    or len(group_running_spiders) == 0):
                stage_throwing = 3

            if stage_throwing == 3:
                if random.choice((0, 1)) == 0:
                    helper = player_other_a
                else:
                    helper = player_other_b

                if not main_scene.has(helper):
                    # print("added " + helper.__repr__())
                    helper.add(main_scene)
                helper.walk_x = 2000
                last_tick = pg.time.get_ticks()
                stage_throwing = 4

            if stage_throwing == 4 and now_tick - last_tick > 500:
                helper.walk_y = 600
                helper.walk_left(2000, 1400, 15.0, 0.5)
                stage_throwing = 5

            if stage_throwing == 5 and helper.walk_x <= 1400:
                helper.set_action(core.THROW)
                last_tick = pg.time.get_ticks()
                stage_throwing = 6

            if stage_throwing == 6 and now_tick - last_tick > 1500:
                sparkle = Sparkle()
                sparkle.interp = 4
                sparkle.path = Sparkle.path7
                stage_throwing = 7

            if stage_throwing == 7 and sparkle and not sparkle.alive():
                one_attacker = group_attacking_spiders.sprites()[0]
                if one_attacker.start_sprite == 0:  # horizontal
                    Explosion(one_attacker.rect.move(130, -45))
                else:
                    Explosion(one_attacker.rect.move(-20, 100))
                chn2.play(snd_explosion)
                last_tick = pg.time.get_ticks()
                stage_throwing = 8

            if stage_throwing == 8 and now_tick - last_tick > 200:
                one_attacker.kill()
                stage_throwing = 9

            if stage_throwing == 9 and now_tick - last_tick > 1000:
                helper.set_action(core.EXCITEMENT)
                stage_throwing = 10

            if stage_throwing == 10 and now_tick - last_tick > 1600:
                helper.walk_right(helper.walk_x, 2000, 15, 0.5)
                stage_throwing = 0
                make_throw_trick = False
                delayed_new_round = True
                last_tick = pg.time.get_ticks()

        if len(group_running_spiders) > 0:
            oldest_running_spider = group_running_spiders.sprites()[0]
        else:
            oldest_running_spider = None

        if oldest_running_spider and oldest_running_spider.waiting and oldest_running_spider.age > 2:
            # or glass.stage == 4):
            # if glass is nearly to break, mercy convert running to attacking immediately
            # todo condition is wrong; does not work
            rect = oldest_running_spider.rect
            oldest_running_spider.kill()
            # horizontally and vertically attacking spiders are placed a little bit different
            if hrz:
                youngest_attacker = SpiderAttack(rect.x, rect.y, start_sprite=0)
                hrz = False  # the next attacking spider must be horizontal
            else:
                youngest_attacker = SpiderAttack(rect.x + 180, rect.y - 180 + len(group_attacking_spiders) * 4, start_sprite=16)
                hrz = True
            if glass.alive():
                chn1.play(snd_bang, loops=max(len(group_attacking_spiders), 3))

        if youngest_attacker and youngest_attacker.frame > 100:
            # after some delay increment the glass stage
            glass.stage = max(glass.stage, len(group_attacking_spiders))
            glass.stage = min(glass.stage, 4)
            if glass.alive() and glass.stage == 4 and len(group_attacking_spiders) == 5:
                chn1.stop()
                chn1.play(snd_break)
                glass.kill_later()

        if not glass.alive() and not game_over:
            # now all spiders run to the victim
            game_over = True
            logging.info('Player ' + players[selection].get('name', '?') + ' lost.')
            idx = 0
            for attacker in group_attacking_spiders:
                r = attacker.rect
                attacker.kill()
                aggressive = SpiderRunAggressive(644 + idx * 2, 860 + idx * 10, idx, random.choice((0,1,2,3,4,5,6,7)))
                aggressive.set_action(core.WALK_LEFT, 290 + idx * 4, 860 + idx * 10, 10, 0)
                idx += 1
                last_tick = pg.time.get_ticks()

        if game_over and now_tick - last_tick > 1600:
            break

        # draw the scene
        dirty = main_scene.draw(win)
        pg.display.update(dirty)

        # cap the framerate
        clock.tick(40)

    time_end_game = datetime.datetime.now()
    seconds = (time_end_game - time_start_game).seconds
    logging.info('Collected score ' + str(score_value))
    logging.info(players[selection].get('name', '?') + ' played ' + str(int(seconds / 60)) + ' minutes.')
    players[selection]['high_score'] = max(players[selection]['high_score'], score_value)
    players[selection]['total'] += score_value
    save_players_data(players)

    if not game_over and table_index >= len(table) - 1:
        players[selection]['awards'] += 1
        logging.info('Player ' + players[selection].get('name', '?') + ' has won.')
        stage_win = 0
        sparkle1 = None
        sparkle2 = None
        sparkle3 = None
        sparkle4 = None
        sparkle5 = None
        sparkle6 = None

        while True:
            for event in pg.event.get():
                keys = pg.key.get_pressed()

            now_tick = pg.time.get_ticks()

            if event.type == pg.QUIT:
                return False

            main_scene.clear(win, bg)
            main_scene.update()

            if stage_win == 0:
                if pg.mixer:
                    pg.mixer.music.fadeout(500)
                chn0.play(snd_thunder)
                last_tick = pg.time.get_ticks()
                stage_win = 1

            if stage_win == 1 and sparkle1 is None and now_tick - last_tick > 2000:
                chn1.play(snd_fireball)
                sparkle1 = Sparkle()
                sparkle1.interp = 4
                sparkle1.path = Sparkle.path8

            if stage_win == 1 and sparkle2 is None and now_tick - last_tick > 2500:
                chn2.play(snd_fireball)
                sparkle2 = Sparkle()
                sparkle2.interp = 4
                sparkle2.path = Sparkle.path9

            if stage_win == 1 and sparkle3 is None and now_tick - last_tick > 2800:
                chn0.play(snd_fireball)
                sparkle3 = Sparkle()
                sparkle3.interp = 10
                sparkle3.path = Sparkle.path10

            if stage_win == 1 and sparkle4 is None and now_tick - last_tick > 3000:
                chn1.play(snd_fireball)
                sparkle4 = Sparkle()
                sparkle4.interp = 10
                sparkle4.path = Sparkle.path11

            if stage_win == 1 and sparkle5 is None and now_tick - last_tick > 3200:
                chn2.play(snd_fireball)
                sparkle5 = Sparkle()
                sparkle5.interp = 4
                sparkle5.path = Sparkle.path9

            if stage_win == 1 and sparkle6 is None and now_tick - last_tick > 3500:
                chn0.play(snd_fireball)
                sparkle6 = Sparkle()
                sparkle6.interp = 4
                sparkle6.path = Sparkle.path8

            if stage_win == 1 and sparkle1 and not sparkle1.alive():
                for sprite in group_all_spiders.sprites():
                    sprite.kill()

            if stage_win == 1 and sparkle3 and not sparkle3.alive():
                board_text.kill()
                if digits and digits.alive():
                    digits.kill()
                if marks and marks.alive():
                    marks.kill()
                if marks2 and marks2.alive():
                    marks2.kill()
                if correction and correction.alive():
                    correction.kill()

            if stage_win == 1 and sparkle5 and not sparkle5.alive():
                glass.kill()
                last_tick = pg.time.get_ticks()
                stage_win = 2

            if stage_win == 2 and now_tick - last_tick > 1000:
                chn0.play(snd_thunder)
                last_tick = pg.time.get_ticks()
                stage_win = 3

            if stage_win == 3 and now_tick - last_tick > 2500:
                win.blit(bg3, (0, 0))
                bg.blit(bg3, (0, 0))  # strange workaround. Need better solution
                pg.display.flip()

                music_monsters = os.path.join(main_dir, 'data', 'happy_dreams.mp3')
                if pg.mixer:
                    pg.mixer.music.load(music_monsters)
                    pg.mixer.music.play(-1)
                stage_win = 4

            if stage_win == 4 and now_tick - last_tick > 3000:
                if not main_scene.has(player_other_a):
                    player_other_a.add(main_scene)
                if not main_scene.has(player_other_b):
                    player_other_b.add(main_scene)

                player_other_a.walk_x = 2000
                player_other_b.walk_x = 2000
                player_other_a.walk_y = 600
                player_other_b.walk_y = 600
                player_other_a.walk_left(2000, 500, 15.0, 0.5)
                player_other_b.walk_left(2200, 700, 15.0, 0.5)
                stage_win = 5

            if stage_win == 5 and player_other_a.walk_x <= 500:
                last_tick = pg.time.get_ticks()
                stage_win = 6

            if stage_win == 6 and now_tick - last_tick > 1000:
                player.set_action(core.EXCITEMENT)
                player_other_a.set_action(core.EXCITEMENT)
                player_other_b.set_action(core.EXCITEMENT)
                stage_win = 7

            if stage_win == 7:
                if int(player.frame * player.speed) >= player.jump_idx:
                     player.action = core.STOP
                if int(player_other_a.frame * player_other_a.speed) >= player_other_a.jump_idx:
                    player_other_a.action = core.STOP
                if int(player_other_b.frame * player_other_b.speed) >= player_other_b.jump_idx:
                    player_other_b.action = core.STOP
                    last_tick = pg.time.get_ticks()
                    stage_win = 8

            if stage_win == 8:
                chn1.play(snd_shutter)
                last_tick = pg.time.get_ticks()
                stage_win = 9

            if stage_win == 9 and now_tick - last_tick > 3000:
                player.action = core.EXCITEMENT
                player_other_a.action = core.EXCITEMENT
                player_other_b.action = core.EXCITEMENT
                stage_win = 10

            if stage_win == 10 and now_tick - last_tick > 5000:
                player.walk_x = 320
                player_other_a.walk_x = 500
                player_other_b.walk_x = 700
                player.walk_y = 450
                player_other_a.walk_y = 450
                player_other_b.walk_y = 450
                player.walk_right(player.walk_x, 2000, 15, 1.0)
                player_other_a.walk_right(player_other_a.walk_x, 2000, 15, 1.0)
                player_other_b.walk_right(player_other_b.walk_x, 2000, 15, 1.0)
                player.walk_speed_y = 1.0
                player_other_a.walk_speed_y = 1.0
                player_other_b.walk_speed_y = 1.0
                stage_win = 11

            if stage_win == 11 and player.walk_x >= 2000:
                if keys[pg.K_ESCAPE]:
                    return True

            # draw the scene
            dirty = main_scene.draw(win)
            pg.display.flip()

            # cap the framerate
            clock.tick(40)


    if game_over:
        if pg.mixer:
            pg.mixer.music.load(music_chase)
            pg.mixer.music.play(-1)
        blackout = pg.Surface((1920, 1080))
        blackout.fill((0, 0, 0))
        for alpha in range(0, 100):
            blackout.set_alpha(alpha)
            win.blit(blackout, (0, 0))
            pg.display.update()
            pg.time.delay(5)

        win.blit(brick, (0, 0))
        pg.display.flip()

        font_score = pg.font.SysFont("comicsansms", 36)
        font_hint = pg.font.SysFont("arial", 24)
        text_hint = font_hint.render('<Esc> Exit, <n> New game', 1, Color('white'))
        text_score = font_score.render("Score " + str(score_value), 1, Color('white'))

        spider_deco = SpiderRunDeco(300, 780)
        spider_deco.set_position(1920 / 2 - 90)
        spider_deco.limit = 700

        while True:
            for event in pg.event.get():
                keys = pg.key.get_pressed()

            if keys[pg.K_ESCAPE] or event.type == pg.QUIT:
                return False

            if keys[pg.K_n]:
                return True

            game_over_scene.clear(win, brick)
            game_over_scene.update()

            win.blit(game_over_txt, (420, 380))
            win.blit(text_score, (20, 950))
            win.blit(text_hint, (1600, 1050))

            # draw the scene
            dirty = game_over_scene.draw(win)
            pg.display.flip()

            # cap the framerate
            clock.tick(40)

    if pg.mixer:
        pg.mixer.music.fadeout(1000)
    pg.time.wait(1000)
    pg.quit()


if __name__ == '__main__': main()
