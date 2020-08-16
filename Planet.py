import pygame
import random

import Particle

class World:
    orbit_distance = 50

    def __init__(self, universe, radius):
        self.name = None
        self.mass = Particle.Mass(universe)
        self.mass.universe_radius = radius
        self.mass.universe_location = 0, 0 # Put this at the origin
        self.mass.permanent = True
        self.mass.invisible = False
        self.products = None
        self.world_type = self.get_world_type()


    def get_world_type(self):
        # Worlds are either industrial or agricultural, which determines their produce types
        produce_table = self.mass.universe.produce.get_product_tables()
        types = produce_table.keys()
        R = random.Random(self.mass.id)
        seed = R.randint(-999999999999, 999999999999)

        result = types[seed%len(types)]
        # print seed, result

        self.products = {}
        # Add the trades table - with buy and sell prices
        for key in types:
            max_variance = 0.20
            if key == result: # Type of world is this one?
                max_variance = -0.30
            products = produce_table[key]
            #print products
            for product in products:
                # print product
                # print products[product]
                price_base = products[product]["price"]
                price_shift = max_variance*R.random()
                price_low = float(price_base) + float(price_base * price_shift)
                price_high = price_low + float(price_low * (0.03+R.random()*0.17))
                self.products[product] = {
                    "buy" : int(price_low) ,  # Planet's buy price from player
                    "sell" : int(price_high) , # Planet's sell price to player
                }
        # print self.products

        return result

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
            if self.name != None and self.mass.display_box != None and (display.show_planet_labels or self.mass.targeted):
                (x, y), (w, h) = self.mass.display_box
                dataline = self.name
                if self.world_type != None:
                    dataline = dataline+" [" + self.world_type + "]"
                lbl = display.labelfont.render(dataline, False, (40, 255, 255))
                display.surface.blit(lbl, (x, y - 18))

            if self.mass.targeted and self.products != None:
                (x, y), (w, h) = self.mass.display_box
                cursory = y+h+8
                for product in self.products:
                    dataline = "$CR BUY: "
                    buy_price = str(self.products[product]["buy"])
                    sell_price = str(self.products[product]["sell"])
                    dataline = dataline+str(self.pad(buy_price," ",4))+"  SELL: "+str(self.pad(sell_price," ",4))+"  "+product
                    lbl = display.labelfont.render(dataline, False, (220, 255, 255))
                    display.surface.blit(lbl, (x, cursory))
                    cursory += 18

        self.mass.draw(display, pos, radius, False)

    def pad(self, text, char, length):
        padlength = length*len(char)-len(text)
        if padlength > 0:
            for i in xrange(0, padlength):
                text += char
        return text

    def update(self):
        self.mass.update()

    def handle_click(self, pos, select):
        return False # Disable left click on planets
        #self.mass.handle_click(pos, select)

    def handle_pickclick(self, pos, select):
        return self.mass.handle_pickclick(pos, select)

    def handle_rightclick(self, pos, select):
        return self.mass.handle_rightclick(pos, select)