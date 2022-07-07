import pycxsimulator
from pylab import *

"""
state 0 = recuperandose negro
state 1 = sano naranja
state 2 = enfermo blanco
"""
width = 100
height = 100
initProb = 0.1
infectionRate = 0.85
regrowthRate = 0.15
efectividad=0.23#entre más pequeño sea este valor, se supone una efectividad mayor de la vacuna
vaccine=zeros([height, width])

def initialize():
    global time, config, nextConfig

    time = 0
    
    config = zeros([height, width])

    for x in range(width):
        for y in range(height):
            if random() < initProb:
                state = 2 #enfermo/blanco
            else:
                state = 1 #sano/naranja
            config[y, x] = state

    nextConfig = zeros([height, width])


def observe():
    cla()
    imshow(config, vmin = 0, vmax = 2, cmap = cm.hot)
    axis('image')
    title('t = ' + str(time))

def update():
    global time, config, nextConfig

    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            if state == 0:#recuperandose/negro
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if vaccine[y,x]==1:
                            if config[(y+dy)%height, (x+dx)%width] == 1:#sano/naranja
                                if random() < (regrowthRate* efectividad):#random representa la susceptibilidad de la celula de infectarse
                                    state = 1#sano/naranja                    
                        else:
                            if config[(y+dy)%height, (x+dx)%width] == 1:#sano/naranja
                                if random()< regrowthRate:
                                    state = 1#sano/naranja
                                    vaccine[y,x]=1
            elif state == 1:  #sano/naranja
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if vaccine[y,x]==1:    
                            if config[(y+dy)%height, (x+dx)%width] == 2:#enfermo/blanco
                                if random() < (infectionRate*efectividad): 
                                    state = 2#enfermo/blanco
                        else:
                           if config[(y+dy)%height, (x+dx)%width] == 2:#enfermo/blanco
                                if random() < (infectionRate):                     
                                    state = 2#enfermo/blanco 
                                    vaccine[y,x]=1
            else:#enfermo/blanco
                state = 0 #recuperandose/negro

            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config

pycxsimulator.GUI().start(func=[initialize, observe, update])