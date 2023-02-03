import sys

if __name__ == '__main__':
    sys.path.append("D:\Python\RKit\GUIs")
    sys.path.append("/media/tommy/Tommy/Python/RKit/GUIs")

import guis
# from guis.guis import *
import pygame
from pygame.locals import *
from random import uniform,randint,random
import pathlib
from math import sin,cos,radians
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

usefull = False
looping = True
ldw = 1280
ldh = 640
path = str(pathlib.Path(__file__).parent.resolve())
if __name__ == "__main__":
    if usefull:
        gameDisplay = pygame.display.set_mode((ldw, ldh), pygame.FULLSCREEN, pygame.RESIZABLE)
        s = pygame.display.get_window_size()
        dw = s[0]
        dh = s[1]
    else:
        gameDisplay = pygame.display.set_mode((ldw, ldh), pygame.RESIZABLE)
    s = pygame.display.get_window_size()
    dw = s[0]
    dh = s[1]
gameDisplay = pygame.display.get_surface()
pygame.display.set_icon(pygame.image.load(path + "/assets/duck_icon.png"))
pygame.display.set_caption('Duck massacre')
s = pygame.display.get_window_size()
dw = s[0]
dh = s[1]
variabletest = 0
looping = True
clock = pygame.time.Clock()
score = 0
# print(path,file=open("log.txt","w"))
gun = pygame.mixer.Sound(path + "/assets/duck_gun.ogg")
gun.set_volume(.5)
pygame.mixer.music.load(path + "/assets/war-full.wav")
pygame.mixer.music.set_volume(.5)
video = guis.videoplayer.Video(str(path) + "/assets/TitleScreen.mp4", 23.98, 356, 14, dw, dh)
video.set_size((dw, dh))
sprites = {}


class particle():
    def move(self):
        global particles
        self.y += self.yv
        self.x += self.xv
        self.x += uniform(-1, 1)
        self.yv += uniform(.41, .49)
        self.xv = self.xv * uniform(.9, 1)
        if self.y > dh or len(self.trail) >= 20:
            if len(self.trail) > 0:
                self.trail.pop(0)
            else:
                particles.remove(self)
        else:
            self.trail.append(( self.getX(), self.getY() ))

    def draw(self, surface):
        last = (self.x, self.y)
        # pygame.draw.circle(surface,(150,0,0,155),self.modPos(last),radius=5)
        # trail = self.trail.copy()
        # trail.reverse()
        if len(self.trail) > 2:
            pygame.draw.polygon(surface, (150, 0, 0), self.trail)
        """
        for x in trail:
            pygame.draw.line(surface,(150,0,0),self.modPos(x),self.modPos(last),width=10)
            last = x
            pygame.draw.circle(surface,(150,0,0),self.modPos(last),radius=5)"""
        # surface.blit( self.getSurface(),self.getBox())

    def modPos(self, pos):
        x = (pos[0] / 1280) * dw
        y = (pos[1] / 640) * dh
        return (x, y)

    def getPos(self):
        return (self.getX(), self.getY())

    def getX(self):
        return (self.x / 1280) * dw

    def getY(self):
        return (self.y / 640) * dh

    def getTexture(self):
        return path + "/assets/blood.png"

    def getBox(self):
        # print((self.x,self.y,32,32))
        return (self.getX(), self.getY(), 16, 16)

    def getSurface(self):
        return None

    def __init__(self, angle, pos):
        self.x = pos[0] + 32 + sin(radians(angle * 36)) * 15
        self.xv = sin(radians(angle * 36)) * 10
        self.y = pos[1] + 32 + cos(radians(angle * 36)) * 15
        self.yv = cos(radians(angle * 36)) * 10
        self.trail = []


