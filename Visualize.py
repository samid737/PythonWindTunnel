

#Made by Dara Sami, Studentnumber 4313992.
#This script visualizes a 2D steady flow around an airfoil in Pygame. 
# I made this as a project for the Python Programming course for Aerospace Engineers.

#The Flow.py script models the flow using the vortex panel method.
# The GUI.py script creates the menu.I made it using example code contained in the PGU library.
#Source:http://pygame.org/project-PGU+-+Phil's+pyGame+Utilities-108-.html


#This file actually visualizes the data computed by Flow.py using pygame. In this file
#parameters are passed on to a function Compute, which is the main function in Flow.py.
#The accuracy of the vortex panel method can be adjusted here if desired by adjusting 
#the number of grid points and the number of panels used in the model. 
#Basically, I am using a grid of Nx times Ny points where at each point a velocity (u,v) vector is given.
#Then using Pygame I map these grid points as circles, so that they resemble an area of influence. 
#The grid points are the grey circles and tracks the movement of particles, and determines their velocity based upon where they 
#collide with a grid area *(using distance formula).

#I made the code for Flow.by by following an online course provided by Prof. Lorena.A.Barba.
# Source: http://lorenabarba.com/blog/announcing-aeropython/
#here step-by-step instructions are found for vortex panel modeling.
#I slightly adapted the structure of the code to make it suitable for pygame.


import pygame,sys,numpy,random
from Flow import Compute
from pygame.locals import *
pygame.init()

infoObject = pygame.display.Info()
width= int(infoObject.current_w*0.75)
height=int(infoObject.current_h*0.75)
Surface =pygame.display.set_mode((width,height)) 


#Surface = pygame.display.set_mode((width,height))
#read airfoil geometry from an external file

with open ('./airfoils/naca0018.dat') as file_name:
    x, y = numpy.loadtxt(file_name, dtype=float, delimiter='     ', unpack=True)    

#parameters used to describe the flow. These values are all passed onto Flow.py in line 57.
#Nx and Ny represent amount of grid points, you can adjust these values, but the GUI is 
#guaranteed to run properly after modifying. 
#N represents the number of panels.
# u_inf is the freestream velocity and should not be modified.
#Compute function is basically the function that is called once to compute the grid.

Nx=30
Ny=10
N=28
alpha=5
u_inf=1
number_of_particles=10
u,v,X,Y= Compute(x,y,N,alpha,u_inf,Nx,Ny)  

#Lists containing the grids and particles.
Circles = []
Particles= []


