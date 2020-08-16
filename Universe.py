# @TheWorldFoundry

import random
import math
import Planet
import Station
import Ship
import Produce

import Identifier

class Universe:
    def __init__(self):
        self.identifier = Identifier.ID(0)
        self.home_planet = None # Special planet
        self.universe_configuration = None
        self.produce = Produce.Produce()
        self.score = 10000

    def setup_start_area(self, elements, display):
        self.universe_configuration = UniverseConfiguration(420)

        self.universe_configuration.setup_universe(elements, self)
        # self.universe_configuration.set_up_ship_and_planet(self, elements)

class UniverseConfiguration:

    def __init__(self, seed):
        self.seed = seed
        self.R = random.Random(seed)

    def get_catalog_id(self, length):
        digits = "ABCDEFGHJKMNPQRSTUWXYZ23456789"
        catalog = ""
        for i in xrange(0, length):
            catalog = catalog + digits[self.R.randint(0,len(digits)-1)]
        return catalog

    def setup_universe(self, elements, universe):
        position = 0, 0
        self.make_solar_system_at(elements, universe, position)

    def make_asteroids_at(self, centre_of_system, elements, universe, rmin, rmax):
        for i in xrange(0, self.R.randint(5, 150)):
            asteroid = Planet.World(universe, self.R.randint(4, 16))
            R = self.R.randint(100, 200)
            asteroid.mass.colour = (R, R - 40, R - self.R.randint(0, 60), 255)
            asteroid.mass.enter_orbit(centre_of_system, self.R.randint(rmin, rmax), self.R.random() * math.pi * 2.0,
                                      -0.00001 * self.R.randint(-50, 50))
            elements.append(asteroid)

    def make_station_at_planet(self, planet, elements, universe):
        station = Station.Station(universe, 32)
        station.mass.enter_orbit(planet, planet.mass.universe_radius*1.5, self.R.random()*math.pi*2.0, 0.000001*self.R.randint(-20,20))
        station.name = planet.name+" Station"
        elements.append(station)

        self.make_ship_at_station( station, elements, universe)

    def make_ship_at_station(self, station, elements, universe):
        ship = Ship.Ship(universe, 16)
        ship.mass.enter_orbit(station, station.mass.universe_radius+ship.mass.universe_radius, self.R.random() * math.pi *2.0, station.ship_orbit_speed)
        # ship.mass.enter_orbit(station, 0, self.R.random() * math.pi * 2.0, 0)
        ship.name = "SS "+ self.get_catalog_id(10)
        elements.append(ship)

    def make_planetary_system_at(self, centre_of_system, elements, universe, rmin, rmax):
        # Anchor a planet within the band, possibly with moons
        if rmax - rmin > 1000:
            R = self.R
            if R.random() > 0.6:
                # Single planet
                radius = (rmax-rmin)>>1
                radius = R.randint(radius>>4, radius)
                planet = Planet.World(universe, radius)
                planet.set_name(centre_of_system.name+"-"+self.get_catalog_id(8))
                planet.set_colour( (int(R.randint(128,240)), int(R.randint(128,240)), int(R.randint(128,240)), 255))
                planet.mass.enter_orbit(centre_of_system, rmin+(rmax - rmin)>>1, R.random()*math.pi*2.0, 0.000001*R.randint(-20,20))
                elements.append(planet)

                self.make_station_at_planet(planet, elements, universe)

            else:
                # Mini system
                # Single planet
                radius = (rmax-rmin)>>3
                radius = R.randint(radius>>2, radius)
                planet = Planet.World(universe, radius)
                planet.set_name(centre_of_system.name+"-"+self.get_catalog_id(8))
                planet.set_colour( (int(R.randint(128,240)), int(R.randint(128,240)), int(R.randint(128,240)), 255))
                planet.mass.enter_orbit(centre_of_system, rmin+(rmax - rmin)>>1, R.random()*math.pi*2.0, 0.000001*R.randint(-20,20))
                self.make_station_at_planet(planet, elements, universe)
                elements.append(planet)
                delta_radius = ((rmax-rmin)>>1)-radius

                # Neighbours
                self.make_planetary_system_at(planet, elements, universe, radius, delta_radius)




    def make_stars_at(self, centre_of_system, elements, universe, radius):
        R = self.R

        cx, cy = centre_of_system.get_universe_location()
        number_of_stars = R.randint(1,5)

        phi = math.pi*2.0

        star_angle_gap = phi/number_of_stars

        star_distance = R.randint(0,radius)

        MAXRADIUS = star_distance
        MINRADIUS = star_distance>>4

        radius_cursor = star_distance>>1
        star_radius = radius_cursor

        for i in xrange(0, number_of_stars):
            x = cx+radius_cursor * math.cos(star_angle_gap * i)
            y = cy+radius_cursor * math.sin(star_angle_gap * i)
            radius_cursor += star_radius # Offset by old radius
            star_radius = R.randint(MINRADIUS, MAXRADIUS)
            radius_cursor += star_radius # Offset by new radius
            temperature = 1.0 - float(star_radius)/float(MAXRADIUS)
            temp_R = 255 # (1.0-temperature) * 40 + 200
            temp_G = temperature * 240 +15
            temp_B = temperature * 255
            star = Planet.World(universe, star_radius)
            star.set_name(centre_of_system.name + "-" + "ST-" +  str(i+1))
            star.set_universe_location((x,y))
            star.set_colour( (int(temp_R), int(temp_G), int(temp_B), 255))
            star.mass.enter_orbit(centre_of_system, radius_cursor, star_angle_gap * i, 0.000001*R.randint(-50,50))
            star.world_type = None # Remove any industry
            star.products = None # Remove any trades
            elements.append(star)


    def make_solar_system_at(self, elements, universe, position):
        centre_of_system = Planet.World(universe, 1)
        centre_of_system.set_invisible(True)  # Centre of gravity for the system - nothing to see here
        centre_of_system.set_universe_location(position)
        centre_of_system.set_colour((0,0,0,0))
        centre_of_system.set_name(self.get_catalog_id(5))
        elements.append(centre_of_system) # This is the object about which everything may rotate

        self.make_stars_at(centre_of_system, elements, universe, self.R.randint(1000,5000))

        # Within bands out to the edge of the system, create planetary systems
        SYSRADIUSMIN = 10000
        SYSRADIUSMAX = 500000
        system_radius = self.R.randint(SYSRADIUSMIN, SYSRADIUSMAX)
        cursor = SYSRADIUSMIN
        while cursor < system_radius:
            gapsize = self.R.randint(1000, 10000)
            if cursor < (system_radius>>3) and gapsize < 2000 and self.R.random() > 0.3: # Asteroids
                self.make_asteroids_at(centre_of_system, elements, universe, cursor, cursor + gapsize)
            elif self.R.random() > 0.4:
                self.make_planetary_system_at(centre_of_system, elements, universe, cursor, cursor + gapsize)
            # Otherwise leave a gap
            cursor += gapsize



    def setup_start_area_random_orbits(self, universe, elements, display):
        # Create the first place the player sees

        for x in xrange(-10, 10):
            print "Preparing", x
            for y in xrange(-10, 10):
                if random.random() > 0.8:
                    rad = random.randint(80, 300)
                    planet = Planet.World(universe, rad)
                    if self.home_planet == None:
                        self.home_planet = planet
                        display.focus_object = planet

                    planet.mass.colour = (120+random.randint(0,30), 150+random.randint(0,30), 175+random.randint(0,30), 255)
                    px, py = (x*10000+random.randint(-5000,5000),y*10000+random.randint(-5000,5000))
                    planet.mass.universe_location = (x*1000000+random.randint(-5000,5000),y*1000000+random.randint(-5000,5000))
                    if len(elements) > 1:
                        planet.mass.enter_orbit(elements[0], (px+py), random.random()*math.pi*2.0, -0.0001 * random.randint(1, 15))
                    elements.append(planet)

                    if random.random > 0.95:
                        moon = Planet.World(universe, random.randint(30,100))
                        moon.mass.colour = (170, 170, 175, 255)
                        moon.mass.enter_orbit(planet, rad*4, 0, -0.0001*random.randint(-5,5))
                        elements.append(moon)

                        moon2 = Planet.World(universe, 16)
                        moon2.mass.colour = (170, 110, 115, 255)
                        moon2.mass.enter_orbit(moon, random.randint(150,250), 0, -0.001*random.randint(-5,5))
                        elements.append(moon2)

                        moon2 = Planet.World(universe, 32)
                        moon2.mass.colour = (170, 110, 115, 255)
                        moon2.mass.enter_orbit(moon, random.randint(250,350), 0, -0.002*random.randint(-5,5))
                        elements.append(moon2)


                    if random.random > 0.95:

                        for i in xrange(0, random.randint(5,15)):
                            asteroid = Planet.World(universe, random.randint(4,16))
                            R = random.randint(100, 200)
                            asteroid.mass.colour = (R, R-40, R-random.randint(0,60), 255)
                            asteroid.mass.enter_orbit(planet, random.randint(2500,3000), random.random()*math.pi*2.0, -0.00001*random.randint(-50,50))
                            elements.append(asteroid)

    def set_up_ship_and_planet(self, universe, elements):
        R = self.R
        planet = Planet.World(universe, 100)
        planet.set_name("PL" + "-" + self.get_catalog_id(8))
        planet.set_universe_location((0,0))
        planet.set_colour((int(R.randint(128, 240)), int(R.randint(128, 240)), int(R.randint(128, 240)), 255))
        elements.append(planet)
        planet2 = Planet.World(universe, 100)
        planet2.set_name("PL" + "-" + self.get_catalog_id(8))
        planet2.set_universe_location((1000,0))
        planet2.set_colour((int(R.randint(128, 240)), int(R.randint(128, 240)), int(R.randint(128, 240)), 255))
        elements.append(planet2)

        self.make_station_at_planet(planet, elements, universe)
        self.make_station_at_planet(planet2, elements, universe)




    def tests(self, universe, elements):
        p0 = Particle.Mass(universe)
        p0.set_location((0,0))
        p0.set_velocity(0, 0)
        elements.append(p0)

        if False: # First test
            p1 = Particle.Mass(universe)
            p1.enter_orbit(p0, 100, 0, 0.01)
            elements.append(p1)

            p2 = Particle.Mass(universe)
            p2.enter_orbit(p1, 100, math.pi/2, -0.02)
            elements.append(p2)

            p1 = Particle.Mass(universe)
            p1.enter_orbit(p0, 100, math.pi, -0.01)
            elements.append(p1)

            p2 = Particle.Mass(universe)
            p2.enter_orbit(p1, 100, math.pi/2*3, 0.02)
            elements.append(p2)

        if False: # Test 2
            create_orbiting_particles_equi(universe, elements, p0, 1, 200, random.random()*math.pi/2, 0.01, 8)

        if True: # Test 3
            create_orbiting_particles_equi(universe, elements, p0, 3, 200, random.random()*math.pi/2, 0.0001, 8)
