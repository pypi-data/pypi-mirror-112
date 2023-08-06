import sys,time,math,pygame,re,os
from pygame.locals import *
cd=os.path.dirname(os.path.abspath(__file__))
FPS=30
ROWNUM=4
WINWIDTH = 600
WINHEIGHT=800
IMAGESIZE=46
BLACK=(0,0,0)
DARKGRAY=(70,70,70)
BRIGHTBLUE=(0,170,255)
WHITE=(255,255,255)

class Skill:
    
    def __init__(self,name,level=0,pre=[]):
        self.name=name
        self.level=level
        self.pre=pre
        self.rank=1

    def setName(self,name):
        self.name=name

    def setLevel(self,level=0):
        self.level=level

    def addPre(self,pre):
        if isinstance(pre,list):
            for each in pre:
                self.pre.append(each)
        else:
            self.pre.append(pre)

    def setPos(self,N_x,N_y,x,y):
        self.N_x=N_x
        self.N_y=N_y
        self.x=x
        self.y=y
        
    def drawImage(self):
        DISPLAYSURF.blit(LEVEL[self.level],(self.x,self.y))
        self.textSurf=FONT.render(self.name,True,BLACK)
        self.textRect=self.textSurf.get_rect()
        self.textRect.center=(self.x+IMAGESIZE/2,self.y+IMAGESIZE+5)
        DISPLAYSURF.blit(self.textSurf,self.textRect)
        self.levelSurf=FONT.render(str(self.level),True,BLACK)
        self.levelRect=self.levelSurf.get_rect()
        self.levelRect.center=(self.x+IMAGESIZE/2,self.y+IMAGESIZE/2)
        DISPLAYSURF.blit(self.levelSurf,self.levelRect)
        self.rect=pygame.Rect(self.x,self.y,IMAGESIZE,IMAGESIZE)

def main():
    global FPSCLOCK,DISPLAYSURF,LEVEL,FONT
    pygame.init()
    DISPLAYSURF=pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    FPSCLOCK=pygame.time.Clock()
    FONT=pygame.font.SysFont('simhei',16)
    pygame.display.set_caption('Skill Tree')
    mousex=0
    mousey=0
    '''
    L1=pygame.image.load('img\L1.png')  # beginner level
    L2=pygame.image.load('img\L2.png')  # fair level
    L3=pygame.image.load('img\L3.png')  # good level
    L4=pygame.image.load('img\L4.png')  # excelent level
    L5=pygame.image.load('img\L5.png')  # master level
    L0=pygame.image.load('img\L0.png')  # not available
    '''
    LEVEL=[pygame.transform.smoothscale(pygame.image.load(cd+'\img\L%s.png' % i),(IMAGESIZE,IMAGESIZE)) for i in range(6)]
    LEVELDISC=['not available','beginner','fair','good','excelent','master']
    #for each in skills:
        
    
    while True:
        DISPLAYSURF.fill(WHITE)
        drawImages(skills)
        checkForQuit()
        
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                for each in skills:
                    if each.rect.collidepoint((mousex,mousey)):
                        if event.button in [1,4]:
                            if 0<=each.level<5:
                                each.level+=1
                            elif each.level==5:
                                each.level=1
                        elif event.button in [3,5]:
                            if 1<=each.level<6:
                                each.level-=1
                            elif each.level==1:
                                each.level=5
                        elif event.button==2:
                            textSurf=[]
                            textRect=[]
                            textSurf.append(FONT.render(each.name+' 需要 : ',True,BLACK))
                            textRect.append((0.7*xGap,WINHEIGHT-1.2*yGap))
                            rect=textSurf[-1].get_rect()
                            n=0
                            for i in each.pre:
                                textSurf.append(FONT.render(i[0]+'>='+str(i[1]),True,BLACK))
                                textRect.append((0.7*xGap+rect[2],WINHEIGHT-1.2*yGap+n*20))
                                n+=1
                        resetAva(skills)
                        drawImages(skills)
                #print(mousex,mousey)
        if 'textSurf' in locals():
            for i,j in zip(textSurf,textRect):
                DISPLAYSURF.blit(i,j)
        pygame.display.update()
        FPSCLOCK.tick(FPS)  

def qsave():
    with open(cd+"\points.txt",'w',encoding='utf-8') as f:
        for each in skills:
            f.write(each.name+':'+str(each.level)+'\n')
    
def checkForQuit():
    for event in pygame.event.get(QUIT):
        qsave()
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key==K_ESCAPE:
            qsave()
            pygame.quit()
            sys.exit()
        pygame.event.post(event)

def drawImages(skill):
    for each in skills:
        each.drawImage()

        

def positSkill(m):
    global xGap,yGap
    n=len(skills)
    xGap=WINWIDTH//(m+1)
    yGap=WINHEIGHT//(n//m+1+1)
    n_x=1
    n_y=1
    for each in skills:
        x=(n_x-0.3)*xGap
        y=(n_y-0.5)*yGap
        each.setPos(n_x,n_y,x,y)
        n_x+=1
        if n_x>m:
            n_x=1
            n_y+=1

def preGenerator(raw):
    preg=[]
    raw=raw.split(',')
    for i in range(0,len(raw),2):
        preg.append([raw[i],int(raw[i+1])])
    return preg

def checkAvailable(skil):
    for each in skil.pre:
        for ite in skills:
            if ite.name==each[0] and ite.level<each[1]:
                return 0
    return 1

def resetAva(skills):
    for each in skills:
        result=checkAvailable(each)
        if result==0:
            each.setLevel(0)
        elif each.level==0:
            each.setLevel(1)

def init():
    with open(cd+'\points.txt','r',encoding='utf-8') as f:
        for line in f.readlines():
            matchObj=re.match(r'(.*):(.*)\n',line,re.M|re.I)
            for each in skills:
                if each.name==matchObj.group(1):
                    each.level=int(matchObj.group(2))




global skills
skills=[]

with open(cd+'\skills.txt',encoding='utf-8') as f:
    for line in f.readlines():
        #print(line)
        if ":" not in line:
            skills.append(Skill(line.strip('\n')))
        else:
            matchObj=re.match(r'(.*):(.*)\n',line,re.M|re.I)
            skills.append(Skill(matchObj.group(1),pre=preGenerator(matchObj.group(2))))     

init()

resetAva(skills)
positSkill(ROWNUM)

'''
for each in skills:
    print(each.name,end=' : ')
    print(each.level,end=' : ')
    print(each.pre)
    '''
main()
