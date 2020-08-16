# @TheWorldFoundry

import pygame
import math


class View:
    def __init__(self, universe, size, location):
        self.universe = universe
        self.width, self.height = size
        self.centre_of_view = location
        self.focus_object = None
        self.scale = 1
        self.clear_every = 1
        self.clear_flags = 0 # pygame.BLEND_RGBA_SUB
        self.age = 0

        self.show_planet_labels = False
        self.show_ship_labels = False
        self.show_station_labels = True

        pygame.init()

        print "Creating Surface and Window"
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.SRCALPHA)
        print "Converting the surface to optimise rendering"
        self.surface.convert()
        print "Changing the caption"
        pygame.display.set_caption('SiNGe: the Simulation eNGine')
        self.labelfont = pygame.font.SysFont("monospace", 16)
        pygame.key.set_repeat(100) # Milliseconds before new key event issued
        self.initialised = True

    def set_scale(self, scale):
        if scale > 0:
            self.scale = scale

    def get_world_box(self):
        '''
            What are the world co-ordinates at each corner of the display?
            :return: Tuple (minx, miny), (width, height)
        '''
        ox, oy = self.centre_of_view
        width = self.width * self.scale
        height = self.height * self.scale
        rx = width >> 1
        ry = height >> 1
        return ((ox - rx, oy - ry), (width + width%2, height + height%2))  # Point, Sizes

    def draw(self, elements):
        if self.surface != None:
            if self.age%self.clear_every == 0:
                self.surface.fill((2,2,1,0), None, self.clear_flags)
            # Centre of view
            pygame.draw.circle(self.surface, (255, 255, 255, 255), (self.width>>1, self.height>>1), 16, 1)
            for e in elements:
                if e.mass.alive:
                    # Check if any part of this element is onscreen.
                    (display_world_minx, display_world_miny), (display_width, display_height) = self.get_world_box()
                    display_world_maxx = display_world_minx + display_width
                    display_world_maxy = display_world_miny + display_height

                    px, py = e.mass.universe_location # This is the centre of the object
                    my_world_min_x = px - e.mass.universe_radius
                    my_world_max_x = px + e.mass.universe_radius
                    my_world_min_y = py - e.mass.universe_radius
                    my_world_max_y = py + e.mass.universe_radius
                    if my_world_min_x < display_world_maxx and my_world_max_x >= display_world_minx:
                        if my_world_min_y < display_world_maxy and my_world_max_y >= display_world_miny:
                            # I'm on the display, but where?
                            e.mass.offscreen_count = 0
                            world_dx = my_world_min_x - display_world_minx # Relative co-ordinates
                            world_dy = my_world_min_y - display_world_miny # Relative co-ordinates
                            display_radius = e.mass.universe_radius / self.scale # Apparent size
                            display_px = world_dx / self.scale
                            display_py = world_dy / self.scale

                            e.draw(self, (display_px+display_radius, display_py+display_radius), display_radius)
                            e.mass.display_box = ((int(display_px), int(display_py)), (display_radius<<1, display_radius<<1))


                    else: # Is not onscreen
                        e.mass.offscreen_count += 1
                        e.mass.display_box = None
        # Housekeeping
        #  Center of view
        if self.labelfont != None:
            x,y = self.centre_of_view
            dataline = "$CR: "+str(self.universe.score)+"  POS: "+str(int(x))+" "+str(int(y))+" SCALE: "+str(self.scale)
            if self.focus_object != None and self.focus_object.name != None:
                dataline += " FO: "+self.focus_object.name
            lbl = self.labelfont.render(dataline, False, (140, 140, 240))
            self.surface.blit(lbl, (4, 4))

    def toggleFlag(self, flag):
        if flag:
            return False
        else:
            return True

    def update(self):
        self.age += 1
        if self.focus_object != None:
            self.centre_of_view = self.focus_object.get_universe_location()
        unhandledEvents = []
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                # Clicked on a UI element?
                unhandledEvents.append(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll
                    scaleDelta = math.log(self.scale)
                    newScale = self.scale-(1+int(scaleDelta))
                    if newScale < 1:
                        newScale = 1
                    self.set_scale(newScale)

                if event.button == 5:  # Scroll
                    scaleDelta = math.log(self.scale)
                    self.set_scale(self.scale + (1 + int(scaleDelta)))

                else:
                    unhandledEvents.append(event)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    scaleDelta = math.log(self.scale)
                    self.set_scale(self.scale+(1+int(scaleDelta)))
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                    scaleDelta = math.log(self.scale)
                    newScale = self.scale-(1+int(scaleDelta))
                    if newScale < 1:
                        newScale = 1
                    self.set_scale(newScale)
                elif event.key == pygame.K_LEFT:
                    x,y = self.centre_of_view
                    x -= self.scale*16
                    self.centre_of_view = x,y
                    self.focus_object = None
                elif event.key == pygame.K_RIGHT:
                    x,y = self.centre_of_view
                    x += self.scale*16
                    self.centre_of_view = x,y
                    self.focus_object = None
                elif event.key == pygame.K_UP:
                    x,y = self.centre_of_view
                    y -= self.scale*16
                    self.centre_of_view = x,y
                    self.focus_object = None
                elif event.key == pygame.K_DOWN:
                    x,y = self.centre_of_view
                    y += self.scale*16
                    self.centre_of_view = x,y
                    self.focus_object = None
                elif event.key == pygame.K_0:
                    self.centre_of_view = 0,0 # Default centre of view
                    self.scale = 1 # Default scale
                    self.focus_object = self.universe.home_planet
                elif event.key == pygame.K_l:
                    self.show_station_labels = self.toggleFlag(self.show_station_labels)
                    self.show_ship_labels = self.toggleFlag(self.show_ship_labels)
                    self.show_planet_labels = self.toggleFlag(self.show_planet_labels)
                elif event.key == pygame.K_p:
                    self.show_planet_labels = self.toggleFlag(self.show_planet_labels)
                elif event.key == pygame.K_s:
                    self.show_ship_labels = self.toggleFlag(self.show_ship_labels)
                elif event.key == pygame.K_t:
                    self.show_station_labels = self.toggleFlag(self.show_station_labels)

            else:
                unhandledEvents.append(event)

        pygame.display.update()

        return unhandledEvents