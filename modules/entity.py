
import pygame as pg
from pygame import mixer

class Entity:
    def __init__(self, scr, name, ent_type, cg, pos, icons, v_speed, h_speed, player_cg=(), sound_list=[], life_span=999999):
        self.screen = scr
        self.name = name
        self.type = ent_type
        self.cg = cg    # collision geometry dimension wxh
        self.pos = pos.copy()
        self.init_pos = pos.copy()
        self.current_speed_h = h_speed
        self.current_speed_v = v_speed
        self.base_speed_h = h_speed
        self.base_speed_v = v_speed
        self.player_cg = player_cg
        self.screen_height = scr.get_height()
        self.alive = True
        self.state = 'ready'
        self.icon_list = icons
        self.life_span =life_span
        self.travel_total = 0
        self.travel_per_event = 0

        # sound stuff
        self.sound_list = sound_list
        self.sound_played = False
        if len(sound_list) > 0:
            self.sound = mixer.Sound(sound_list[0])

        self.icons = []
        for i in range(len(icons)):
            self.icons.append(pg.image.load(icons[i]))   

    def update(self, keys, events=[]):
        # handle speed
        if keys[pg.K_UP]:
            self.speed_up()
        elif keys[pg.K_DOWN]:
            self.slow_down()
        else:
            self.current_speed_v = self.base_speed_v
        
        self.pos[1] += self.current_speed_v

        # play the explosion sound 
        if not self.sound_played:
            pg.mixer.Channel(1).play(self.sound)
            # self.sound.play()
            self.sound_played = True

        self.update_odometer()

        # draw on screen
        self.screen.blit(self.icons[0], self.pos) 

    def speed_up(self):
        self.current_speed_v = self.base_speed_v * 2.0

    def slow_down(self):
        self.current_speed_v = self.base_speed_v / 2.0
        
    def set_walls(self, walls):
        self.walls = walls

    def set_barrier(self):
        pass

    def update_odometer(self):
        self.travel_total += self.current_speed_v

    def is_active(self):
        if self.type == 'explosion':
            if self.travel_per_event > self.life_span:
                self.alive = False
                self.travel_per_event = 0
            else:
                self.travel_per_event += self.current_speed_v

        if self.pos[1] > self.screen_height or not self.alive:
            return False
        else:
            return True
               
    def sign(self, num):
        if num > 0:
            return 1
        elif num < 0:
            return -1 
        else:
            return 0