import pygame
import pickle
import csv
import cfg


#str, health, agility, skill
floorboard=cfg.newimg("floorboard")
brickbg=cfg.newimg("brickbgbig")
            
class startingArea(cfg.Scene):
    def __init__(self, refreshrate=3):
        global player
        cfg.cs = self.loadStats()
        player=cfg.player_class(cfg.cs[0], cfg.cs[1], cfg.cs[2], cfg.cs[3])
        self.left=False
        self.right=False
        self.up=False
        self.h=False
        self.g=False
        self.offset=[0, 21]
        self.all=[]
        self.drawable=[]
        self.bg=[]
        self.refreshrate=refreshrate
        self.currefresh=1
        self.pvel=[0,0]
        self.collision=[]
        self.timerbar=False
        for i in range(30):
            p=cfg.Terrain(i*224-320, 773,floorboard, True)
            self.all.append(p)
        self.bg=brickbg
        self.bgrect=self.bg.get_rect()
        
        
        
        self.addObject(cfg.henemy(15, 15, 15, 15, 200, 478), True)
    
    def addObject(self, obj, drawable):
        if drawable:
            self.drawable.append(obj)
            return
        if type(obj)==cfg.henemy:
            cfg.enemies.append(obj)
        if type(obj) == cfg.timerBar:
            self.timerbar=obj
    
    def loadStats(self):
        with open("./data/save1/charsheet.info", "rb") as cs:
            unpickledstats=pickle.load(cs)
            stats=[]
            for i in unpickledstats:
                stats.append((i-32)/4)
            return stats
    
    def handleEvent(self, ev):        
        if ev.type == pygame.KEYDOWN:
            if ev.key==pygame.K_j and cfg.tertiary(player):
                player.overswing=True
                player.rect.y-=56
                if player.flip:
                    player.rect.x-=46
            if ev.key == pygame.K_LEFT:
                self.left=True
            if ev.key==pygame.K_RIGHT:
                self.right=True
            if ev.key == pygame.K_UP and player.onground:
                self.up=True
            if ev.key==pygame.K_h:
                self.h=True
            if ev.key==pygame.K_g:
                self.g=True
                
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT:
                self.left=False
            if ev.key == pygame.K_RIGHT:
                self.right=False
            if ev.key==pygame.K_h:
                self.h=False
            if ev.key==pygame.K_g:
                self.g=False
            
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    def update(self):
        
        self.pvel=player.calc_move(self.left, self.right, self.up, self.pvel)
        player.collision(self.collision, self.offset, self.pvel)
        player.move(self.pvel[0], 0)
        if self.g and not cfg.ba: 
            player.checkHit("g")
            self.g=False
        elif self.h and not cfg.ba:
            player.checkHit("h")
            self.h=False
        
        
        
        check, decision = player.timer(self.g, self.h)
        check, decision = False, False
        if check == "g":
            
            if decision: player.dodge()
            else:
                if player.rect.x < cfg.attacker.rect.x-self.offset[0]:
                    self.offset[0]-=300
                else:
                    self.offset[0]+=300
        
            
        if self.currefresh==self.refreshrate:
            self.drawable=[]
            self.collision=[]
            for i in self.all:
                if i.rect.right+self.offset[0] > -10 and i.rect.left+self.offset[0] < 1376 and i.rect.top+self.offset[1] < 776 and i.rect.bottom+self.offset[1] > -10:
                    self.drawable.append(i)
                    self.collision.append(i)
            for i in cfg.enemies:
                if i.rect.right+self.offset[0] > -10 and i.rect.left+self.offset[0] < 1376 and i.rect.top+self.offset[1] < 776 and i.rect.bottom+self.offset[1] > -10:
                    i.fight(player, self.offset)
                    self.drawable.append(i)
                    
            self.currefresh=1
        else:
            self.currefresh+=1
            
        self.g=False
        self.h=False
        
        cfg.clock.tick(cfg.dt)
    
    def draw(self):
        cfg.wn.blit(self.bg, self.bgrect)
        for i in cfg.enemies:
            pygame.draw.rect(cfg.wn, (255, 0, 255), [j for j in cfg.enemies][0].ohswrect)
            pygame.draw.rect(cfg.wn, (255, 0, 0), [j for j in cfg.enemies][0].crect)
            
        pygame.draw.rect(cfg.wn, (255, 255, 0), player.crect)
        pygame.draw.rect(cfg.wn, (0, 255, 0), player.ohswrect)
        for i in self.drawable:
            cfg.wn.blit(i.img, (int(i.rect.x + self.offset[0]), i.rect.y+self.offset[1], i.rect.w, i.rect.h))
        for i in cfg.selfdraw:
            i.draw(cfg.wn)
        
            
            
        cfg.wn.blit(pygame.transform.flip(player.img, player.flip, False), player.rect)
        
        pygame.display.flip()
        cfg.wn.fill((255, 255, 255))

import mainmenu
cfg.scenes["startingArea"] = startingArea

def main():
    
    run=True
    
    while run:
        if cfg.scene == "switchtomaingame":
            cfg.scene=cfg.scenes["startingArea"]()
            
            
        cfg.scene.update()
        cfg.scene.draw()
        
        for ev in pygame.event.get():
            cfg.scene.handleEvent(ev)
            
main()