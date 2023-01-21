
import sys
if __name__ == '__main__':
    sys.path.append("D:\Python\RKit\GUIs")

import guis
#from guis.guis import *
import pygame
from pygame.locals import *
import random
import pathlib
import math
pygame.init()

usefull = False
looping=True
dw = 1280
dh = 640
ldw = 1280
ldh = 640
variabletest = 0
looping=True
clock = pygame.time.Clock()
score = 0
path = str(pathlib.Path(__file__).parent.resolve())
print(path,file=open("log.txt","w"))
gun = pygame.mixer.Sound(path+"/assets/duck_gun.ogg")
gun.set_volume(.5)
pygame.mixer.music.load(path+"/assets/war-full.wav")
video = guis.videoplayer.Video(path+"/assets/TitleScreen.mp4")
video.set_size((dw,dh))

class particle():
    def move(self):
        self.y+=self.yv
        self.x+=self.xv
        self.yv+=.45
        self.xv=self.xv*.99
        if(self.y>dh):
            if(len(self.trail)>0):
                self.trail.pop(0)
            else:
                particles.remove(self)
        else:
            self.trail.append((self.x,self.y))

    def draw(self,surface):
        last = self.getPos()
        pygame.draw.circle(surface,(150,0,0),last,radius=5)
        trail = self.trail.copy()
        trail.reverse()
        for x in trail:
            pygame.draw.line(surface,(150,0,0),x,last,width=10)
            last = x
            pygame.draw.circle(surface,(150,0,0),last,radius=5)
        #surface.blit( self.getSurface(),self.getBox())

    def getPos(self):
        return (self.x+8,self.y+8)

    def getTexture(self):
        return path+"/assets/blood.png"

    def getBox(self):
        #print((self.x,self.y,32,32))
        return (self.x,self.y,16,16)

    def getSurface(self):
        self.texbackup = self.getTexture()
        rect = (0,0,16,16)
        sprite = pygame.image.load( self.texbackup ).subsurface(rect)
        self.surf = sprite
        return self.surf


    def __init__(self,angle,pos):
        self.x = pos[0]+32
        self.xv = math.sin(math.radians(angle*18))*10
        self.y = pos[1]+32
        self.yv = math.cos(math.radians(angle*18))*10
        self.trail=[]

class bird():
    def die(self):
        global score
        if(self.dead):
            return
        self.dead = True
        self.frame2 = 0
        if(self.direction==None):
            score += 1000
            text.text = str(score)

    def advanceframe(self):
        self.frame+=1
        if(self.frame==3):
            self.frame=0
            if(self.dead):
                birds.remove(self)

    def getTexture(self):
        if(self.direction==None):
            return path+"/assets/furry.png"
        if(self.bear):
            return path+"/assets/polor_bear.png"
        return path+"/assets/duck_hunt.png"

    def getSurface(self):
        self.texbackup = self.getTexture()
        if(self.direction==None):
            rect = (0,0,32,32)
        else:
            if(self.bear==False):
                if(not self.dead):
                    if(self.color==0):
                        rect = (109+((self.frame)*36),8,36,36)
                    if(self.color==1):
                        rect = (107+((self.frame)*36),48,36,36)
                    if(self.color==2):
                        rect = (105+((self.frame)*36),91,36,36)
                else:
                    if(self.color==0):
                        rect = (225,8,36,36)
                    if(self.color==1):
                        rect = (223,48,36,36)
                    if(self.color==2):
                        rect = (221,91,36,36)
            else:
                if(not self.dead):
                    rect = (123+((self.frame)*30),297,30,33)
                else:
                    rect = (213,297,30,33)
        #print(rect)
        sprite = pygame.image.load( self.texbackup ).subsurface(rect)
        sprite = pygame.transform.scale2x(sprite)
        self.surf = pygame.transform.flip(sprite ,not self.direction,False)
        return self.surf

    def moveX(self,x):
        if(self.dead):
            return
        if(self.direction==True):
            self.x += x
            if(self.x>dw):
                self.die()
        elif(self.direction==False):
            self.x -= x
            if(self.x<-64):
                self.die()

    def getPos(self):
        return (self.x,self.y)

    def getBox(self):
        #print((self.x,self.y,32,32))
        if(self.direction==None):
            return (self.x,self.y,36,36)
        if(self.bear==True):
            return (self.x,self.y,33,33)
        return (self.x,self.y,36,36)

    def __init__(self,x,y,direction,bear=False):
        self.x = x
        self.y = y
        self.color = random.randint(0,2)
        self.frame = 0
        self.dead = False
        self.direction = direction
        self.speed = random.uniform(1,3)
        self.bear = bear

birds = [bird(0,0,True),bird(128,0,True)]
particles = []
mouse = None
spawns = [(208,448),(490,308),(1070,248),(1150,248),(460,308)]
doneMusic = False
doneIntro = False
introTime = 0
skipIntro = False
killCounter = 0

