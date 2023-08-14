import pygame
import pickle
import csv
import characterCreator
import cfg
from time import sleep
#from main import all, Uimenu, buttons, textBoxes, terrain, wn, clock, colors, Scene, Terrain, tButton, button, scenes, text, scene
#MAKE change everything to one global variable file, check cfg

newimg = lambda x: pygame.image.load(f"./img/{x}.png").convert_alpha()
newimgb = lambda x: pygame.image.load(f"./baseImgs/{x}.png").convert_alpha()

font = pygame.font.Font("./data/upheavtt.ttf", 50)

saveSlotImg = newimgb("saveSlot")

# new game button image
ngbi = newimg("NewGameImg")
titleImg = newimg("Title")
turfImg=newimg("Turf")
pIdle = newimg("character/Idle")
#create character bg
ccbg=newimg("ccbg")
ccTxtBar=newimg("ccTxtBar")
leftArrow=newimg("leftArrow")
rightArrow=newimg("rightArrow")
fireicon=newimg("fire")
watericon=newimg("water")
earthicon=newimg("earth")
windicon=newimg("wind")
#start new game button image
sngbi=newimg("StartNewGameButton")

#element icon
eicon=fireicon.get_rect()
eicon.center = (670, 340)






class mainMenu(cfg.Scene):
    def __init__(self):
        menuAppearence(True, True)
        
        self.tir = titleImg.get_rect()
        self.tir.center=(650, 100)
        sleep(0.4)
    def update(self):
        
        cfg.clock.tick(30)
        
    def handleEvent(self, ev):
        if ev.type == pygame.QUIT:
            run=False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                x, y = pygame.mouse.get_pos()
                for i in cfg.buttons:
                    if i.rect.collidepoint(x, y):
                        
                        cfg.Uimenu.clear()
                        cfg.terrain.clear()
                        cfg.textBoxes.clear()
                        cfg.buttons.clear()
                        i.onClick()              
                        break    
        
    def draw(self):
        pygame.display.flip()
        cfg.wn.fill((80, 250, 80))
        
        for i in cfg.terrain:
            cfg.wn.blit(i.img, i.rect)
            
        
        cfg.wn.blit(titleImg, self.tir)
        for i in cfg.Uimenu:
            cfg.wn.blit(i.img, i.rect)
    
    
        

