import pygame
import sys  # to exit the game
import random
import os
from assets.resources.functions import displayimage,displaytext,loadimage,scaleimage,playmusic,listallthefiles # some custom functions
from co_ordinates import co_ordinates

pygame.init()

# checking whether the data.txt file exist or not
allthedir = os.listdir("assets/resources")
if not allthedir.__contains__("data.txt"):
    data = open("assets/resources/data.txt","a")
    data.write("0")
    data.close()



width = 600
height = 600

display = pygame.display.set_mode((width,height))

# loading all the stuffs
player = scaleimage(loadimage("assets/asteroid/player.png"),80,80)

bigasteriod = loadimage("assets/asteroid/alienship.png")
mediumasteriod = loadimage("assets/asteroid/asteroid100.png")
smallasteriod = loadimage("assets/asteroid/asteroid50.png")
background = scaleimage(loadimage("assets/asteroid/starbg.png"),width,height)
playimage = scaleimage(loadimage("assets/gui/Play (1).png"),100,100)
exitimage = scaleimage(loadimage("assets/gui/Exit (1).png"),100,100)
homeimage = scaleimage(loadimage("assets/gui/Home (1).png"),100,100)
restartimage = scaleimage(loadimage("assets/gui/Reload (1).png"),100,100)

clock = pygame.time.Clock()
fps = 90


def gameloop():

    playerx = width/2-player.get_width()/2
    playery = height/2-player.get_height()/2
    playerxspeed = 0
    playeryspeed = -3
    rotationalangle = 0
    bulletlist = []
    asteroidlist = []
    score = 0
    life = 3

    while True:
        try:
            # handling when the player get outs of the canvas
            if playerx<-(0+player.get_width()):
                playerx=width
                
            elif playerx>width:
                playerx=-(0+player.get_width())

            elif playery<-(0+player.get_height()):
                playery=height

            elif playery>height:
                playery=-(0+player.get_height())
            

            # handling the events8
            keys = pygame.key.get_pressed()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                
                if keys[pygame.K_a]:
                    if rotationalangle>360 or rotationalangle<-360 or rotationalangle==360 or rotationalangle==-360:
                        rotationalangle=0
                    rotationalangle+=3
                if keys[pygame.K_d]:
                    if rotationalangle>360 or rotationalangle<-360 or rotationalangle==360 or rotationalangle==-360:
                        rotationalangle=0
                    rotationalangle-=3
                if keys[pygame.K_w]:
                    if not keys[pygame.K_a] and not keys[pygame.K_d]:
                        if rotationalangle>360 or rotationalangle<-360 or rotationalangle==360 or rotationalangle==-360:
                            rotationalangle=0
                        playerxspeed,playeryspeed = getxandy(rotationalangle)
                        playerx+=playerxspeed
                        playery+=playeryspeed
                
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        if len(bulletlist)<6:
                            playmusic("assets/sounds/shoot.wav")
                            bulletspeedx,bulletspeedy = getxandy(rotationalangle)
                            obj = {
                                "bulletx":playerx+player.get_width()/2,
                                "bullety":playery+player.get_height()/2,
                                "bulletspeedx":bulletspeedx,
                                "bulletspeedy":bulletspeedy
                            }
                            bulletlist.append(obj)

            if not keys[pygame.K_w]:
                playerx+=playerxspeed/7
                playery+=playeryspeed/7

            display.fill("black")

            # displaying moving the bullets
            for index,data in enumerate(bulletlist):
                bulletx = data["bulletx"]
                bullety = data["bullety"]
                pygame.draw.circle(display,"red",(data["bulletx"],data["bullety"]),5)
                bulletlist[index].update({
                    "bulletx":bulletx+data["bulletspeedx"],
                    "bullety":bullety+data["bulletspeedy"]
                })
                if bulletx<-10 or bulletx>width or bullety<-10 or bullety>height:
                    bulletlist.remove(bulletlist[index])
                    break
            
            # displaying the player
            displayimage(display,pygame.transform.rotate(player,rotationalangle),playerx,playery)

            # spawing the asteroid over here
            if len(asteroidlist)<6:
                asteroidlist = spawntheasteriod(asteroidlist)
            
            for index,data in enumerate(asteroidlist):
                asteroid = data["name"]
                level = data["level"]
                asteroidx=data["asteroidx"]
                asteroidy=data["asteroidy"]
                asteroidspeedx=data["asteroidspeedx"]
                asteroidspeedy=data["asteroidspeedy"]
                if playerx>asteroidx and playerx<asteroidx+asteroid.get_width() and playery>asteroidy and playery<asteroidy+asteroid.get_height():
                    if life>0:
                        life-=1
                        playerx+=100
                        playery+=100
                    if life <1:
                        scorescreen(score)
                for index2,data2 in enumerate(bulletlist):
                    bulletx = data2["bulletx"]
                    bullety = data2["bullety"]
                    if bulletx>asteroidx and bulletx<asteroidx+asteroid.get_width() and bullety>asteroidy and bullety<asteroidy+asteroid.get_height():
                        bulletlist.remove(bulletlist[index2])
                        asteroidlist.remove(asteroidlist[index])
                        if level == "small":
                            playmusic("assets/sounds/bangsmall.wav")
                        if level == "medium":
                            for i in range(2):
                                asteroidlist.append({
                                    "name":smallasteriod,
                                    "level":"small",
                                    "asteroidx":asteroidx,
                                    "asteroidy":asteroidy,
                                    "asteroidspeedx":.5 if random.randint(0,1)==0 else -.5,
                                    "asteroidspeedy":.5 if random.randint(0,1)==0 else -.5
                                })
                            playmusic("assets/sounds/bangSmall.wav")
                        if level == "big":
                            asteroidlist.append({
                                    "name":mediumasteriod,
                                    "level":"medium",
                                    "asteroidx":asteroidx,
                                    "asteroidy":asteroidy,
                                    "asteroidspeedx":.5 if random.randint(0,1)==0 else -.5,
                                    "asteroidspeedy":.5 if random.randint(0,1)==0 else -.5
                                })
                            playmusic("assets/sounds/bangLarge.wav")
                        score+=1




            for index,data in enumerate(asteroidlist):
                    
                asteroid = data["name"]
                level=data["level"]
                asteroidx=data["asteroidx"]
                asteroidy=data["asteroidy"]
                asteroidspeedx=data["asteroidspeedx"]
                asteroidspeedy=data["asteroidspeedy"]
                displayimage(display,asteroid,asteroidx,asteroidy)

                if asteroidx<-100 or asteroidx>width+100 or asteroidy<-100 or asteroidy>height+100:
                    asteroidlist.remove(asteroidlist[index])
                    break

                asteroidlist[index].update({
                    "asteroidx":asteroidx+asteroidspeedx,
                    "asteroidy":asteroidy+asteroidspeedy
                })   

            pygame.draw.circle(display,"red",(playerx+player.get_width()/2,playery+player.get_height()/2),5)

            displaytext(display,f"Score :- {score}",0,0,50,"red",True,True)
            displaytext(display,f"Life : {life}",width-150,0,50,"white",True,True)

            pygame.display.update()

            clock.tick(fps)
        except Exception as e:
            print("Hey some error occurred! 🟠")
                


