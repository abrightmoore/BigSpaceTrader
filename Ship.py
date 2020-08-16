import pygame
import math
import random

import Particle

import VesselRenderer9

class Ship:
    orbit_distance = 0
    def __init__(self, universe, radius):
        self.name = None
        self.mass = Particle.Mass(universe)
        self.mass.universe_radius = radius
        self.mass.universe_location = 0, 0 # Put this at the origin
        self.mass.permanent = True
        self.mass.invisible = False
        self.mass.colour = (40, 60, 255, 255)
        self.texture = VesselRenderer9.makeShip((0,0),
                            universe.universe_configuration.R.randint(-999999999999,999999999999),
                                                (radius<<1,radius)).gfx
        self.trade_targets = []
        self.trade_target_current = None
        self.move_targets = []
        self.move_target_current = None

    def get_universe_location(self):
        return self.mass.universe_location

    def get_id(self):
        return self.mass.id

    def set_colour(self, colour):
        self.mass.colour = colour

    def set_invisible(self, invisible):
        self.mass.invisible = invisible

    def set_universe_location(self, universe_location):
        self.mass.universe_location = universe_location

    def set_name(self, name):
        self.name = name

    def draw(self, display, pos, radius):
        if self.mass.invisible == False:
            x, y = pos
            # @ place the particle on the display if it is in fact within the world coordinates
            if radius < 3:
                radius = 3
            pygame.draw.circle(display.surface, self.mass.colour, (int(x), int(y)), int(radius), 0)
            #display.surface.blit(self.texture, (x-(self.mass.universe_radius>>1),y-self.mass.universe_radius))

            if self.name != None and self.mass.display_box != None and display.show_ship_labels:
                (x, y), (w, h) = self.mass.display_box
                dataline = self.name+"-"+str(self.mass.id)
                lbl = display.labelfont.render(dataline, False, (40, 60, 255))
                display.surface.blit(lbl, (x, y+h + 6))

                # dataline = "V: "+str(self.mass.direction)+", "+str(self.mass.speed)
                # lbl = display.labelfont.render(dataline, False, (40, 60, 255))
                # display.surface.blit(lbl, (x, y+h + 6 +18))

                # dataline = " O: "+str(self.mass.orbit_angle)+", "+str(self.mass.orbit_angular_velocity)+"  ODist: "+str(self.mass.orbit_distance)
                # lbl = display.labelfont.render(dataline, False, (40, 60, 255))
                # display.surface.blit(lbl, (x, y+h + 6 +18 + 18))

                if self.move_target_current != None and self.move_target_current.mass.display_box != None:
                    (x2, y2), (w2, h2) = self.move_target_current.mass.display_box
                    pygame.draw.line(display.surface,(100+(self.mass.age%150),0,90,255),(x+(w>>1),y+(h>>1)),(x2+(w2>>1),y2+(h2>>1)),self.mass.age%4)
                    

        self.mass.draw(display, pos, radius, False)

    def update(self):
        # Check target

        if self.trade_target_current == None and len(self.trade_targets) > 0:
            self.trade_target_current = self.trade_targets.pop(0)
            self.move_target_current = self.trade_target_current

        if self.move_target_current == None and len(self.move_targets) > 0:
            # I can select a new target
            self.move_target_current = self.move_targets.pop(0)
            self.mass.selected = False
            self.mass.targeted = False

        if self.move_target_current != None: # I should be moving now!
            # Where is the target in space?
            px, py = self.move_target_current.get_universe_location()
            x, y = self.get_universe_location()

            dx = px-x
            dy = py-y
            distance_to_target = math.sqrt(dx**2+dy**2)
            newOrbitDistance = self.move_target_current.mass.universe_radius+self.move_target_current.orbit_distance+self.mass.universe_radius
            angle = math.atan2(dy, dx)
            if distance_to_target < newOrbitDistance: # Am I close to the destination
                self.mass.enter_orbit(self.move_target_current, newOrbitDistance, angle+math.pi, 0.0001)
                self.move_target_current = None # Expire the current target
                self.move_targets = []
                self.trade_targets = []
                self.trade_target_current = None

            else: # Recalculate
                self.mass.set_velocity(angle, 1.5) # ToDo - turn slowly instead of all at once
                self.mass.orbit = None
                self.mass.orbit_angular_velocity = 0
                # print self.mass.direction/(math.pi/180), self.mass.speed
        # print self.mass.id, "Move Targets:", self.move_targets
        # print self.mass.id, "Move Target Current:", self.move_target_current

        # print self.mass.id, "Trade Targets", self.trade_targets
        # print self.mass.id, "Trade Target Current:", self.trade_target_current

        self.mass.update()

    def handle_click(self, pos, select):
        return self.mass.handle_click(pos, select)

    def handle_pickclick(self, pos, select):
        return self.mass.handle_pickclick(pos, select)

    def handle_rightclick(self, pos, select):
        return self.mass.handle_rightclick(pos, select)