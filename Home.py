#Tkinter home screen environment generator
from Tkinter import *
from Physics import *
from Body import *

#init bodies list
global bodies
bodies = []



###################### body-maker wizard ####################

def make_body():
    global body
    body = Tk()

    #make labels
    mass_label = Label(body,text="mass")
    pos_label = Label(body,text="position (x,y)")
    vect_label = Label(body,text="velocity (x,y)")
    radius_label = Label(body,text="radius")
    collision_label = Label(body,text="can collide")
    color_label = Label(body,text="color (r,g,b)")

    #make entry fields and assosciated StringVar's
    global mass_field,px_field,py_field,vx_field,vy_field,radius_field,massint_field,r_field,g_field,b_field
    #mass = StringVar()
    mass_field = Entry(body)
    px_field = Entry(body)
    py_field = Entry(body)
    vx_field = Entry(body)
    vy_field = Entry(body)
    radius_field = Entry(body)
    r_field = Entry(body)
    g_field = Entry(body)
    b_field = Entry(body)

    #make checkboxes
    global collision,autorad
    collision = IntVar()
    collision_check = Checkbutton(body,variable=collision)
    collision_check.select()
    autorad = IntVar()
    autorad_check = Checkbutton(body,text="mass-based",variable=autorad)
    autorad_check.select()

    #make buttons
    submit_button = Button(body,text="add body",command=submit)

    #grid all elements to body
    mass_label.grid(row=0,column=0,sticky=E)
    mass_field.grid(row=0,column=1)
    
    pos_label.grid(row=1,column=0,sticky=E)
    px_field.grid(row=1,column=1)
    py_field.grid(row=1,column=2)
    
    vect_label.grid(row=2,column=0,sticky=E)
    vx_field.grid(row=2,column=1)
    vy_field.grid(row=2,column=2)
    
    radius_label.grid(row=3,column=0,sticky=E)
    radius_field.grid(row=3,column=1)
    autorad_check.grid(row=3,column=2,sticky=W)
    
    collision_label.grid(row=4,column=0,sticky=E)
    collision_check.grid(row=4,column=1,sticky=W)

    color_label.grid(row=5,column=0,sticky=E)
    r_field.grid(row=5,column=1)
    g_field.grid(row=5,column=2)
    b_field.grid(row=5,column=3)
    
    submit_button.grid(row=6,columnspan=4)
    

    body.mainloop()




def submit():
    mass = float(mass_field.get())
    pos = (float(px_field.get()),float(py_field.get()))
    vect = (float(vx_field.get()),float(vy_field.get()))
    color = (int(r_field.get()),int(g_field.get()),int(b_field.get()))
    if autorad:
        rad = -1
    else:
        rad = float(radius_field.get())
    collisionbool = collision.get()
    body.destroy()
    bodies.append(Body(mass,pos,vect,color,rad,collisionbool))

#################################################################

########################### make star sytem #####################

def make_star_system():
    global star
    star = Tk()

    #make labels
    mass_label = Label(star,text="star mass")
    planets_label = Label(star,text="number of planets")
    planetmass_label = Label(star,text="planet mass (min,max)")
    dist_label = Label(star,text="planet distance (min,max)")
    circular_label = Label(star,text="circular orbits")

    #make entry fields
    global mass_field,planets_field,minmass_field,maxmass_field,mindist_field,maxdist_field
    mass_field = Entry(star)
    planets_field = Entry(star)
    minmass_field = Entry(star)
    maxmass_field = Entry(star)
    mindist_field = Entry(star)
    maxdist_field = Entry(star)

    #make check boxes
    global circular
    circular = IntVar()
    circular_check = Checkbutton(star,variable=circular)
    circular_check.select()
    print circular.get()

    #make buttons
    submit_button = Button(star,text="make system",command=submit_system)

    #grid all elements to star
    mass_label.grid(row=0,column=0,sticky=E)
    mass_field.grid(row=0,column=1)
    
    planets_label.grid(row=1,column=0,sticky=E)
    planets_field.grid(row=1,column=1)
    
    planetmass_label.grid(row=2,column=0,sticky=E)
    minmass_field.grid(row=2,column=1)
    maxmass_field.grid(row=2,column=2)
    
    dist_label.grid(row=3,column=0)
    mindist_field.grid(row=3,column=1)
    maxdist_field.grid(row=3,column=2)

    circular_label.grid(row=4,column=0,sticky=E)
    circular_check.grid(row=4,column=1,sticky=W)
    
    submit_button.grid(row=5,columnspan=4)


    star.mainloop()

    


def submit_system():
    mass = int(mass_field.get())
    planets = int(planets_field.get())
    minmass = int(minmass_field.get())
    maxmass = int(maxmass_field.get())
    mindist = int(mindist_field.get())
    maxdist = int(maxdist_field.get())
    circularbool = circular.get()
    print circular.get()

    star.destroy()
    bodies.extend(star_sys(mass,planets,minmass,maxmass,mindist,maxdist,True))




#################################################################




def run_simulation(bodies):
    root.destroy()
    physics(bodies)



#init root
global root
root = Tk()



#create buttons
add_body = Button(root,text="add body",command=make_body)
star_system = Button(root,text="star system",command=make_star_system)
run = Button(root,text="run simulation",command=lambda: run_simulation(bodies))

#grid buttons to root
add_body.grid(row=0,column=0,sticky=W)
star_system.grid(row=1,column=0,sticky=W)
run.grid(row=2,column=0,columnspan=2,sticky=W)




root.mainloop()




