# The gui uses this function to rebuild the grid after pressing Recompute flow button.
def rebuild(NewNx,NewNy,N,alpha,airfoil):
    global x
    global y
    global u
    global v
    global X
    global Y
    global panel_x
    global panel_y
    global grid_x
    global grid_y
    global grid_u
    global grid_v
    global panelcoordinates
    global Circles
    global radii
    global circle_spacing_x
    global circle_spacing_y
    global circle_first_x
    global circle_first_y
    global Nx
    global Ny
    with open (airfoil) as file_name:
        x,y = numpy.loadtxt(file_name, dtype=float, delimiter='     ', unpack=True)    
    u,v,X,Y= Compute(x,y,N,alpha,u_inf,NewNx,NewNy) 
    Circles=[]
    # repeat line 119-134
    xmagnitude=(width/3)
    ymagnitude=-(height/2)
    vmag=30
    umag=30
    panel_x= numpy.multiply(x,xmagnitude)+(width//3)
    panel_y= numpy.multiply(y,ymagnitude)+(height//2)
    
    grid_x= numpy.multiply(X,xmagnitude)+(width//3)
    grid_y= numpy.multiply(Y,ymagnitude)+(height//2)
    
    grid_u =numpy.multiply(u,umag)
    grid_v =numpy.multiply(v,-vmag)
    
    radii= int(grid_x[0][2]-grid_x[0][1])//2
    panelcoordinates=  zip(panel_x, panel_y)
    Circles = appender(NewNx,NewNy,Circles,grid_x,grid_y,grid_u,grid_v)
    Nx=NewNx
    Ny=NewNy
    circle_spacing_x = Circles[1].x - Circles[0].x
    circle_spacing_y = Circles[NewNx].y - Circles[0].y
    circle_first_x = Circles[0].x - circle_spacing_x / 2
    circle_first_y = Circles[0].y - circle_spacing_y / 2
    
    
        

#Scaling factors used to properly position the potential flow on the pygame surface
xmagnitude=(width/3)
ymagnitude=-(height/2)
vmag=30
umag=30
panel_x= numpy.multiply(x,xmagnitude)+(width/3)
panel_y= numpy.multiply(y,ymagnitude)+(height/2)

grid_x= numpy.multiply(X,xmagnitude)+(width/3)
grid_y= numpy.multiply(Y,ymagnitude)+(height/2)


grid_u =numpy.multiply(u,umag)
grid_v =numpy.multiply(v,-vmag)
panelcoordinates=  zip(panel_x, panel_y)
radii= int(grid_x[0][2]-grid_x[0][1])//2

#Property of a grid point/area is defined here and is called a Circle
class Circle:
    def __init__(self,xpos,ypos,vx,vy,radii):

        self.radius=radii
        self.x = xpos
        self.y = ypos
        self.speedx = vx
        self.speedy = vy

#Append each Circle to the list
def appender(Nx,Ny,Circless,grid_x,grid_y,grid_u,grid_v):
    for i in range(Ny):
        for s in range(Nx):
            Circless.append(Circle(int(grid_x[i][s]),int(grid_y[i][s]),grid_u[i][s],grid_v[i][s],radii)) 
    return Circless
Circles= appender(Nx,Ny,Circles,grid_x,grid_y,grid_u,grid_v)

#used for collision detection in determining distances
circle_spacing_x = Circles[1].x - Circles[0].x
circle_spacing_y = Circles[Nx].y - Circles[0].y
circle_first_x = Circles[0].x - circle_spacing_x / 2
circle_first_y = Circles[0].y - circle_spacing_y / 2

#Property of a particle is defined here. I make them as circles, since the collisison detection is based upon circle collision.
class Particle:
    

    def __init__(self,xpos,ypos,vx,vy,radii):
        
        self.image1 = pygame.image.load("images/smoke1.png")
        self.image1 = self.image1.convert_alpha()
        self.image2 = pygame.image.load("images/smoke2.png")
        self.image2 = self.image2.convert_alpha()
        self.image3 = pygame.image.load("images/smoke3.png")
        self.image3 = self.image3.convert_alpha()
        self.image4 = pygame.image.load("images/smoke4.png")
        self.image4 = self.image4.convert_alpha()
        
        self.image5 = pygame.image.load("images/smoke5.png")
        self.image5 = self.image5.convert_alpha()
        self.image6 = pygame.image.load("images/smoke6.png")
        self.image6 = self.image6.convert_alpha()
        self.image7 = pygame.image.load("images/smoke7.png")
        self.image7 = self.image7.convert_alpha()
        self.image8 = pygame.image.load("images/smoke8.png")
        self.image8 = self.image8.convert_alpha()        
        self.image9 = pygame.image.load("images/smoke9.png")
        self.image9 = self.image9.convert_alpha()
        self.image10 = pygame.image.load("images/smoke10.png")
        self.image10 = self.image10.convert_alpha()       
        
        self.radius =radii*2
        self.x = xpos
        self.y = ypos
        self.speedx = umag
        self.speedy = 0
        self.size1 = self.image1.get_size()


        #THESE ARE ALL DIFFERENT PARTICLES TO GIVE A SMOKE EFFECT.
        self.spray0 = pygame.transform.scale(self.image1, (int(self.size1[0]*2), int(self.size1[1]*2)))
        self.spray1 = pygame.transform.scale(self.image1, (int(self.size1[0]*2), int(self.size1[1])*2))
        
        self.size2 = self.image2.get_size()

        self.spray2 = pygame.transform.scale(self.image2, (int(self.size2[0]*2), int(self.size2[1]*2)))
        self.spray3 = pygame.transform.scale(self.image2, (int(self.size2[0]*2), int(self.size2[1]*2)))
        

        self.spray4 = pygame.transform.scale(self.image3, (int(self.size1[0]*2), int(self.size1[1]*2)))
        self.spray5 = pygame.transform.scale(self.image3, (int(self.size1[0]*2), int(self.size1[1])*2))
        

        self.spray6 = pygame.transform.scale(self.image4, (int(self.size2[0]*2), int(self.size2[1]*2)))
        self.spray7 = pygame.transform.scale(self.image4, (int(self.size2[0]*2), int(self.size2[1]*2)))        
        

        self.spray8 = pygame.transform.scale(self.image5, (int(self.size2[0]*2), int(self.size2[1]*2)))
        self.spray9 = pygame.transform.scale(self.image5, (int(self.size2[0]*2), int(self.size2[1]*2)))        
                

        self.spray10 = pygame.transform.scale(self.image6, (int(self.size2[0]*2), int(self.size2[1]*2)))
        self.spray11 = pygame.transform.scale(self.image6, (int(self.size2[0]*2), int(self.size2[1]*2)))        
        
        
        self.spray12 = pygame.transform.scale(self.image7, (int(self.size2[0]*2), int(self.size2[1]*2)))
        self.spray13 = pygame.transform.scale(self.image7, (int(self.size2[0]*2), int(self.size2[1]*2)))           
        
        self.spray14 = pygame.transform.scale(self.image8, (int(self.size2[0]*2), int(self.size2[1]*2)))
        self.spray15 = pygame.transform.scale(self.image8, (int(self.size2[0]*2), int(self.size2[1]*2)))                
        
        
        self.spray16 = pygame.transform.scale(self.image9, (int(self.size2[0]*2), int(self.size2[1]*2)))
        self.spray17 = pygame.transform.scale(self.image9, (int(self.size2[0]*2), int(self.size2[1]*2)))                
         
        self.spray18 = pygame.transform.scale(self.image10, (int(self.size2[0]*2), int(self.size2[1]*2)))
        self.spray19 = pygame.transform.scale(self.image10, (int(self.size2[0]*2), int(self.size2[1]*2)))       
             
        self.spray20 = pygame.transform.scale(self.image9, (int(self.size2[0]*3), int(self.size2[1]*3)))    
        self.spray21 = pygame.transform.scale(self.image10, (int(self.size2[0]*3), int(self.size2[1]*3)))                  
        
        
#The motion of a particle
def Move():
    for Particle in Particles:
        Particle.x += Particle.speedx
        Particle.y += Particle.speedy

#spray particles in flow
def SpawnClick(number_of_particles,xpos,ypos):
    global spray
    if ypos <3*(height/4)-50 or ypos>(height/4)+50:
        spray=True
        Particles.append(Particle(xpos,ypos,1,0,radii))

def Spawn(number_of_particles):
    for i in range(number_of_particles):
            h=(((2*height/3)-(height/3))/(number_of_particles+1))
            Particles.append(Particle(0, (2*(height/3)-(i+1)*h),1,0,radii))
            
 #If our particles exit the screen at the wake, remove them and respawn particles at initial location.       
def Respawn(number_of_particles):
        for Particle in Particles:
            if Particle.x >width-(width//10):
                Particles.remove(Particle)
        if Particles==[]:
                Spawn(number_of_particles)
            
#We use detection for each particle in particle list, based upon distance formula. If particles exit the flow boundary, remove them.

def CollisionDetect():
    for particle in Particles:
        if particle.y >Circles[0].y or particle.y<Circles[-1].y:
           Particles.remove(particle)
           continue
        c = (particle.x - circle_first_x) // circle_spacing_x
        r = (particle.y - circle_first_y) // circle_spacing_y
        if r==20:
            circle = Circles[(r-1)*Nx+c]
        else:
            circle = Circles[r*Nx+c]
        if ((circle.x - particle.x)**2 + (circle.y - particle.y)**2
            <= (circle.radius+particle.radius)**2):       
                particle.speedx = int(circle.speedx)
                particle.speedy = int(circle.speedy)
                
#Visualize everything in pygame.
                
background=(255,255,255)
bg=pygame.image.load("images/tunnel.png")
bg = pygame.transform.scale(bg, (width,height-(height/5)))
gridcolor= (245,245,245)
spray=False
tunnel=False;


#Draw everthing on surface
def Draw():

    if tunnel:
        Surface.blit(bg,(0,0))   
        
    else:
        Surface.fill(background)
        for Circle in Circles:
            pygame.draw.circle(Surface,gridcolor,(Circle.x,Circle.y),Circle.radius)
  
  
    for Particle in Particles:
        if spray:
            whichparticle= random.randint(0,21)
            Surface.blit(getattr(Particle,"spray"+str(whichparticle)),(Particle.x,Particle.y))
        else:
            Surface.blit(Particle.spray1,(Particle.x,Particle.y))
            #pygame.draw.circle(Surface,(150,0,0),(Particle.x,Particle.y),Particle.radius)
    
    for i in range(len(panelcoordinates)-1):
        pygame.draw.line(Surface,(0,0,0),panelcoordinates[i],panelcoordinates[i+1],3)


def GetInput():# (!) CAN BE USED IF YOU WANT TO RUN VISUALIZE SEPERATELY
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]:
            pygame.quit();sys.exit()
        # (!)
        #else:
        #      # handle MOUSEBUTTONUP
        #    if pygame.mouse.get_pressed()[0]:
        #        pos = pygame.mouse.get_pos()
        #        SpawnClick(1,pos[0],pos[1])
def main():
    #clock = pygame.time.Clock() (!)
    #while True: (!)
        #ticks = clock.tick(30) (!)
        Respawn(number_of_particles)
        #GetInput() (!)
        CollisionDetect()
        Move()
        Draw()
        pygame.display.flip()
if __name__ == '__main__': main()