class bird():
    def die(self):
        global score
        if (self.dead):
            return
        self.dead = True
        self.frame = 0
        if self.direction == None:
            score += 1000
            text.text = str(score)

    def advanceframe(self):
        self.frame += 1
        if self.frame == 3:
            self.frame = 0
            if self.dead:
                birds.remove(self)

    def getTexture(self):
        if (self.direction == None):
            return path + "/assets/furry.png"
        if (self.bear):
            return path + "/assets/polor_bear.png"
        return path + "/assets/duck_hunt.png"

    def getSurface(self):
        self.texbackup = self.getTexture()
        if (self.direction == None):
            rect = (0, 0, 32, 32)
        else:
            if (self.bear == False):
                if (not self.dead):
                    if (self.color == 0):
                        rect = (109 + ((self.frame) * 36), 8, 36, 36)
                    if (self.color == 1):
                        rect = (107 + ((self.frame) * 36), 48, 36, 36)
                    if (self.color == 2):
                        rect = (105 + ((self.frame) * 36), 91, 36, 36)
                else:
                    if (self.color == 0):
                        rect = (225, 8, 36, 36)
                    if (self.color == 1):
                        rect = (223, 48, 36, 36)
                    if (self.color == 2):
                        rect = (221, 91, 36, 36)
            else:
                if (not self.dead):
                    rect = (123 + ((self.frame) * 30), 297, 30, 33)
                else:
                    rect = (213, 297, 30, 33)
        # print(rect)
        outstr = "".join( (self.texbackup,":",str(self.frame),str(self.dead)))
        if outstr in sprites:
            sprite = sprites[outstr]
        else:
            sprite = pygame.image.load(self.texbackup).convert_alpha().subsurface(rect)
            sprites[outstr] = sprite

        self.surf = pygame.transform.scale2x(sprite)
        if not self.direction:
            self.surf = pygame.transform.flip(self.surf, True, False)
        return self.surf

    def moveX(self, x):
        if (self.dead):
            return
        if (self.direction == True):
            self.x += x
            if (self.x > dw):
                self.die()
        elif (self.direction == False):
            self.x -= x
            if (self.x < -64):
                self.die()

    def getPos(self):
        return (self.getX(), self.getY())

    def getX(self):
        return (self.x / 1280) * dw

    def getY(self):
        return (self.y / 640) * dh

    def getBox(self):
        # print((self.x,self.y,32,32))
        if (self.direction == None):
            return (self.getX(), self.getY(), 36, 36)
        if (self.bear == True):
            return (self.getX(), self.getY(), 33, 33)
        return (self.getX(), self.getY(), 36, 36)

    def __init__(self, x, y, direction, bear=False):
        self.x, self.y  = x,y
        self.color = randint(0, 2)
        self.frame = 0
        self.dead = False
        self.direction = direction
        self.speed = uniform(1, 3)
        self.bear = bear


birds = [bird(0, 0, True)]
particles = []
spawns = [(208, 448), (490, 308), (1070, 248), (1150, 248), (460, 308)]

frame = 0


def spawnFurry():
    i = spawns[int(uniform(0, 4))]
    w = i[0]
    h = i[1]
    birds.append(bird(w, h, None))


def Font(fontFace, size):
    return pygame.font.Font(fontFace, round(size))


class DataStore:
    def __init__(self):
        self.doneMusic = False
        self.doneIntro = False
        self.introTime = 0
        self.frame = 0
        self.skipIntro = True
        self.killCounter = 0
        self.mouse = None
        blood = pygame.image.load(path + "/assets/blood_overlay.png").convert_alpha()
        self.blood = pygame.transform.scale(blood, (dw, dh))
        targetimage = pygame.image.load(path + "/assets/target.png").convert_alpha()
        self.targetimage = pygame.transform.scale(targetimage, (32, 32))
        background = pygame.image.load(path + "/assets/background.png").convert_alpha()
        self.background = pygame.transform.scale(background, (dw, dh))
        self.bloodbackground = self.background.copy()
        self.bloodbackground.blit(self.blood, (0, 0, dw, dh))
        self.bloodbackground.convert()

        fontpath = str(pathlib.PurePath(path, "assets/Xolonium-Bold.ttf"))
        self.font = Font(fontpath,32)



data = DataStore()