class createCharacter(cfg.Scene):
    def __init__(self):
        cfg.clock.tick(30)
        self.displaystart=False
        self.elements=[]
        self.tele=[]
        sleep(0.5)
        # strength, skill, agility, health, bar, rect
        self.stbr = ccTxtBar.get_rect()
        self.skbr = ccTxtBar.get_rect()
        self.agbr = ccTxtBar.get_rect()
        self.hpbr = ccTxtBar.get_rect()
        self.stbr.center = (320, 155)
        self.skbr.center = (1000, 155)
        self.agbr.center = (320, 550)
        self.hpbr.center = (1000, 550)
        self.elements.append(self.stbr)
        self.elements.append(self.skbr)
        self.elements.append(self.agbr)
        self.elements.append(self.hpbr)
        self.bg = pygame.transform.scale(ccbg, (1366, 768))
        self.bgr=self.bg.get_rect()
        self.bgr.x=0
        self.bgr.y=0
        self.str=1
        self.skill=1
        self.agility=1
        self.health=1
        self.statpoints=35
        self.decstr = cfg.button(483, 180, 48, 48, leftArrow, self.changestat, ["str", "dec"])
        self.incstr = cfg.button(543, 180, 48, 48, rightArrow, self.changestat, ["str", "inc"])
        self.decskill = cfg.button(1163, 180, 48, 48, leftArrow, self.changestat, ["skill", "dec"])
        self.incskill = cfg.button(1223, 180, 48, 48, rightArrow, self.changestat, ["skill", "inc"])
        self.decagility = cfg.button(483, 575, 48, 48, leftArrow, self.changestat, ["agility", "dec"])
        self.incagility = cfg.button(543, 575, 48, 48, rightArrow, self.changestat, ["agility", "inc"])
        self.dechealth = cfg.button(1163, 575, 48, 48, leftArrow, self.changestat, ["health", "dec"])
        self.inchealth = cfg.button(1223, 575, 48, 48, rightArrow, self.changestat, ["health", "inc"])
        self.sngb = cfg.button(760, 600, 192, 96, sngbi, self.create, [], custom=True)
        
        
        #stat descriptions
        self.strdesc = cfg.text(95, 200, ["Strength is a measure of damage, associated", "with fire", "Base damage: 3", "+0.05 base strength per point", r"+2% strength per point"], 20, cfg.colors["white"])
        self.healthdesc = cfg.text(780, 410, ["Health is a measure of how much damage one can", "take, associated with earth", "Base health: 10", "+0.2 base health per point (rounded down)", r"+3% health per point"], 20, cfg.colors["white"])
        self.agilitydesc = cfg.text(95, 390, ["Agility is a measure of how easily one can move", "and dodge,", "associated with water", "Base agility: 5", "+0.1 base agility per point (rounded down)", r"+4% agility per point"], 20, cfg.colors["white"])
        self.skilldesc = cfg.text(780, 200, ["Skill is a measure of how easily one can wield", "their weapon,", "associated with air", "Base skill: 5", "+0.1 base skill per point (rounded down)", r"+4% skill per point", "-allows for easier combos"], 20, cfg.colors["white"])
        self.tele.append(self.strdesc)
        self.tele.append(self.healthdesc)
        self.tele.append(self.agilitydesc)
        self.tele.append(self.skilldesc)
        
        
    def create(self):
        with open("./data/save1/charsheet.info", "wb") as cs:
            stats=[self.str*4+32, self.health*4+32, self.agility*4+32, self.skill*4+32]
            pickledstats=pickle.dump(stats, cs)
            #cs.write(pickledstats)
            cfg.scene="switchtomaingame"
        
        
    def changestat(self, arg):
        
        modifier= 0
        if arg[1] == "inc": 
            modifier = 1
            if self.statpoints == 0: return
        else: 
            if self.statpoints==35:
                return
            modifier = -1
            self.statpoints+=2
        
        if arg[0] == "str": self.str+=modifier
        if arg[0] == "skill": self.skill+=modifier
        if arg[0] == "agility": self.agility+=modifier
        if arg[0] == "health": self.health+=modifier
        self.statpoints-=1
        if self.str < 1: 
            self.str=1
            self.statpoints+=1
        if self.agility < 1: 
            self.agility=1
            self.statpoints+=1
        if self.skill < 1: 
            self.skill=1
            self.statpoints+=1
        if self.health < 1: 
            self.health=1
            self.statpoints+=1
        return
    
    def handleEvent(self, ev):
        if ev.type == pygame.QUIT:
            run=False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                run=False
                
                cfg.Uimenu.clear()
                cfg.terrain.clear()
                cfg.textBoxes.clear()
                cfg.buttons.clear()
                global scene
                cfg.scene=cfg.scenes["selectSave"]()
                
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                x, y = pygame.mouse.get_pos()
                if self.canstart:
                    if self.sngb.rect.collidepoint(x, y):
                        self.sngb.onClick()
                for i in cfg.buttons:
                    if i.rect.collidepoint(x, y):
                        i.onClick()           
    
    def update(self):
        self.strtxt = cfg.text(110, 130, [f"Strength: {self.str}"], 35, (230, 230, 230))
        self.skilltxt = cfg.text(790, 130, [f"Skill: {self.skill}"], 35, (230, 230, 230))
        self.strtxt = cfg.text(110, 525, [f"Agility: {self.agility}"], 35, (230, 230, 230))
        self.skilltxt = cfg.text(790, 525, [f"Health: {self.health}"], 35, (230, 230, 230))
        self.pointsleft = cfg.text(460, 50, [f"Points Left: {self.statpoints}"], 50, (230, 230, 230))
        
        temp={self.str: "str", self.skill:"skill", self.agility:"agility", self.health:"health"}
        
        maxv = max(self.str, self.skill, self.agility, self.health)
        self.maxv=maxv
        self.p=[self.str, self.skill, self.agility, self.health]
        self.p.sort()
        if self.p[-1] == self.p[-2]:
            self.canstart=False
        else: self.canstart=True
    
    def draw(self):
        
        pygame.display.flip()
        
        cfg.wn.blit(self.bg, self.bgr)
        
        if self.agility==self.maxv:
            cfg.wn.blit(watericon, eicon)
        if self.skill == self.maxv:
            cfg.wn.blit(windicon, eicon)
        if self.health == self.maxv:
            cfg.wn.blit(earthicon, eicon)
        if self.str==self.maxv:
            cfg.wn.blit(fireicon, eicon)
        if self.canstart:
            cfg.wn.blit(sngbi, self.sngb)    

        for i in self.elements:
            cfg.wn.blit(ccTxtBar, i)
        for i in cfg.terrain:
            cfg.wn.blit(i.img, i.rect)
            
        for i in cfg.Uimenu:
            cfg.wn.blit(i.img, i.rect)
        
        
        for i in self.tele:
            for line in range(len(i.text)):
                cfg.wn.blit(i.text[line], i.rects[line])
        for i in cfg.textBoxes:
            for line in range(len(i.text)):
                cfg.wn.blit(i.text[line], i.rects[line])
                
        cfg.textBoxes.clear()




