import pygame
import pickle

from random import randint

colors={"red": (240, 20, 20), "blue": (20, 20, 240), "grey": (120, 120, 120), "white": (255, 255, 255), "black": (20, 20, 20), "brown": (131, 52, 0)}

pygame.init()
wn = pygame.display.set_mode((1300, 700), pygame.RESIZABLE)
pygame.display.set_caption("Spellsword")
clock=pygame.time.Clock()
dt=60
scene=0
reactimer=0
react=False
attacker=None
scenes = {}
terrain={}
buttons = {}
Uimenu = {}
enemies={}
textBoxes={}
all = {}
selfdraw=[]
#list of enemys about to attack the player and where they are in the animation, and where the cutoff is
attacklis=[]
timerbar=False
cs=[]
#bar active (only one timer bar at a time)
ba=False
newsound = lambda x: pygame.mixer.Sound(f"./sound/{x}.wav")
newimg = lambda x: pygame.image.load(f"./img/{x}.png").convert_alpha()
#progressbarimg
bpimg = newimg("barprogress")
#barmarkerimg
bmimg= newimg("barmarker")
#barcircle
bcimg=newimg("barcircle")

playerimg=newimg("character/Idle")
playerhitimg=newimg("character/got_hit")
#player walk animation
pwa=[newimg(f"character/walk_{i}") for i in range(1, 8)]
pwa = [newimg("character/Idle")]+pwa
pohsa=[newimg(f"character/overhead/overhead-{i}") for i in range(1, 13)]
pha = [playerhitimg, playerimg, playerimg]
#backwards cuz im dumb af and lazy
h1s = [newimg(f"enemy/humanoid1/humanoid1swing ({i})") for i in range(17, 1, -1)]

# player hit sound
phs = newsound("playerhit")

timeractive=False

def tertiary(player):
    return not (player.overswing or player.hit or ba)

def combat(atkskl, defskl, defagl):
    pass
    #global dt
    #dt=15 -()

def chooseDefence(attacka, player):
    global ba
    if ba == False: 
        
        ba=True
    else: return
    global attacker
    global react
    attacker=attacka
    react=True
    scene.addObject(timerBar(1366/2-5, 50, decision=True, spd=(player.lvl / ((player.agl + player.skl)/20)**0.5)**1.5), False)

    
class text():
    def __init__(self, x, y, text, size, txtcolor, bgcolor=None):
        self.font = pygame.font.Font("./data/upheavtt.ttf", size)
        self.textcontent=text
        if bgcolor != None:
            self.text = [self.font.render(i, False, txtcolor, bgcolor) for i in text]
        else:
            self.text = [self.font.render(i, False, txtcolor) for i in text]
        self.rects=[txt.get_rect() for txt in self.text]
        for i in self.rects:
            i.x=x
        offset=0
        for i in self.rects:
            i.y=y+offset
            offset+=size
        textBoxes[self]=self

        


class tButton():
    def __init__(self, x, y, w, h, img, onclick, arg=[]):
        self.x=x
        self.y=y
        self.h=h
        self.w=w
        self.img=img
        self.onclick=onclick
        self.rect = self.img.get_rect()
        self.rect.center = (x-w/2, y-h/2)
        buttons[self] = self
        all[self]=self
        Uimenu[self]=self
        self.arg=arg
        
    def onClick(self):
        global scene
        
        scene=scenes[self.onclick]()
        
        
class button():
    def __init__(self, x, y, w, h, img, onclick, arg=[], custom=False):
        self.x=x
        self.y=y
        self.h=h
        self.w=w
        self.img=img
        self.onclick=onclick
        self.rect = self.img.get_rect()
        self.rect.center = (x-w/2, y-h/2)
        if custom == False:
            buttons[self] = self
            all[self]=self
            Uimenu[self]=self
        self.arg=arg
        
    def onClick(self):
        if self.arg == []:
            self.onclick()
        else:
            self.onclick(self.arg)
    
class Terrain():
    def __init__(self, x, y, img, collision: False):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.center = (x-self.rect.w, y-self.rect.h)
        self.collision=collision
        terrain[self] = self

class Scene():
    def __init__(self):
        self.drawable=[]
        pass

    def handleEvent(self, event):
        raise NotImplementedError(f"Dumb mofo forgor to handle event: {self}")
    
    def update(self, event):
        raise NotImplementedError(f"Dumb mofo forgor to write an update: {self}")
    
    def addObject(self, obj):
        raise NotImplementedError(f"dumb mofo forgor to addObjects >.<: {self}")
    
    def draw(self, event):
        raise NotImplementedError(f"Dumb mofo forgor to draw: {self}")