def renderframe(events, display, skipevents=False, screen=None):
    # print("frame")
    global dw
    global dh
    #guis.globallink = globals()
    if not skipevents:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                screen.prossesinputs("Keydown", event, display, globals())
            if event.type == pygame.KEYUP:
                screen.prossesinputs("Keyup", event, display, globals())
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.prossesinputs("Mousedown", event, display, globals())
                if (not data.doneIntro):
                    break
                gun.play()
                for x in birds:
                    pos = event.pos
                    # print(pos)
                    bpos = (x.getPos())
                    brealpos = (x.x, x.y)
                    if (bpos[0] < pos[0] and bpos[1] < pos[1]):
                        if (bpos[0] + 64 > pos[0] and bpos[1] + 64 > pos[1]):
                            if (not x.dead):
                                if x.direction != None:
                                    data.killCounter += 1
                                    if (data.killCounter > 19):
                                        data.killCounter = int(uniform(0, 5))
                                        spawnFurry()
                                for p in range(10):
                                    particles.append(particle(p, brealpos))
                            x.die()
                            break
            if event.type == pygame.MOUSEMOTION:
                screen.prossesinputs("Mousemove", event, display, globals())
                data.mouse = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                screen.prossesinputs("Mouseup", event, display, globals())
            if event.type == pygame.VIDEORESIZE:
                s = pygame.display.get_window_size()
                guis.dw = s[0]
                guis.dh = s[1]
                dw = s[0]
                dh = s[1]
                display.fill((0, 0, 0))
                targetimage = pygame.transform.scale(targetimage, (32, 32))
                blood = pygame.transform.scale(blood, (dw, dh))
                pygame.display.update()
            if event.type == WINDOWLEAVE:
                screen.prossesinputs("Mouseleave", event, display, globals())

    # pygame.display.update()
    print(clock.get_fps())
    # screen.redraw(display)
    if (data.doneIntro or data.skipIntro) and not data.doneMusic:
        # print("s")
        pygame.mixer.music.play(loops=-1)
        data.doneMusic = True
    if len(particles) > 0:
        gameDisplay.blit(data.bloodbackground, (0, 0, dw, dh), special_flags=pygame.BLEND_ALPHA_SDL2)
        pass
    surface = gameDisplay
    if random() > .985:
        if (random() > .5):
            if (random() > .5):
                birds.append(bird(0, uniform(0, dh / 2), True))
            else:
                birds.append(bird(dw - 32, uniform(0, dh / 2), False))
        else:
            if (random() > .5):
                birds.append(bird(0, uniform(dh / 1.2, (dh / 1.2) - 32), True, True))
            else:
                birds.append(bird(dw - 32, uniform(dh / 1.2, (dh / 1.2) - 32), False, True))
    data.frame += 1
    for x in birds:
        x.moveX(x.speed)
        if data.frame % 5 == 0:
            x.advanceframe()
        surface.blit(x.getSurface(), x.getBox())
    for x in particles:
        x.move()
        x.draw(surface)
    if (data.mouse != None):
        surface.blit(data.targetimage, (data.mouse[0] - 16, data.mouse[1] - 16, 32, 32))
    # print(introTime)
    if data.introTime <= 450 and not data.skipIntro:
        video.draw(display, (0, 0))
        data.introTime += 1
    else:
        # print("s")
        if not data.doneIntro:
            data.doneIntro = True
            video.close()

print("BLAH")

def render():
    global looping
    guis.globallink = globals()
    while 1:
        global variablestr
        global variabletest
        # Quit on clicking the "X" in the corner, or by pressing the escape + enter key.
        # variabletest += .5
        clock.tick(60)
        # variablestr = str(round(variabletest))
        # variabletest+=1
        gameDisplay.fill(pygame.Color("blue3"))
        gameDisplay.blit(data.background,(0,0,dw,dh))
        gameDisplay.blit(data.font.render("Score: "+str(score),False,"black"),dest=(dw-320,0,320,dh))
        renderframe(pygame.event.get(), gameDisplay, screen=screen)
        # screen.update()
        pygame.display.flip()
        # pygame.time.wait(1500)
        # variabletest += .5
        # print("Tick",clock.get_time())
        # print(vl.countchildren())
    pygame.quit()


screen = guis.mainWidget("blue", inglobals=globals(), style={}, data={})
overlay = guis.overlayWidget("Overlay", screen)
image = guis.imageWidget("Img", overlay,
                         style={"W": "pygame.display.get_window_size()[0]", "H": "pygame.display.get_window_size()[1]",
                                "Image": path + "/assets/background.png"})
vlist = guis.vlistWidget("List", overlay)
hlist = guis.hlistWidget("Hlist", vlist)
surfacewidget = guis.surfaceWidget("Surface", overlay, style={"W": "pygame.display.get_window_size()[0]",
                                                              "H": "pygame.display.get_window_size()[1]"})
guis.emptyWidget("Empty", hlist, style={"W": "pygame.display.get_window_size()[0]-240", "H": 32})
guis.textWidget("Text", hlist, style={"W": 76, "H": 32, "Text": "Score:"})
text = guis.textWidget("Text2", hlist, style={"W": 128, "H": 32})
text.text = str(score)
render()
