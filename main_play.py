import pygame as pg
from sky import Sky


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.FPS = 50
        self.size = self.width, self.height = 800, 600
        self.main_screen = pg.display.set_mode(self.size)
        self.sky = Sky(1000, self.size, world_size=10000)
        self.running = True
        
        self.speed = 1
        self.angle = 0.00
        self.speed_up = self.speed_down = False
        
    def run(self):
        while self.running:
            self.event_process(pg.event.get())
            self.render(self.main_screen)
            pg.display.flip()
            self.clock.tick(self.FPS)
        pg.quit()
        
    def event_process(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.speed_up = True
                elif event.key == pg.K_DOWN:
                    self.speed_down = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.speed_up = False
                elif event.key == pg.K_DOWN:
                    self.speed_down = False
        if self.speed_up:
            self.speed += 10
        if self.speed_down:
            self.speed -= 10


    def render(self, screen):
        self.sky.render(screen)
        self.speed, self.angle = self.sky.update(self.speed, self.angle)

if __name__ == '__main__':
    app = Game()
    app.run()