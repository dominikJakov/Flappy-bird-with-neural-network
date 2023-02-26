import nn
import pygame
import random
import time

#brain = nn.Neurol_Network(2,4,1)

pygame.init()

DisplayHeight = 600

DisplayWidth = 800

gameDisplay = pygame.display.set_mode((DisplayWidth,DisplayHeight))

pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface,textSurface.get_rect()


def message_display(text,x,y):
    largeText = pygame.font.Font("freesansbold.ttf", 25)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    gameDisplay.blit(TextSurf, TextRect)

def Game_over():
    Game_loop()

class bird():
    def __init__(self):
        self.fitnes = 0
        self.brain = nn.Neurol_Network(5,4,1)
        self.x = 100
        self.y = random.randrange(200, 400)
        self.jump_force = 0
        self.Player_Image = pygame.image.load("C:/Users/Dominik/Documents/Python/Projects/flappy bird/flappybirdbird.png")
    #    self.Player_Image_best = pygame.image.load("C:/Users/Dominik/Documents/Python/Projects/flappy bird/flappybirdbird2.png")
        self.pipe_near = Pipe()
        self.dead = False
        DisplayHeight = 600
        DisplayWidth = 800

    def jump(self):
        if self.y > 30:
            self.jump_force = 8;

    def predict(self):
        inputs  = [1,2,3,4,5]
        inputs[0] = self.y / DisplayHeight
        inputs[1] = (self.pipe_near.y_up + 550) / DisplayHeight
        inputs[2] = self.pipe_near.y_down / DisplayHeight
        inputs[3] = self.pipe_near.x/ DisplayWidth
        inputs[4] = self.jump_force / 8
        if self.brain.feedfoward(inputs)[0] > 0.5:
            self.jump()

    def gravity_down(self,gravity_force):
        if self.jump_force > -4:
            self.jump_force -= gravity_force
        self.y += -self.jump_force

    def draw(self):
    #    pygame.draw.rect(gameDisplay,black,[self.x,self.y,84,60])
        gameDisplay.blit(self.Player_Image,(self.x,self.y))


    def check_near_pipe(self,pipes):
        new_pipes = []
        for x in range(0,len(pipes)):
            if pipes[x].x - self.x > 0:
                new_pipes.append(pipes[x])
        self.pipe_near =  new_pipes[0]
        for a in range(0,len(new_pipes)):
            if self.pipe_near.x - self.x > new_pipes[a].x - self.x:
                self.pipe_near = new_pipes[a]

class Pipe():
    def __init__(self):
        self.x = 800
        self.y_up = -random.randrange(50, 300)
        self.y_down = self.y_up + 550
        self.Pipe_down_Image = pygame.image.load("C:/Users/Dominik/Documents/Python/Projects/flappy bird/pipe_down.png")
        self.Pipe_up_Image = pygame.image.load("C:/Users/Dominik/Documents/Python/Projects/flappy bird/pipe_up.png")

    def move_left(self):
        self.x -= 4

    def offscreen(self):
        if self.x < 0:
            return True
        else:
            return False

    def draw(self):
        gameDisplay.blit(self.Pipe_down_Image,(self.x,self.y_down))
        gameDisplay.blit(self.Pipe_up_Image,(self.x,self.y_up))

    #    pygame.draw.rect(gameDisplay,green,[self.x,self.y_down,128,793])
    #    pygame.draw.rect(gameDisplay,green,[self.x,self.y_up,128,793])


    def collision_check(self,bird_x,bird_y):
      if bird_y > self.y_down - 30 or bird_y < self.y_up + 395:
         if bird_x > (self.x - 32) and bird_x < (self.x + 69):
                return True
      if  bird_y >  600 :
         return True

class population():

    def __init__(self):
        self.new_game = True
        self.fittnes = []
        self.organisam = []
        self.best_organisam = bird()
        self.puplation_number = 200
        self.max_fittnes_ever = 0
        self.max_fittnes_organisam = bird()

    def repopulation(self):
        self.organisam = []
        self.fittnes = []
        for x in range(self.puplation_number):
            self.organisam.append(bird())
            self.fittnes.append(0)
        self.fittnes.append(0)
        self.fittnes.append(0)



    def find_best_organisam(self):
            for x in range(len(self.organisam)):
                    if self.fittnes[x] == max(self.fittnes):
                        self.best_organisam = self.organisam[x]
                        if self.fittnes[x] > self.max_fittnes_ever:
                            self.max_fittnes_ever = self.fittnes[x]
                            self.max_fittnes_organisam = self.organisam[x]


    def copy_DNA(self):
        for x in range(len(self.organisam)):
            self.organisam[x].brain = self.best_organisam.brain.copy()
            self.organisam[x].brain.mutate(0.1)
    #    self.best_organisam.Player_Image = pygame.image.load("C:/Users/Dominik/Documents/Python/Projects/flappy bird/flappybirdbird2.png")
        self.organisam.append(self.best_organisam)
        self.organisam.append(self.max_fittnes_organisam)

generation = 0
Population = population()
def Game_loop():
    global Population
    global generation


    death_bird = []
    frame_counter_points_start = 0
    pocetak_pointsa = False
    gravity = 0.6
    pipes = [Pipe()]

    frame_counter = 0
    points = 0
    if Population.new_game == False:
        Population.find_best_organisam()
        avg_fittnes = sum(Population.fittnes) / len(Population.fittnes)
    Population.repopulation()
    if Population.new_game == False:
        Population.copy_DNA()

    Population.new_game = False

    for b in range(0,len(Population.organisam)):
        Population.organisam[b].pipe_near = pipes[0]

    generation += 1

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_SPACE:
        for x in range(0,len(Population.organisam)):
            if Population.organisam[x].dead == False:
                Population.fittnes[x] += 1
                Population.organisam[x].predict()
                Population.organisam[x].check_near_pipe(pipes)


        gameDisplay.fill(white)

        frame_counter += 1
        frame_counter_points_start += 1

        if frame_counter % 120 == 0:
            pipes.append(Pipe())
            frame_counter= 0

        if frame_counter_points_start % 90 == 0:
            pocetak_pointsa = True
            frame_counter_points_start = 0

        if frame_counter_points_start % 120 == 0:
            if pocetak_pointsa == True:
                frame_counter_points_start = 0
                points += 1

        for x in range(0,len(Population.organisam)):
            if Population.organisam[x].dead == False:
                Population.organisam[x].gravity_down(gravity)
                Population.organisam[x].draw()


        for a in range(0,len(pipes)):
            pipes[a].move_left()
            pipes[a].draw()
            for b in range(0,len(Population.organisam)):
                if Population.organisam[b].dead == False:
                    if pipes[a].collision_check(Population.organisam[b].x,Population.organisam[b].y) == True:
                        Population.organisam[b].dead = True

        for x in range(0,len(pipes)):
            if pipes[x].offscreen() == True:
                pipes.pop(0)
                break

        broj_mrtvih = 0
        for x in range(0,len(Population.organisam)):
            if Population.organisam[x].dead == True:
                broj_mrtvih += 1

        if  broj_mrtvih == len(Population.organisam):
            Game_over()

        message_display("Points " + str(points),60,30)
        message_display("Generation " + str(generation),90,60)
        message_display("Live " + str(len(Population.organisam) - broj_mrtvih),60,90)
        message_display("Max Fittnes " + str(Population.max_fittnes_ever),90,120)
        if generation > 1:
            message_display("Avg Fittnes " + str(int(avg_fittnes)),100,150)
        pygame.display.update()
        clock.tick(1000)

Game_loop()
pygame.quit()
quit()
