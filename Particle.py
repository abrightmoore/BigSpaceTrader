# @TheWorldFoundry
import random
import math
import pygame

import Identifier

class Mass:

    def __init__(self, universe):
        self.universe = universe
        self.id = universe.identifier.getNext()
        self.universe_location = 0, 0
        self.universe_radius = 4
        self.direction = random.random() * math.pi * 2.0
        self.speed = 0
        # self.target_speed = 0
        self.mass = 0
        self.colour = (255,255,255,255)

        self.orbit = None
        self.orbit_distance = None
        self.orbit_angle = 0
        self.orbit_angular_velocity = 0

        self.invisible = True
        self.age = 0

        # Rendering hints
        self.alive = True
        self.offscreen_count = 0
        self.display_box = None
        self.permanent = False

        # Interaction hints
        self.selected = False
        self.targeted = False

    def set_alive(self, value):
        self.alive = value

    def set_location(self, pos):
        self.universe_location = pos

    def set_velocity(self, direction, speed):
        self.direction = direction
        self.speed = speed

    def enter_orbit(self, orbitee, distance, angle, angular_velocity):
        if orbitee.mass.orbit == None or (orbitee.mass.orbit.mass != self and orbitee.mass != self):
            # Sort out angular velocity and distance
            #if distance == 0 or angular_velocity == 0:
                #   I want an orbiting body to move at about X pixels each update
            #    distance = orbitee.mass.universe_radius + self.universe_radius
            #    angular_velocity = math.atan2(0.1,float(distance))

            self.orbit = orbitee
            self.orbit_angle = angle
            self.orbit_distance = distance
            self.orbit_angular_velocity = angular_velocity

    def draw(self, display, pos, radius, draw_flag):
        x, y = pos
        if self.invisible == False and draw_flag:
            # @ place the particle on the display if it is in fact within the world coordinates
            if radius < 3:
                radius = 3
            pygame.draw.circle(display.surface, self.colour, (int(x), int(y)), int(radius), 1)

        if self.selected:
            pulseCol = math.cos(math.pi/360*self.age)*120
            G = 100+abs(int(pulseCol))
            pygame.draw.circle(display.surface, (80, G, 80, 255), (int(x), int(y)), int(radius+2), 2)

            # Directional indicator
            pygame.draw.line(display.surface, (255,0,0,255), (int(x), int(y)), (int(x+16*math.cos(self.direction)), int(y+16*math.sin(self.direction))), 1)

        if self.targeted:
            pulseCol = math.cos(math.pi/360*self.age)*120
            R = 100+abs(int(pulseCol))
            pygame.draw.circle(display.surface, (R, 80, 80, 255), (int(x), int(y)), int(radius+2), 2)


    def handle_click(self, pos, select):
        self.selected = False
        if self.display_box != None:
            cx, cy = pos
            (mx, my), (width, height) = self.display_box
            Mx = mx+width
            My = my+height
            if mx <= cx < Mx and my <= cy < My: # In bounds
                if select:
                    self.selected = True
                return True
        return False

    def handle_pickclick(self, pos, select):
        # self.selected = False
        if self.display_box != None:
            cx, cy = pos
            (mx, my), (width, height) = self.display_box
            Mx = mx+width
            My = my+height
            if mx <= cx < Mx and my <= cy < My: # In bounds
                if select:
                    self.selected = True
                return True
        return False

    def handle_rightclick(self, pos, select):
        self.targeted = False
        if self.display_box != None:
            cx, cy = pos
            (mx, my), (width, height) = self.display_box
            Mx = mx+width
            My = my+height
            if mx <= cx < Mx and my <= cy < My: # In bounds
                if select:
                    self.targeted = True
                return True
        return False


    def update(self):
        self.age += 1

        if self.orbit == None:
            # ToDo: lerping to target speed
            x, y = self.universe_location
            dx = self.speed * math.cos(self.direction)
            dy = self.speed * math.sin(self.direction)
            self.universe_location = x+dx, y+dy
            # print "Not orbiting "+str(self.id)
        else:
            self.orbit_angle += self.orbit_angular_velocity

            ox, oy = self.orbit.get_universe_location() # Location to orbit around
            # Position relative to the origin
            x = self.orbit_distance * math.cos(self.orbit_angle)
            y = self.orbit_distance * math.sin(self.orbit_angle)

            # Orientation
            newDir = float(self.orbit_angle)
            self.direction = newDir

            self.universe_location = ox+x, oy+y
            # print "Orbiting " + str(self.id)
        if self.permanent == False and self.offscreen_count > 600: # Ten seconds offscreen
            self.alive = False

