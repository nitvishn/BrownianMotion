import random
import math
import pygame
from copy import deepcopy

random.seed()
pygame.init()
length=1200
display=pygame.display.set_mode((1300, 700))
pygame.display.set_caption('Brownian Motion Simulation')
clock = pygame.time.Clock()
red = (255,0,0)
green = (50,255,100)
blue = (200,50,200)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
grey=(0, 0, 0)
light_grey=(58, 58, 58)

display.fill(black)

class Position(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def getCoordinates(self):
        return (self.x, self.y)

    def __str__(self):
        return str((self.x, self.y))

def inProximity(pos1, pos2):
    x1=pos1.x
    x2=pos2.x
    y1=pos1.y
    y2=pos2.y
    distance=math.sqrt(((x1-x2)**2)+((y1-y2)**2))
    if(distance<20):
        return True
    else:
        return False

class GasParticle(object):
    def __init__(self, speed, position):
        # self.tendency = random.random()*3
        self.speed=speed
        self.position=position

    def updatePos(self, multiplier):
        # if(random.random()>0.5):
        #     self.tendency = random.random() * 3
        # tendency=self.tendency
        # tendency=multiplier
        x=self.position.x
        y=self.position.y
        speed=self.speed*multiplier

        angle=random.random()*2*math.pi
        x2=speed*math.cos(angle) + x
        y2=speed*math.sin(angle) + y
        chosen=Position(x2, y2)


        # choices=[
        #     Position(x+speed, y),
        #     Position(x-speed, y),
        #     Position(x, y+speed),
        #     Position(x, y-speed),
        #     Position(x+sqrt(speed), y+sqrt(speed)),
        #     Position(x+sqrt(speed), y-sqrt(speed)),
        #     Position(x-sqrt(speed), y+sqrt(speed)),
        #     Position(x-sqrt(speed), y-sqrt(speed))
        # ]
        # chosen = random.choice(choices)

        while(chosen.x<100 or chosen.y<100 or chosen.y>600 or chosen.x>1200):
            angle = random.random() * 2 * math.pi
            x2 = speed * math.cos(angle) + x
            y2 = speed * math.sin(angle) + y
            chosen = Position(x2, y2)
        self.position=chosen

    def getPosition(self):
        return self.position

    def __str__(self):
        return 'GasParticle'+str(self.position)

multiplier=1
numParticles=100

var2=4.2387543253

class AmmoniaParticle(GasParticle):
    def __init__(self, pos):
        GasParticle.__init__(self, var2, pos)

class HclParticle(GasParticle):
    def __init__(self, pos):
        GasParticle.__init__(self, 1, pos)

def density(particles):
    x0=2000
    y0=2000
    x1=0
    y1=0
    num=0
    for item in particles:
        num+=1
        if(item.position.x<x0):
            x0=item.position.x
        elif(item.position.x>x1):
            x1=item.position.x
        if(item.position.y<y0):
            y0=item.position.y
        elif(item.position.y>y1):
            y1=item.position.y
    try:
        return num/(x1-x0)*(y1-y0)
    except:
        return num

def touchingBorder(pos):
    x=pos.x
    y=pos.y
    if(x<=110):
        return True
    elif(x>=length-10):
        return True
    elif(y<=110):
        return True
    elif(y>=550):
        return True
    return False

def getPressure(aparticles, hparticles):
    count=0
    particles=deepcopy(aparticles)
    particles.extend(hparticles)
    for item in particles:
        if(touchingBorder(item.position)):
            count+=1
    return count

aparticles=[]
for i in range(numParticles):
    pos=Position(random.randint(100, 500), random.randint(100, 600))
    aparticles.append(AmmoniaParticle(pos))
hparticles=[]
for i in range(numParticles):
    pos=Position(random.randint(length-250, length), random.randint(100, 600))
    hparticles.append(HclParticle(pos))

particles=[]
corners = [(100, 100), (100, 600), (length, 600), (length, 100)]

circlesize=4
outline=2

fps=30

sliderpos=200

crashed = False
moving=False

pressureList=[]

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex=pygame.mouse.get_pos()[0]
            mousey=pygame.mouse.get_pos()[1]
            if(abs(mousey-50)<50):
                if(mousex>sliderpos and mousex-sliderpos<10):
                    moving=True
                elif(mousex<sliderpos and sliderpos-mousex<10):
                    moving=True
        if event.type == pygame.MOUSEBUTTONUP:
            moving=False
            print("up")
    display.fill(black)

    if(moving):
        x=pygame.mouse.get_pos()[0]
        sliderpos=x
        if(sliderpos>290):
            sliderpos=290
        if(sliderpos<110):
            sliderpos=110

    #WHITE PARTICLES
    pygame.draw.rect(display, white, (940, 30, 260, 30), 1)
    percentage=len(particles)/numParticles
    pygame.draw.rect(display, white, (945, 35, percentage*250, 20))

    #GREEN PARTICLES
    pygame.draw.rect(display, white, (675, 30, 260, 30), 1)
    percentage = len(hparticles) / numParticles
    pygame.draw.rect(display, green, (680, 35, percentage * 250, 20))

    #BLUE PARTICLES
    pygame.draw.rect(display, white, (410, 30, 260, 30), 1)
    percentage = len(hparticles) / numParticles
    pygame.draw.rect(display, blue, (415, 35, percentage * 250, 20))

    #PRESSURE BAR
    pressureList.append(getPressure(aparticles, hparticles) / (numParticles))
    pressure=sum(pressureList)/len(pressureList)+0.4
    print(pressure)
    if(len(pressureList)>=fps):
        pressureList=[]
    pygame.draw.rect(display, white, (100, 630, 260, 30), 1)
    pygame.draw.rect(display, red, (105, 635, pressure * 250, 20))

    #SLIDER
    multiplier=((sliderpos-100)/180)*10
    pygame.draw.line(display, white, (100, 50), (300, 50))
    pygame.draw.line(display, white, (100, 40), (100, 60))
    pygame.draw.line(display, white, (300, 40), (300, 60))
    pygame.draw.circle(display, white, (sliderpos, 50), 10)

    adensity=density(aparticles)
    for particle in aparticles:
        x=particle.position.x
        y=particle.position.y
        particle.updatePos(multiplier)
        # while(density(aparticles)>adensity):
        #     particle.position.x=x
        #     particle.position.y=y
        #     particle.updatePos()
        color=blue
        pygame.draw.circle(display, color, (int(particle.position.x), int(particle.position.y)), circlesize, outline)


    for particle in hparticles:
        for particle2 in aparticles:
            if(inProximity(particle.position, particle2.position)):
                particles.append(GasParticle((0.000000003)*multiplier, particle.position))
                hparticles.remove(particle)
                aparticles.remove(particle2)
                break
        particle.updatePos(multiplier)
        color=green
        pygame.draw.circle(display, color, (int(particle.position.x), int(particle.position.y)), circlesize, outline)


    for particle in particles:
        particle.updatePos(multiplier)
        color=white
        pygame.draw.circle(display, color, (int(particle.position.x), int(particle.position.y)), circlesize+2, 0)


    pygame.draw.lines(display, white, True, corners, 10)
    pygame.display.update()
    clock.tick(fps)
print(crashed)