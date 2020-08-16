# coding=utf-8
# @TheWorldFoundry

import pygame
import math
import random

import Display
import Particle
import Universe

import Planet
import Station
import Ship

def create_orbiting_particles_equi(universe, elements, central, numParticles, distance, base_angle, velocity, recurse):
    if recurse > 0:
        angle_delta = math.pi*2.0/numParticles
        for i in xrange(0, numParticles):
            pNew = Particle.Mass(universe)
            pNew.invisible = True
            if recurse == 1:
                pNew.invisible = False
            pNew.enter_orbit(central, distance, base_angle+angle_delta*i, velocity)
            elements.append(pNew)
            create_orbiting_particles_equi(universe, elements, pNew, numParticles, int(distance/3*2), random.random()*math.pi/2, -velocity*2.2, recurse-1)



def game_loop():
    # Initialisation
    universe = Universe.Universe()
    display = Display.View(universe, (1800,1000), (0,0))
    elements = []

    if False:
        tests(universe, elements)

    universe.setup_start_area(elements, display)


    # Main loop
    keepGoing = True
    iterationCount = 0

    selected = {}
    targeted = {}
    mousepos = -999,-999 # Default
    while keepGoing:
        # DEBUG - Increment the scaling factor to test the various co-ordinate system mappings
        if iterationCount % 1000 == 0:
            print "Number of ships",len(elements)
        #    display.set_scale(display.scale+scalechange)
        #    if abs(display.scale) >= 10:
        #        scalechange = -scalechange
        iterationCount += 1

        # Tick the world
        newElements = []
        for e in elements:
            if e.mass.alive:
                e.update()
                newElements.append(e)
        elements = newElements

        # Draw the world
        display.draw(elements)

        for event in display.update():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEMOTION:
                mousepos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 1 == Left
                    for e in elements:
                        if e.mass.alive:
                            if( e.handle_click(event.pos, True) ):
                                selected[e.get_id()] = e # Keep a record of who is selected. Overwrite duplicates.
                                break
                elif event.button == 2:  # 2 == Centre - Pick
                    for e in elements:
                        if e.mass.alive:
                            if( e.handle_pickclick(event.pos, False) ):
                                display.focus_object = e
                if event.button == 3:  # 3 == Right
                    for e in elements:
                        if e.mass.alive:
                            if( e.handle_rightclick(event.pos, True) ):
                                targeted[e.get_id()] = e # Keep a record of who is selected. Overwrite duplicates.
                                break
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p: # Pick
                    print "Pick"
                    for e in elements:
                        if e.mass.alive:
                            if( e.handle_click(mousepos, False) ):
                                display.focus_object = e
            else:
                print event # Placeholder

        # Handle AI commands

        #  We've been given a bunch of selected entities, and a bunch of targeted entities.
        #  Check if there's a new command to be added to the selected and targeted lists
        #  After processing, clear the lists

        clear_targets = False
        for key in selected:
            e = selected[key]
            if isinstance(e, Ship.Ship):
                for key_tgt in targeted:
                    t = targeted[key_tgt]
                    if isinstance(t, Planet.World) or isinstance(t, Station.Station):
                        if t not in e.trade_targets:
                            e.move_target_current = t

                            # e.trade_targets.append(t)
                            clear_targets = True
                            e.mass.selected = False
                            t.mass.targeted = False
                    elif isinstance(t, Ship.Ship):
                            e.move_target_current = t
                            clear_targets = True
                            e.mass.selected = False
                            t.mass.targeted = False
                # print e.mass.id, e.trade_targets
        if clear_targets:
            targeted = {}
            selected = {}

if __name__ == '__main__':
    game_loop()