class selectSave(cfg.Scene):
    def __init__(self):
        
        #save slot 1 char img
        try:
            self.ss1ci = pygame.image.load("./data/save1/charf.png").convert_alpha()
            
            self.ss1cir = self.ss1ci.get_rect()
            self.ss1cir.center = (340, 270)
        
            self.ss2ci = pygame.image.load("./data/save1/charf.png").convert_alpha()
            self.ss2cir = self.ss1ci.get_rect()
            self.ss2cir.center = (200, 300)
            self.ss3ci = pygame.image.load("./data/save1/charf.png").convert_alpha()
            self.ss3cir = self.ss1ci.get_rect()
            self.ss3cir.center = (200, 300)
            
        except: pass
        #save slot 1 ino
        ss1i=loadSaveSlotBasicInfo(1)
        if ss1i != "" and ss1i != None:
            #ss1t
            ss1t = cfg.text(250, 340, [f"Lvl: {ss1i[3]}", f"Type: {ss1i[4]}"], 30)
            saveSlot1 = cfg.button(450, 500, 240, 360, saveSlotImg, loadSaveSlotBasicInfo, arg=[1])
        else:
            saveSlot1 = cfg.tButton(450, 500, 240, 360, saveSlotImg, "createCharacter")
            

    def handleEvent(self,ev):
        
    
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                
                
                cfg.Uimenu.clear()
                cfg.terrain.clear()
                cfg.textBoxes.clear()
                cfg.buttons.clear()
                pygame.quit()
                exit()
                
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                x, y = pygame.mouse.get_pos()
                for i in cfg.buttons:
                    if i.rect.collidepoint(x, y):
                        cfg.Uimenu.clear()
                        cfg.terrain.clear()
                        cfg.textBoxes.clear()
                        cfg.buttons.clear()
                        i.onClick()              
                        break      
    
    def draw(self):
        pygame.display.flip()
        cfg.wn.fill((90, 100, 200))
        
        
        for i in cfg.terrain:
            cfg.wn.blit(i.img, i.rect)
            
        for i in cfg.Uimenu:
            cfg.wn.blit(i.img, i.rect)
        for i in cfg.textBoxes:
            for line in range(len(i.text)):
                cfg.wn.blit(i.text[line], i.rects[line], special_flags=pygame.BLEND_RGBA_MULT)
        try:
            cfg.wn.blit(self.ss1ci, self.ss1cir)
        except Exception as e:
            print(e)
    
    def update(self):
        
        cfg.clock.tick(30)
        
        




#scenes = {"selectSave": selectSave, "mainMenu": mainMenu, "createCharacter": createCharacter}
cfg.scenes["selectSave"] = selectSave
cfg.scenes["mainMenu"] = mainMenu
cfg.scenes["createCharacter"] = createCharacter
def test():
    print("tester")

    

def loadSaveSlotBasicInfo(slot):
    # arg[0] = 
    # 1. Which save 1-3
    # that save will have all further instructions in order to minimise clutter on this file
    with open(f"./data/save{slot}/progress.info", "r") as basicInfo:
        charsheet_csv = csv.reader(basicInfo, delimiter=",")
        for row in charsheet_csv:
            
            
            if row [0] == False:
                return False
            characterCreator.create(cfg.colors[row[0]], cfg.colors[row[1]], cfg.colors[row[2]], 1)
            return row


def menuAppearence(Buttons, bg):
    if bg:
        for x in range(20):
            for y in range(10):
                p=cfg.Terrain(x*128, y*128, turfImg, collision = False)
    #new game button
    if Buttons:
        ngb = cfg.tButton(750, 300, 192, 96, ngbi, "selectSave")

cfg.scene = cfg.scenes["mainMenu"]()

    
    
    