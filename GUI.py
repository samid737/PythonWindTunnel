#!/usr/bin/env python

# This is not needed if you have PGU installed


import sys
sys.path.insert(0, "..")


# The GUI script. 
#I do not have full knowledge of the code so I cannot provide details, but I simply modified an existing code within the PGU library so that it contains the simulation.
# The whole Visualize.py I put in a container and the menu I just took snippets of code from some examples and added them.
import math
import pygame
import pgu
import Visualize
from pgu import gui, timer

pygame.display.set_caption("2D Flow simulation")
infoObject = pygame.display.Info()
w= int(infoObject.current_w)
h=int(infoObject.current_h)


airfoil= './airfoils/naca0018.dat'

class DrawingArea(gui.Widget):
    def __init__(this, width, height):
        gui.Widget.__init__(this, width=width, height=height)
        this.imageBuffer = pygame.Surface((width, height))

    def paint(this, surf):
        # Paint whatever has been captured in the buffer
        surf.blit(this.imageBuffer, (0, 0))

    # Call this function to take a snapshot of whatever has been rendered
    # onto the display over this widget.
    def save_background(this):
        disp = pygame.display.get_surface()
        this.imageBuffer.blit(disp, this.get_abs_rect())
        
        
class AboutDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Help")
        
        doc = gui.Document(width=400)
        
        space = title.style.font.size(" ")
        
        doc.block(align=-1)
        for word in """Made By Dara Sami\nemail: D.Sami-1@student.tudelft.nl\nstudentnumber:4313992""".split("\n"): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)    
        for word in """For any questions you can contact me.\n """.split("\n"): 
            doc.add(gui.Label(word))
            doc.space(space)        
        
        
        doc.block(align=-1)
        for word in """\nThis script visualizes a 2D steady flow around an airfoil in Pygame.\n The Flow.py script computes the flow using the vortex panel method. \n
The airfoil, angle of attack and flow accuracy are parameters that can be adjusted if desired\n(increasing doubles the grid).\n After changing the parameters click the Recompute flow button to recompute. \n This might take up to 20 seconds depending on the desired accuracy and your computer.\n\nYou can browse through some of the airfoils I have added to the program,but you can always \nadd more .dat files. \nPlease note that each .dat file must only contain coordinates in Selig format \n(see available .dat files as an example)and must be seperated by tabs.""".split("\n"): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)    
        for word in """I built the Flow.by code with the help of a course provided by Prof. Lorena.A.Barba.\nSource: http://lorenabarba.com/blog/announcing-aeropython/\nhere step-by-step instructions are found for vortex panel modeling.\nI slightly modified the code to make it suitable for pygame.
\nThe GUI.py script creates the menu.I made it using example code(gui18) contained in the PGU library.\nSource:http://pygame.org/project-PGU+-+Phil's+pyGame+Utilities-108-.html        
        
        
        """.split("\n"): 
            doc.add(gui.Label(word))
            doc.space(space)

        gui.Dialog.__init__(self,title,doc)