class entity():
    def __init__(self, stn, hp, agl, skl, lvl=1):
        self.calc_stats(stn, hp, agl, skl, lvl)
        self.lvl=lvl
        maxv=max(stn, hp, agl, skl)
        if stn == maxv:
            self.element="fire"
            
        if hp == maxv:
            self.element="earth"
        if agl==maxv:
            self.element="water"
        if skl==maxv:
            self.element="air"
            
    def calc_stats(self, stn, hp, agl, skl, lvl):
        self.str=(3+(stn*0.05))*(1+(stn*0.02)) + (0.15*lvl*(1+(stn/5)))
        self.hp=(10+(hp*0.2))*(1+(hp*0.03)) + (0.5*lvl*(1+hp/5))
        self.agl=(5+(agl*0.1))*(1+(agl*0.04)) + (0.25*lvl*(1+agl/5))
        self.skl=(5+(skl*0.1))*(1+(skl*0.04)) + (0.25*lvl*(1+skl/5))
        self.turntime=1.8/(((self.agl-5)*3)**0.5)

class player_class(entity):
    def __init__(self, stn, hp, agl, skl, lvl=1):
        super().__init__(stn, hp, agl, skl, lvl)
        self.img=playerimg
        self.rect=self.img.get_rect()
        self.rect.w-=50
        self.rect.center=(630, 500)
        self.crect=self.img.get_rect()
        self.crect.w-=70
        self.crect.center=(640, 500)
        self.ohswrect=pygame.Rect(680, 450, 90, 70)
        
        self.hit=False
        self.onground=False
        self.flip=False
        self.wanttoflip=False
        self.fliptimer=0
        self.overswing=False
        self.wanimindex=0
        self.oanimindex=0 

    def get_hit(self):
        self.hit=True
        self.animindex=0
        phs.play()
        
    def set_anim_state(self, nanim=0, hit=False, ohs=False):
        self.animindex=nanim
        self.hit=hit
        self.overswing=ohs
        self.wanimindex=nanim
        self.oanimindex=nanim

    def calc_move(self, left, right, up, pvel):
        newpvel=pvel
        
        # when going left and not already left, set a timer to say when actually going left
        if left and not self.wanttoflip:
            self.wanttoflip=True
            self.fliptimer=pygame.time.get_ticks()+self.turntime*1000
            
        
        if right and self.wanttoflip:
            self.wanttoflip=False
            self.fliptimer=pygame.time.get_ticks()+self.turntime*1000
            
        if left:
            newpvel[0]=-3
        if right:
            newpvel[0]=3
        if self.wanttoflip and self.fliptimer<pygame.time.get_ticks() and (tertiary(self)):
            
            self.rect.centerx=625
            self.crect.centerx=670
            self.ohswrect.centerx=575
            
            self.flip=True
        if not self.wanttoflip and self.fliptimer < pygame.time.get_ticks() and (tertiary(self)):
            
            self.rect.centerx=640
            self.crect.centerx=650
            self.ohswrect.centerx=740
            
            self.flip=False
        if not left and not right and not self.hit:
            self.animindex=0
        
        if up:
            newpvel[1]=-13
        if self.onground == False:
            up=False
        if pvel[1]<0:
            newpvel[1]+=0.40
        else:
            newpvel[1]+=0.3
        if not left and not right:
            newpvel[0]=0
        
        return newpvel
        
    def move(self, x, y):
        global ba
        self.animindex+=0.3
        
        if self.hit:
            self.animindex-=0.2

            if self.animindex >= 3:
                self.set_anim_state()
                
                ba=False
                return
            
            self.img=pha[int(self.animindex)]
            
            if self.flip: scene.offset[0]-=0.9
            else: scene.offset[0]+=0.9
            return
        
        
        if ba:
            return
        if self.overswing:
            self.oanimindex+=0.4
            if self.oanimindex >12:
                self.oanimindex=0
                self.overswing=False
                self.rect.y+=56
                if self.flip:
                    self.rect.x+=46
            else:
                self.img=pohsa[int(self.oanimindex)]
                scene.offset[1]-=y
                return
        
        
            
        if self.animindex>=8:
            self.animindex=0
        self.img=pwa[int(self.animindex)]
    
        scene.offset[0]-=x
        scene.offset[1]-=y
        
    def collision(self, objects, offset, vel):
        x=vel[0]
        y=vel[1]
        for i in objects:
            
            if self.crect.colliderect((offset[0]+i.rect.x-x, offset[1]+i.rect.y, i.rect.w, i.rect.h)):
                if x > 0:
                    scene.pvel[0]=i.rect.left - self.rect.right+offset[0]
                    x=i.rect.left-self.rect.right+offset[0]
            
                else: 
                    scene.pvel[0]=self.rect.left - i.rect.right-offset[0]
                    x=self.rect.left-i.rect.right-offset[0]
            
            ycollision= self.rect.colliderect((offset[0]+i.rect.x-x, offset[1]+i.rect.y-y, i.rect.w, i.rect.h))
            
            if y>0 and ycollision: 
                y=i.rect.top - self.rect.top
                self.onground=True
                scene.pvel[1]=(i.rect.top+offset[1]) - self.rect.bottom
            if y < 0:
                self.onground=False
                
            if y<0 and ycollision: scene.pvel[1]=self.rect.top - i.rect.bottom+offset[1]
            
            
    def parry(self):
        pass
    
    def dodge(self):
        global ba
        global attacker
        if ba == False: 
            
            ba=True
        else: return
        global react
        react=True
        
        scene.addObject(timerBar(1366/2-5, 50, decision=False, spd=(attacker.agl/self.agl)), False)
    
    
    def checkHit(self, btn):
        global attacklis
        global attacker
        #attack to dodge
        prevhigh=10
        atkr=None


        for i in attacklis:
            if i[2] == 0: return
            if i[1]/i[2] < prevhigh and i[2]>=i[1]:
                atkr=i[0]
                prevhigh=i[1]/i[2]
        if atkr==None and len(attacklis) != 0:
            #MAKE PARRIED, attacker anim checking aint working as well
            atkr.parried=True
            attacklis.pop(attacklis.index(atkr))
            self.get_hit()
        if btn == "g":
            attacker=atkr
            self.dodge()
        
        
    def timer(self, g, h):
        global timeractive
        global timerbar
        global ba
        global selfdraw
        if timeractive:
            timerbar.doShit(self.rect.x, self.rect.y, g, h)
            
            if timerbar.g or timerbar.h or timerbar.nothing:
                
                if timerbar.g:
                    selfdraw.pop(selfdraw.index(timerbar))
                    ba=False
                    decision=timerbar.decision
                    timerbar=False
                    timeractive=False
                    
                    return "g", decision
                if timerbar.h:
                    return "h", timerbar.decision
                
                if timerbar.nothing:
                    
                    self.get_hit()
                
                
                selfdraw.pop(selfdraw.index(timerbar))
                timeractive=False
                ba=False
                timerbar=False
                
                #hit
        return False, False