def getxandy(angle):
    try:
        return co_ordinates[angle]
    except Exception as e:
        print("Hey some error occurred! 🟠")

def spawntheasteriod(asteroidlist):
    try:
        # rondomly taking an asteroid
        name = smallasteriod
        level = ""

        choice = random.randint(0,2)

        '''
        0 - small
        1 - medium
        2 - big
        '''

        if choice == 0:
            name = smallasteriod
            level = "small"
            
        elif choice == 1:
            name = mediumasteriod
            level = "medium"

        elif choice == 2:
            name = bigasteriod
            level = "big"
        

        # choicing the direction
        direction = random.randint(1,3)
        randomx = random.randint(0,width)
        randomy = random.randint(0,height)
        newx = 0
        newy = 0
        if direction == 1:
            newx = -name.get_width()
            newy = randomy
        elif direction == 2:
            newx = randomx
            newy = -name.get_height()
        else:
            newx = width+name.get_width()
            newy = randomx
        

        newspeedx = 0.4 if random.randint(0,1) == 0 else -0.4
        newspeedy = 0.4 if random.randint(0,1) == 0 else -0.4


        obj = {
            "name":name,
            "level":level,
            "asteroidx":newx,
            "asteroidy":newy,
            "asteroidspeedx":newspeedx,
            "asteroidspeedy":newspeedy
        }

        asteroidlist.append(obj)
        return asteroidlist
    except Exception as e:
        print("Hey some error occurred! 🟠")
    

def homescreen():
    while True:
        try:
            if not pygame.mixer.music.get_busy():
                playmusic("assets/sounds/home.mp3")
                pygame.mixer.music.set_volume(.1)
            for e in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if e.type == pygame.QUIT:
                    sys.exit()
                
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        gameloop()
                
                if pygame.mouse.get_pressed()[0]:
                    mousex = pos[0]
                    mousey = pos[1]
                    if mousex>width/2-playimage.get_width()/2 and mousex<width/2-playimage.get_width()/2+playimage.get_width() and mousey>200 and mousey<200+playimage.get_height():
                        gameloop()
                    if mousex>width/2-exitimage.get_width()/2 and mousex<width/2-exitimage.get_width()/2+exitimage.get_width() and mousey>360 and mousey<360+playimage.get_height():
                        sys.exit()
                

            display.fill("black")
            displayimage(display,background,0,0)
            displayimage(display,player,30,10)
            displaytext(display,"And",110,30,60,"white",False,False)
            displayimage(display,bigasteriod,200,10)
            displaytext(display,"Shooter",400,30,60,"white",False,False)

            displayimage(display,playimage,width/2-playimage.get_width()/2,200)
            displayimage(display,exitimage,width/2-exitimage.get_width()/2,360)

            pygame.display.update()
        except Exception as e:
            print("Hey some error occurred! 🟠")

def scorescreen(score):
    # checking about hight score
    showhighscore = False
    data = open("assets/resources/data.txt","r")
    initialhighscore = int(data.readline())
    data.close()
    if score>initialhighscore:
        data = open("assets/resources/data.txt","w")
        data.write(str(score))
        data.close()
        showhighscore=True
    while True:
        try:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    mousex = pos[0]
                    mousey = pos[1]
                    if mousex>100 and mousex<100+restartimage.get_width() and mousey>310 and mousey<310+restartimage.get_height():
                            gameloop()
                    if mousex>width/2-homeimage.get_width()/2 and mousex<width/2-playimage.get_width()/2+homeimage.get_width() and mousey>310 and mousey<310+homeimage.get_height():
                            homescreen()
                    if mousex>400 and mousex<400+exitimage.get_width() and mousey>310 and mousey<310+exitimage.get_height():
                            sys.exit()
            display.fill((103, 58, 0))
            displaytext(display,f"Score :- {score}",200,100,50,"black",True,True)
            if showhighscore:
                displaytext(display,"Hight Score",200,140,50,"black",True,True)
                
            displayimage(display,restartimage,100,310)
            displayimage(display,homeimage,width/2-playimage.get_width()/2,310)
            displayimage(display,exitimage,400,310)

            pygame.display.update()
        except Exception as e:
            print("Hey some error occurred! 🟠")
            



# running the game
# enjoy it 😎
homescreen()
    