class MainGui(gui.Desktop):
    gameAreaHeight = (4*h/5)
    gameArea = None
    menuArea = None
    # The game engine
    engine = None

    def __init__(this, disp):
        gui.Desktop.__init__(this)

        # Setup the 'game' area where the action takes place
        this.gameArea = DrawingArea(disp.get_width(),this.gameAreaHeight)
        # Setup the gui area
        this.menuArea = gui.Container(
        height=disp.get_height()-this.gameAreaHeight)

        tbl = gui.Table(height=disp.get_height())
        tbl.tr()
        tbl.td(this.gameArea)
        tbl.tr()
        tbl.td(this.menuArea)

        this.setup_menu()

        this.init(tbl, disp)

    def setup_menu(this):
        global NewNx
        global NewNy
        NewNx= Visualize.Nx
        NewNy= Visualize.Ny
        #--------------------------- ACCURACY

        tbl = gui.Table(vpadding=2, hpadding=1)
        
        def open_file_browser(arg):
            d = gui.FileDialog()
            d.connect(gui.CHANGE, handle_file_browser_closed, d)
            d.open()
        
        
        def handle_file_browser_closed(dlg):
            if dlg.value: input_file.value = dlg.value
            global airfoil
            airfoil=dlg.value

        td_style = {'padding_right': 10}
        t = gui.Table()
        t.tr()
        t.td( gui.Label('Airfoil') , style=td_style )
        input_file = gui.Input()
        t.td( input_file, style=td_style )
        b = gui.Button("Browse...")
        t.td( b, style=td_style )
        b.connect(gui.CLICK, open_file_browser, None)
        tbl.add(t)
        
        #----------------------row 1
        tbl1 = gui.Table(vpadding=2, hpadding=1)
        timeLabel2 = gui.Label("Accuracy")
        tbl1.td(timeLabel2)
        slider3 = gui.HSlider(1,min=1,max=2,size=20,height=16,width=120)
        
        def update_accuracy():
            global NewNx
            global NewNy
            if slider3.value==1:
                NewNx=30 
                NewNy=10
            if slider3.value==2:
                NewNx=60 
                NewNy=20                
       
        slider3.connect(gui.CHANGE, update_accuracy)
        tbl1.td(slider3)        
        #---------------------------------------alpha
        timeLabel2 = gui.Label("Alpha")
        tbl1.td(timeLabel2)
        slider2 = gui.HSlider(value=Visualize.alpha,min=-10,max=10,size=20,height=16,width=120)
        def update_alpha():
            Visualize.alpha=slider2.value
       
        slider2.connect(gui.CHANGE, update_alpha)
        tbl1.td(slider2)
        
        
         #---------------------------------------

        def recompute_cb():
            global airfoil
            global NewNx
            global NewNy
            Visualize.rebuild(NewNx,NewNy,Visualize.N,Visualize.alpha,airfoil);


        btn = gui.Button("Recompute flow", height=25)
        tbl1.td(btn)
        btn.connect(gui.CLICK, recompute_cb)
        #---------------------------------------gamepause
        tbl.add(tbl1)        
        tbl.tr()
        

        #------------------------row2        
        
        def pause_cb():
            if (this.engine.clock.paused):
                this.engine.resume()
            else:
                this.engine.pause()

        
         #---------------------------------------gamespeed
        tbl2 = gui.Table(vpadding=2, hpadding=1)
        timeLabel = gui.Label("Playback speed")
        tbl2.td(timeLabel)
        slider = gui.HSlider(value=1,min=1,max=100,size=20,height=16,width=120)
        
        def update_speed():
            this.engine.clock.set_speed((slider.value/5)*3)
        slider.connect(gui.CHANGE, update_speed)
        tbl2.td(slider)
        
        #-------button speed        
        
        btn = gui.Button("Toggle normal speed", height=25)
        btn.connect(gui.CLICK, pause_cb)
        tbl2.td(btn)
        tbl2.tr()
        
        #---------------------------------------particles
        timeLabel3 = gui.Label("N particles")
        tbl2.td(timeLabel3)
        
        slider4 = gui.HSlider(Visualize.number_of_particles,min=1,max=14,size=20,height=16,width=120)
        
        def update_particles():
            Visualize.number_of_particles=slider4.value
            
        slider4.connect(gui.CHANGE, update_particles)
        tbl2.td(slider4)        
        tbl2.tr()
        
        
        def gridswitch_changed(switch):
            if switch.value:
                Visualize.tunnel=True
            else:
                Visualize.tunnel=False
            
        gridswitch = gui.Switch(value=False,name='warp')
        gridswitch.connect(gui.CHANGE, gridswitch_changed, gridswitch)
        
        

        tbl2.td(gui.Label("New top secret wind tunnel:"),align=1)
        tbl2.td(gridswitch)        
        
        tbl.add(tbl2)
        
        
        
        #---------------------row 3
        
       
         #---------------------------------------about
        
        
        tbl3=gui.Table()
        

        dlg = AboutDialog()
        def about_cb():
            dlg.open()
            
        btn = gui.Button("About", height=5)
        tbl3.td(btn)
        btn.connect(gui.CLICK, about_cb)
        #tbl3.tr()
        tbl3.td(gui.Label("Hint: Press and hold mouse button to spray particles!",align=1,colspan=2))
        tbl.td(tbl3)
        
        
        
        this.menuArea.add(tbl, 10, 0)

    def open(this, dlg, pos=None):
        # Gray out the game area before showing the popup
        rect = this.gameArea.get_abs_rect()
        dark = pygame.Surface(rect.size).convert_alpha()
        dark.fill((0,0,0,150))
        pygame.display.get_surface().blit(dark, rect)
        # Save whatever has been rendered to the 'game area' so we can
        # render it as a static image while the dialog is open.
        this.gameArea.save_background()
        # Pause the gameplay while the dialog is visible
        running = not(this.engine.clock.paused)
        this.engine.pause()
        gui.Desktop.open(this, dlg, pos)
        while (dlg.is_open()):
            for ev in pygame.event.get():
                this.event(ev)
            rects = this.update()
            if (rects):
                pygame.display.update(rects)
        if (running):
            # Resume gameplay
            this.engine.resume()

    def get_render_area(this):
        return this.gameArea.get_abs_rect()


class GameEngine(object):
    def __init__(this, disp):
        this.disp = disp
        this.app = MainGui(this.disp)
        this.app.engine = this

    # Pause the game clock
    def pause(this):
        this.clock.pause()

    # Resume the game clock
    def resume(this):
        this.clock.resume()



    def run(this):
        this.app.update()
        pygame.display.flip()

        this.font = pygame.font.SysFont("", 16)
        this.clock = timer.Clock() #pygame.time.Clock()
        done = False
        while not done:
            # Process events
            for ev in pygame.event.get():
                if (ev.type == pygame.QUIT or 
                    ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                    pygame.quit();sys.exit()
                else:
                     # handle MOUSEBUTTONUP
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        #print(pos)
                        Visualize.SpawnClick(1,pos[0],pos[1])
                    else:
                        Visualize.spray=False
                    # Pass the event off to pgu
                    this.app.event(ev)
            # Render the game
            rect = this.app.get_render_area()
            updates = []
            this.disp.set_clip(rect)
            lst = Visualize.main()
            if (lst):
                updates += lst

            this.disp.set_clip()

            # Cap it at 30fps
            this.clock.tick(20)

            # Give pgu a chance to update the display
            lst = this.app.update()
            #if (lst):
            #    updates += lst
            #pygame.display.update(updates)
            #pygame.time.wait(10)


###


disp = pygame.display.set_mode((w, h))
eng = GameEngine(disp)
eng.run()