def renderframe(events,display,skipevents=False,screen=None):
    #print("frame")
    global dw
    global dh
    global mouse
    global doneMusic
    global doneIntro
    global introTime
    global killCounter
    guis.globallink = globals()
    if not skipevents:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                screen.prossesinputs("Keydown",event,display,globals())
            if event.type == pygame.KEYUP:
                screen.prossesinputs("Keyup",event,display,globals())
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.prossesinputs("Mousedown",event,display,globals())
                if(not doneIntro):
                    break
                gun.play()
                for x in birds:
                    pos = event.pos
                    #print(pos)
                    bpos = x.getPos()
                    if(bpos[0]<pos[0] and bpos[1]<pos[1]):
                        if(bpos[0]+64>pos[0] and bpos[1]+64>pos[1]):
                            x.die()
                            if(not x.dead):
                                if x.direction!=None:
                                    killCounter+=1
                                    if(killCounter>20):
                                        killCounter=0
                                        i = spawns[int(random.uniform(0,4))]
                                        birds.append(bird(i[0],i[1], None))
                                for p in range(20):
                                    particles.append(particle(p,bpos))
                            break

            if event.type == pygame.MOUSEMOTION:
                screen.prossesinputs("Mousemove",event,display,globals())
                mouse = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                screen.prossesinputs("Mouseup",event,display,globals())
            if event.type == pygame.FINGERDOWN:
                pass
            if event.type == pygame.FINGERUP:
                pass
            if event.type == pygame.VIDEORESIZE:
                s = pygame.display.get_window_size()
                guis.dw = s[0]
                guis.dh = s[1]
                display.fill((0,0,0))
                pygame.display.update()
            if event.type == WINDOWLEAVE:
                screen.prossesinputs("Mouseleave",event,display,globals())

    clock.tick(120)
    #pygame.display.update()
    screen.redraw(display)
    if((doneIntro or skipIntro)and not doneMusic ):
        #print("s")
        pygame.mixer.music.play(loops=-1)
        doneMusic = True
    if(len(particles)>0):
        blood = pygame.image.load(path+"/assets/blood_overlay.png")
        pygame.transform.scale(blood,(dw,dh))
        gameDisplay.blit(blood,(0,0,dw,dh))
    surface = surfacewidget.mysurface
    if(random.random()>.99):
        if(random.random()>.5):
            if(random.random()>.5):
                birds.append(bird(0,random.uniform(0,dh/2), True  ))
            else:
                birds.append(bird(dw-32,random.uniform(0,dh/2), False))
        else:
            if(random.random()>.5):
                birds.append(bird(0,random.uniform(dh/1.2,(dh/1.2)-32), True ,True ))
            else:
                birds.append(bird(dw-32,random.uniform(dh/1.2,(dh/1.2)-32), False,True))
    for x in birds:
        x.moveX(x.speed);
        if(not hasattr(x,"frame2")):
            x.frame2=0
        else:
            x.frame2+=1
        if(x.frame2%10==0):
            x.advanceframe()
        surface.blit( x.getSurface(),x.getBox())
    for x in particles:
        x.move()
        x.draw(surface)
    if(mouse!=None):
        image = pygame.image.load(path+"/assets/target.png")
        image = pygame.transform.scale(image,(32,32))
        surface.blit(image ,(mouse[0]-16,mouse[1]-16,32,32))
    #print(introTime)
    if(introTime<=450 and not skipIntro):
        video.draw(display,(0,0))
        introTime+=1
    else:
        #print("s")
        doneIntro=True
        video.close()

def render():
    global looping
    guis.globallink = globals()
    while looping:
        global variablestr
        global variabletest
        #Quit on clicking the "X" in the corner, or by pressing the escape + enter key.
        variabletest += .5
        clock.tick(60)
        #variablestr = str(round(variabletest))
        #variabletest+=1
        renderframe( pygame.event.get(),gameDisplay,screen=screen )
        screen.update()
        pygame.display.update()
        #pygame.time.wait(1500)
        variabletest += .5
        #print("Tick",clock.get_time())
        #print(vl.countchildren())
    pygame.quit()

if True:
    if usefull:
        gameDisplay = pygame.display.set_mode((ldw, ldh), pygame.FULLSCREEN,pygame.RESIZABLE )
        s = pygame.display.get_window_size()
        dw = s[0]
        dh = s[1]
    else:
        gameDisplay = pygame.display.set_mode((ldw, ldh),pygame.RESIZABLE)
    s = pygame.display.get_window_size()
    dw = s[0]
    dh = s[1]
    pygame.display.set_icon(pygame.image.load( path+"/assets/duck_icon.png"))
    pygame.display.set_caption('Duck massacre')


screen = guis.mainWidget("blue",inglobals=globals(),style={},data={})
overlay = guis.overlayWidget("Overlay",screen)
image = guis.imageWidget("Img",overlay,style={"W":"pygame.display.get_window_size()[0]","H":"pygame.display.get_window_size()[1]","Image":path+"/assets/background.png"})
vlist = guis.vlistWidget("List",overlay)
hlist = guis.hlistWidget("Hlist",vlist)
surfacewidget = guis.surfaceWidget("Surface",overlay,style={"W":"pygame.display.get_window_size()[0]","H":"pygame.display.get_window_size()[1]"})
guis.emptyWidget("Empty",hlist,style={"W":"pygame.display.get_window_size()[0]-160","H":32})
guis.textWidget("Text",hlist,style={"W":76,"H":32,"Text":"Score:"})
text = guis.textWidget("Text2",hlist,style={"W":32,"H":32})
text.text = str(score)
render()
