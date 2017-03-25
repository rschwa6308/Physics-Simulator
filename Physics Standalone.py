import pygame,sys,os,math
from pygame import *
from pygame.locals import *
from random import *
from Colors import *
from Constants import *




def display(screen,bodies):
    #clear last frame
    screen.fill(white)
    #draw bodies
    for body in bodies:
        pygame.draw.ellipse(screen,body.color,body.get_rect())
    #draw text
    screen.blit(tick_text,(s_width-70,0))
    pygame.display.update()




def shift_camera(x,y):
    for body in bodies:
        body.pos = (body.pos[0]-x,body.pos[1]-y)




class Body():
    def __init__(self,mass,pos,vect,color,rad=-1,collision=True):
        self.mass = mass
        self.pos = pos
        self.vect = vect
        self.color = color
        if rad == -1:
            #body size scaling (2 => 2D (area); 3 => 3D (volume))
            D = 3
            self.rad = float(mass)**(1.0/D)*density
        else:
            self.rad = rad
        self.collision = collision

    def get_rect(self):
        return Rect(self.pos[0]-self.rad,self.pos[1]-self.rad,self.rad*2,self.rad*2)

    def get_mom(self):
        return (float(self.mass*self.vect[0]),float(self.mass*self.vect[1]))




def rand_bodies(num,minmass,maxmass,minvel,maxvel,collide=True):
    bodies = []
    for i in range(num):
        mass = randint(minmass,maxmass)
        x = randint(0,s_width)
        y = randint(0,s_height)
        x_vect = uniform(minvel,maxvel)
        y_vect = uniform(minvel,maxvel)
        color = (randint(0,255),randint(0,255),randint(0,255))
        bodies.append(Body(mass,(x,y),(x_vect,y_vect),color,-1,collide))
    return bodies



def star_sys(star_mass,planets,minmass,maxmass,mindist,maxdist,circular=True):
    bodies = [Body(star_mass,(s_width/2,s_height/2),(0,0),yellow,-1,True)]
    for i in range(planets):
        mass = randint(minmass,maxmass)
        dist = randint(mindist,maxdist)
        theta = uniform(0,2*math.pi)
        pos = (s_width/2+dist*math.cos(theta),s_height/2+dist*math.sin(theta))
        if circular:
            ratio = (star_mass/dist)**(1.0/2.0)
            x_vect = ratio*math.cos(theta+math.pi/2)
            y_vect = ratio*math.sin(theta+math.pi/2)
            vect = (x_vect,y_vect)
            print vect
        else:
            vect = (choice([-1,1])*uniform(0.5,1.5),choice([-1,1])*uniform(0.5,1.5))
        color = (randint(0,255),randint(0,255),randint(0,255))
        bodies.append(Body(mass,pos,vect,color,-1,True))
    return bodies



def main():

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


    #create bodies
    #mass, pos, vect, color, rad, collide
    global bodies
    bodies = []
    #bodies = rand_bodies(50,1,100,-1,1)
    #bodies = star_sys(1000,100,1,2,50,250,True)
    #bodies.append(Body(1000,(700,300),(2,0),black,20,True))
    ###bodies.append(Body(1000,(750,300),(0,0),red,-1,True))
    bodies = [
        Body(1000,(300,300),(0,1.0*-1.11803398875),red,-1,True),
        Body(1000,(700,300),(0,1.0*1.11803398875),blue,-1,True)
    ]
    bodies.extend(rand_bodies(100,1,2,3,0))



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
            elif event.type == MOUSEBUTTONDOWN:
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

        cam_speed = 5.0*(60.0/float(tick))
        shift_camera(cam_speed*x_shift,cam_speed*y_shift)

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








main()
