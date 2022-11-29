import pygame as pg
from random import randint
from math import cos, sin

class Sky:
    def __init__(self, height_sky, screen_size, world_size=1000, distance_to_viewing_plane=200):
        self.height_sky = height_sky
        self.world_size = world_size
        self.screen_size = screen_size
        self.distance_to_viewing_plane = distance_to_viewing_plane

        self.fraction_generator(self.height_sky)

    def render_sky(self, screen):
        screen.fill((221,238,255)) # заглушка

    def render_fraction(self, screen):
        for id_fraction in range(len(self.fraction_positions)):
            fraction_xyz = self.fraction_positions[id_fraction]
            v = 100 * (1 - (fraction_xyz[2] / self.world_size))
            v = 100 if v > 100 else v
            v = 0 if v < 0 else v
            color = pg.color.Color(0,0,0)
            color.hsva = self.b_color_f_H, self.b_color_f_S, v, self.b_color_f_A

            fraction_screen_x, fraction_screen_y = self.to_center(*self.perspective_transform(*fraction_xyz))
            pg.draw.circle(screen, color, (int(fraction_screen_x), int(fraction_screen_y)), 2)
            old_fraction_screen_x, old_fraction_screen_y = self.to_center(*self.perspective_transform(*self.old_fraction_positions[id_fraction]))

            if 1000 > abs(self.old_fraction_positions[id_fraction][2] - self.fraction_positions[id_fraction][2]) > 10:
                pg.draw.line(screen, color, (old_fraction_screen_x, old_fraction_screen_y),
                             (fraction_screen_x, fraction_screen_y), 2)

    def render(self, screen):
        self.render_sky(screen)
        self.render_fraction(screen)
        
        #debug_text = pg.font.Font(None, 22).render(f'speed: {self.speed}, angle: {self.angle}', 1, (255, 255, 255))
        #screen.blit(debug_text, (5, 5))

    def update(self, speed, angle):
        #speed = #((self.screen_size[1] // 2) - speed) // 20 
        #angle = #((self.screen_size[0] // 2) - angle) / 10000

        for i in range(len(self.fraction_positions)):
            self.old_fraction_positions[i] = self.fraction_positions[i]
            x, y, z = self.fraction_positions[i]
            x, y = self.rotation(x, y, angle)
            z -= speed

            if z < 1:
                z = self.world_size
            elif z > self.world_size:
                z = 1
            
            self.fraction_positions[i] = x, y, z
    
        return speed, angle

    def fraction_generator(self, height):
        self.fraction_positions = []
        self.old_fraction_positions = []
        if 0 <= height <= 1000:
            self.base_color_fraction = pg.color.Color(150,75,0)
            
            self.b_color_f_H, self.b_color_f_S, self.b_color_f_V, self.b_color_f_A = self.base_color_fraction.hsva
            
            for fraction in range(10):
                x,y,z = (randint(-self.world_size, self.world_size),
                         randint(-self.world_size, self.world_size),
                         randint(1, self.world_size))
                self.fraction_positions.append((x,y,z))
                self.old_fraction_positions.append((x,y,z))

    def to_center(self, x, y):
        return x + self.screen_size[0] // 2, y + self.screen_size[1] // 2

    def perspective_transform(self, x, y, z):
        x_plane = 0 if z * x == 0 else self.distance_to_viewing_plane / z * x
        y_plane = 0 if z * y == 0 else self.distance_to_viewing_plane / z * y
        return x_plane, y_plane

    def rotation(self, x, y, angle):
        return x * cos(angle) - y * sin(angle), x * sin(angle) + y * cos(angle)
