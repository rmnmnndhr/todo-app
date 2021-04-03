import pygame
import random, sys
from settings import *
from particle import *
from extra import *

class Add_screen:
    def __init__(self, super):
        self.isOpen = True
        self.text = ''
        self.super = super
        self.db = super.db
        self.clock = pygame.time.Clock()
        self.cancelRect = pygame.Rect(960,90,120,50)
        self.addRect = pygame.Rect(870,90,77,50)
        self.typingSurface = pygame.Surface((880, 450))
        self.typingSurface.fill(MAIN)
        self.typingRect = pygame.Rect(0, 0, 880, 100)
        self.offset = 0

    def run(self):
        while self.isOpen:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()


    def events(self):
        pygame.key.set_repeat(700, 50)


        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.add()

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) <= 50:
                        self.text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.cancelRect.collidepoint(pygame.mouse.get_pos()):
                        self.isOpen = False
                    elif self.addRect.collidepoint(pygame.mouse.get_pos()):
                        self.add()



    def add(self):
        if self.text:
            self.db.append(self.text)
            save(self.db)
            self.super.notupdated = True
        self.isOpen = False

    def update(self):

        self.super.screen.fill(BACKGROUND)

        for particle in self.super.particles:
            if particle.pos[1] > HEIGHT:
                particle.pos = (random.randrange(0, WIDTH), random.randrange(-100, -10))
                particle.speed = random.randrange(200, 500)
            particle.update(self.dt)
            particle.draw(self.super.screen)


        pygame.draw.rect(self.super.screen, MAIN, self.super.mainSurface, border_radius = 40)



        pygame.draw.rect(self.super.screen, (200,69,80), self.cancelRect, border_radius = 10)
        text('Cancel', self.super.screen, WHITE, 32, 965, 100)
        pygame.draw.rect(self.super.screen, ADD_COLOR, self.addRect, border_radius = 10)
        text('Add', self.super.screen, MAIN_FONT, 32, 880, 100)


        self.super.screen.blit(self.typingSurface, (200,150))

        pygame.draw.rect(self.typingSurface, WHITE, self.typingRect , border_radius = 40)
        x,y = text(str(self.text), self.typingSurface, MAIN_FONT, 32, 30 - self.offset , 30)

        if x > 800:
            self.offset = x - 800

        pygame.display.flip()



# Game loop
class Main:
    def __init__(self):
        pygame.init() #initialize pygame
        pygame.mixer.init() #initialize pygame sound
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.offset = 0
        self.doneContainer = []

    def new(self):
        self.run()

    def run(self):
        # game loop
        self.playing = True
        self.particles = []
        self.mainSurface = pygame.Rect(180, 80, 920, 560)
        self.addRect = pygame.Rect(990, 90, 80, 50)
        self.todoSurface = pygame.Surface((880, 450))
        self.todoSurface.fill(MAIN)
        self.text = ''
        self.db = load()
        self.notupdated = True

        # spawning particles
        for i in range(20):
            self.particles.append(Particle())

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000

            self.events()
            self.update()

    def events(self):
        # game loop - events
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.notupdated = True
                    self.offset += 30
                    if self.offset >= 0:
                        self.offset = 0
                elif event.button == 5:
                    self.notupdated = True
                    if -(self.offset) <=  (100 * len(self.db) - 450):
                        self.offset -= 30

                elif event.button == 1:
                    if self.addRect.collidepoint(pygame.mouse.get_pos()):
                        screen = Add_screen(self)
                        screen.run()
                        self.db = load()

                    else:
                        for i in self.doneContainer:
                            x, y = pygame.mouse.get_pos()
                            if x > 200 and y > 150 and x < 1080 and y < 600:
                                if i.collidepoint((x - 200, y - 150)):
                                    self.db.pop(self.doneContainer.index(i))
                                    save(self.db)
                                    self.notupdated = True


    def update(self):
        self.screen.fill(BACKGROUND)

        for particle in self.particles:
            if particle.pos[1] > HEIGHT:
                particle.pos = (random.randrange(0, WIDTH), random.randrange(-100, -10))
                particle.speed = random.randrange(200, 500)
            particle.update(self.dt)
            particle.draw(self.screen)


        pygame.draw.rect(self.screen, MAIN,  self.mainSurface, border_radius = 40 )
        text('to-do list', self.screen, MAIN_FONT, 32, 640, 110, True)

        pygame.draw.rect(self.screen, ADD_COLOR,  self.addRect, border_radius = 10 )
        text('Add', self.screen, MAIN_FONT, 32, 1000, 100)


        self.screen.blit(self.todoSurface, (200,150))


        if self.notupdated: # some optimiztion
            self.todoSurface.fill(MAIN)
            self.doneContainer = []
            for i in range(len(self.db)):
                pygame.draw.rect(self.todoSurface, CONTAINER, (0, (100 * i + 10) + self.offset, 880, 80) , border_radius = 10)
                text(str(self.db[i]), self.todoSurface, CONTAINER_FONT , 27, 440, (100 * i + 40) + self.offset, True)
                rect = pygame.Rect(850, (100 * i + 20) + self.offset, 20, 20)
                pygame.draw.rect(self.todoSurface, MAIN, rect, border_radius = 10)
                self.doneContainer.append(rect)

            self.notupdated = False

        pygame.display.flip()


g = Main()
while g.running:
	g.new()


pygame.quit()
