import pygame
import os


def loadimage(name):
    img = pygame.image.load(name)
    return img

def scaleimage(name,x,y):
    scaledimg = pygame.transform.scale(name,(x,y))
    return scaledimg

def displayimage(display,name,x,y):
    display.blit(name,(x,y))

def displaytext(display,text,x,y,size,color,bold,italic):
    font = pygame.font.SysFont(None,size,bold,italic)
    text = font.render(text,True,color)
    display.blit(text,(x,y))

def listallthefiles(name):
    dir = os.listdir(name)
    images = []
    for i in range(len(dir)):
        images.append(pygame.image.load(f"{name}/{dir[i]}"))        
    return images

def playmusic(name):
    pygame.mixer.music.load(name)
    pygame.mixer.music.play()