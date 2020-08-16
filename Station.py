import pygame

import Particle

class Station:
    ship_orbit_speed = 0.0001
    orbit_distance = 0

    def __init__(self, universe, radius):
        self.name = None
        self.mass = Particle.Mass(universe)
        self.mass.universe_radius = radius
        self.mass.universe_location = 0, 0 # Put this at the origin
        self.mass.permanent = True
        self.mass.invisible = False
        self.mass.colour = (255, 255, 255, 255)

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
            if self.name != None and self.mass.display_box != None and display.show_station_labels:
                (x, y), (w, h) = self.mass.display_box
                dataline = self.name
                lbl = display.labelfont.render(dataline, False, (40, 255, 255))
                display.surface.blit(lbl, (x, y - 18))

        self.mass.draw(display, pos, radius, False)

    def update(self):
        self.mass.update()

    def handle_click(self, pos, select):
        return False # Disable left click on stations
        # self.mass.handle_click(pos, select)

    def handle_pickclick(self, pos, select):
        return self.mass.handle_pickclick(pos, select)


    def handle_rightclick(self, pos, select):
        return self.mass.handle_rightclick(pos, select)