class timerBar():
    def __init__(self, x, y, decision=True, spd=1):
        self.x=x
        self.y=y
        self.decision=decision
        self.spd=spd
        
        self.barimg=bpimg
        self.markerimg=bmimg
        self.curimg=bcimg
        global timeractive
        global timerbar
        timerbar=self
        timeractive=True
        self.barect=bpimg.get_rect()
        self.markerect=bmimg.get_rect()
        self.curect=bcimg.get_rect()
        
        self.g=False
        self.h=False
        self.nothing=False
        
        selfdraw.append(self)
        # 256 x 64
        
        self.barect.center = (x, y)
        
        self.markerect.center = (x+(randint(-80, 110)), y)
        self.ogmarkerect=self.markerect.center
        self.curect.center = (x-128, y)
        self.markerx=self.curect.x
    def draw(self, screen):
        screen.blit(self.barimg, self.barect)
        if not self.decision:
            screen.blit(self.markerimg, self.markerect)
        screen.blit(self.curimg, self.curect)
    
    def doShit(self, playerx, playery, g, h):
        
        
        self.markerx+=5*self.spd
        self.curect.x=self.markerx
        if (g or h) and not self.curect.colliderect(self.markerect) and not self.decision: 
            self.nothing=True
            return
        if self.curect.colliderect(self.markerect) or self.decision:
            if g: 
                self.g=g
                
            elif h: self.h=h
        if self.curect.x >= self.x+(self.barect.w/2):
            global dt
            self.nothing=True
            dt=60
    

class henemy(entity):
    def __init__(self, stn, hp, agl, skl, x, y, lvl=1, ai="default"):
        super().__init__(stn, hp, agl, skl, lvl=lvl)
        enemies[self]=self
        self.x=x
        self.y=y
        self.img=newimg("/enemy/humanoid1")
        self.iimg=self.img
        self.rect=self.img.get_rect()
        self.rect.center=(x, y)
        self.crect=self.img.get_rect()
        self.crect.width-=70
        self.crect.center=(x-20,y+25)
        self.range=140+(50*(self.lvl/(self.skl**0.4)))
        self.ai=ai
        self.flip=False
        self.wanttoflip=False
        self.fliptimer=0
        self.ohswrect=pygame.Rect(x, y, 90, 70)
        self.ohswrect.center=(x+50,y+25)
        self.animindex=0
        self.swinging=False
        self.parried=False
        # attack list index
        self.ali=-1
        
    def fight(self, player, scroll):
        if ba or self.parried:
            return
        self.crect.center=(int(self.x+scene.offset[0]-15), int(self.y+scene.offset[1]))
        self.ohswrect.center=(self.x+95+scene.offset[0]-15, self.y+25-scene.offset[1])
        
        if self.swinging:
            # 20 times a second.60 frames a second 20/60
            self.animindex+=1
            
            if self.animindex >= 16: 
                self.swinging=False
                self.img=self.iimg
                self.animindex=0
                self.ali=-1
                
            self.img = h1s[int(self.animindex)]
        
        #check if player is near
        
        if abs(self.x-640+scroll[0]) < self.range:
            global attacklis
            if self.ali!=-1: 
                attacklis[self.ali][2] = self.animindex
                print(self.animindex)
                return
            self.ali = len(attacklis)
            attacklis.append([self, 9, self.animindex])
            self.swinging=True
        
        
        if self.ohswrect.colliderect(player.crect):
            if player.hit: return
            global attacker
            attacker=self
            global react
            react=True
            chooseDefence(self, player)
        