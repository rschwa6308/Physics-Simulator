import pygame,sys,os,math
from pygame import *
from pygame.locals import *
from random import *
from Colors import *
from Constants import *
from Body import *


###load assets
##assets = os.path.split(os.path.abspath(__file__))[0]
##assets = os.path.join(assets,"Assets")
##red_circle = pygame.image.load(os.path.join(assets,"red_circle.png"))



def display(screen,bodies):
    #clear last frame
    screen.fill(white)
    #draw bodies
    for body in bodies:
        pygame.draw.ellipse(screen,body.color,body.get_rect())
    #draw text
    screen.blit(tick_text,(s_width-70,0))
    pygame.display.update()




def shift_camera(bodies,x,y):
    for body in bodies:
        body.pos = (body.pos[0]-x,body.pos[1]-y)




def physics(bodies):

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    #start pygame window and init screen
    pygame.init()
    global s_width,s_height
    s_width = 1000
    s_height = 600
    screen = pygame.display.set_mode((s_width,s_height))

    #fonts
    monospace = pygame.font.SysFont("monospace",15)


    #init camera vars
    x_shift = 0
    y_shift = 0


    #set up clock
    clock = pygame.time.Clock()
    tick = 60
    global tick_text
    tick_text = monospace.render(str(tick) + "fps",1,black)
    
    done = False
    while not done:
        clock.tick(tick)

        #user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    tick += 1
                    tick_text = monospace.render(str(tick) + "fps",1,black)
                if event.button == 5 and tick > 1:
                    tick -= 1
                    tick_text = monospace.render(str(tick) + "fps",1,black)
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    y_shift = -1
                elif event.key == K_DOWN:
                    y_shift = 1
                elif event.key == K_LEFT:
                    x_shift = -1
                elif event.key == K_RIGHT:
                    x_shift = 1
            elif event.type == KEYUP:
                if event.key == K_UP:
                    y_shift = 0
                elif event.key == K_DOWN:
                    y_shift = 0
                elif event.key == K_LEFT:
                    x_shift = 0
                elif event.key == K_RIGHT:
                    x_shift = 0
                
        shift_camera(bodies,5*x_shift,5*y_shift)


        #physics engine
        for body in bodies:
            for body_1 in bodies:
                if body_1 != body:
                    #check collisions
                    if body.get_rect().collidepoint(body_1.pos) and body.collision and body_1.collision:
                        print len(bodies)
                        rel = float(body.mass)/(body.mass+body_1.mass)
                        pos = ((body.pos[0]*rel+body_1.pos[0]*(1-rel)),(body.pos[1]*rel+body_1.pos[1]*(1-rel)))
                        #vect = ((body.vect[0]*rel+body_1.vect[0]*(1-rel)),(body.vect[1]*rel+body_1.vect[1]*(1-rel)))
                        x_vect = (body.get_mom()[0]+body_1.get_mom()[0])/(body.mass+body_1.mass)
                        y_vect = (body.get_mom()[1]+body_1.get_mom()[1])/(body.mass+body_1.mass)
                        vect = (x_vect,y_vect)
                        color = ((body.color[0]*rel+body_1.color[0]*(1-rel)),(body.color[1]*rel+body_1.color[1]*(1-rel)),(body.color[2]*(1-rel)+body_1.color[2]*(1-rel)))
                        if max(color) > 255: color = (255,255,255)
                        bodies.remove(body)
                        bodies.remove(body_1)
                        bodies.append(Body(body.mass+body_1.mass,pos,vect,color))
                        break
                        
                    #gravity
                    x = body_1.pos[0]-body.pos[0]
                    y = body_1.pos[1]-body.pos[1]
                    theta = math.atan2(y,x)
                    #print "theta: " + str(theta)
                    #g is measured in units per frame per frame
                    g = (G*body_1.mass)/(x**2+y**2)
                    #print "f: " + str(f)
                    x_acc = math.cos(theta)*g
                    y_acc = math.sin(theta)*g
                    body.vect = (body.vect[0]+x_acc,body.vect[1]+y_acc)


        
            #apply motion
            body.pos = (body.pos[0]+body.vect[0],body.pos[1]+body.vect[1])


        #display room
        display(screen,bodies)



    pygame.quit()
    quit()
    sys.exit(0)








