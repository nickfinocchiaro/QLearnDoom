#!/usr/bin/env python
#
# Authors: Nicholas Finocchiaro and Brian Thomas
#
# We have extended this code to suit the needs of our 
# artificial intelligence final project. A ViZDOOM q-learner.
# 
#
# all licensing information can be found here:
# https://github.com/Marqt/ViZDoom#cite-as
#

#####################################################################
# This script presents how to use the most basic features of the environment.
# It configures the engine, and makes the agent perform random actions.
# It also gets current state and reward earned with the action.
# <episodes> number of episodes are played. 
# Random combination of buttons is chosen for every action.
# Game variables from state and last reward are printed.
#
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from __future__ import print_function

from vizdoom import *

from random import choice
from time import sleep
from qlearningAgent import *

import itertools as it
import sys

# Create DoomGame instance. It will run the game and communicate with you.
game = DoomGame()

# Now it's time for configuration!
game.load_config("../../examples/config/basic.cfg")

# Sets resolution. Default is 320X240
game.set_screen_resolution(ScreenResolution.RES_160X120)

# Enables depth buffer.
game.set_depth_buffer_enabled(True)

# Enables labeling of in game objects labeling.
game.set_labels_buffer_enabled(True)

# Enables buffer with top down map of the current episode/level.
game.set_automap_buffer_enabled(True)

# Adds game variables that will be included in state.
"""
game.add_available_game_variable(GameVariable.KILLCOUNT)
game.add_available_game_variable(GameVariable.ITEMCOUNT)
game.add_available_game_variable(GameVariable.SECRETCOUNT)
game.add_available_game_variable(GameVariable.FRAGCOUNT)
game.add_available_game_variable(GameVariable.DEATHCOUNT)
game.add_available_game_variable(GameVariable.HEALTH)
game.add_available_game_variable(GameVariable.ARMOR)
game.add_available_game_variable(GameVariable.DEAD)
game.add_available_game_variable(GameVariable.ON_GROUND)
game.add_available_game_variable(GameVariable.ATTACK_READY)
game.add_available_game_variable(GameVariable.SELECTED_WEAPON)
game.add_available_game_variable(GameVariable.SELECTED_WEAPON_AMMO)
game.add_available_game_variable(GameVariable.AMMO0)
game.add_available_game_variable(GameVariable.AMMO1)
game.add_available_game_variable(GameVariable.AMMO2)
game.add_available_game_variable(GameVariable.AMMO3)
game.add_available_game_variable(GameVariable.AMMO4)
game.add_available_game_variable(GameVariable.AMMO5)
game.add_available_game_variable(GameVariable.AMMO6)
game.add_available_game_variable(GameVariable.AMMO7)
game.add_available_game_variable(GameVariable.AMMO8)
game.add_available_game_variable(GameVariable.AMMO9)
game.add_available_game_variable(GameVariable.WEAPON0)
game.add_available_game_variable(GameVariable.WEAPON1)
game.add_available_game_variable(GameVariable.WEAPON2)
game.add_available_game_variable(GameVariable.WEAPON3)
game.add_available_game_variable(GameVariable.WEAPON4)
game.add_available_game_variable(GameVariable.WEAPON5)
game.add_available_game_variable(GameVariable.WEAPON6)
game.add_available_game_variable(GameVariable.WEAPON7)
game.add_available_game_variable(GameVariable.WEAPON8)
game.add_available_game_variable(GameVariable.WEAPON9)
game.add_available_game_variable(GameVariable.POSITION_X)
game.add_available_game_variable(GameVariable.POSITION_Y)
game.add_available_game_variable(GameVariable.POSITION_Z)
"""

# Turns on the sound. (turned off by default)
game.set_sound_enabled(True)

# Initialize the game. Further configuration won't take any effect from now on.
#game.set_console_enabled(True)
game.init()

# Define some actions. Each list entry corresponds to declared buttons:
# MOVE_LEFT, MOVE_RIGHT, ATTACK
actions = [[True, False, False], [False, True, False], [False, False, True]]


# Run this many episodes
episodes = 30

# Sets time that will pause the engine after each action (in seconds)
# Without this everything would go too fast for you to keep track of what's happening.
sleep_time = 1 / DEFAULT_TICRATE # = 0.028


screen_width = game.get_screen_width()
screen_height = game.get_screen_height()
resolution = (screen_width, screen_height)
agent = ApproximateQAgent()


def distance(pos1, pos2):
    # Objects received in form [x, y, z] coordinates

    # Find the sum of the squares
    sumOfSquares = 0
    for i in range(0, 3):
        sumOfSquares += pow(pos1[i] - pos2[i], 2)
        
    # Return the square root of the sum of the squares.
    return math.sqrt(sumOfSquares)


def objectCoordinates(buffers):
    # Input:  game.get_state()
    # Output: a dictionary of coordinates of objects with
    #         game.get_state().labels.value as keys

    coordinates = {}
    for l in buffers.labels:
        coordinates[l.value] = [l.object_position_x,
                                l.object_position_y,
                                l.object_position_z]

    return coordinates


def objectDistances(buffers):
    # Input:  game.get_state()
    # Output: a dictionary of distances of objects with
    #         game.get_state().labels.value as keys

    coordinates = {}
    for l in buffers.labels:
        coordinates[l.value] = [l.object_position_x,
                                l.object_position_y,
                                l.object_position_z]

    gv = buffers.game_variables

    distances = {}

    
    for key in list(coordinates.keys()):
        distances[key] = distance(coordinates[key], coordinates[255])
                
    return distances


def extractObjects(buffers, resolution):
    coordinates = objectCoordinates(buffers)    
    labels_buf  = buffers.labels_buffer
    
    # Objects dictionary data: [leftmost pixel, rightmost pixel, object coords]
    objects     = {}
    
    if labels_buf == None:
        return objects
    else:
        # Examine every cell of the buffer.
        for row in range(0, screen_height):
            for col in range(0, screen_width):
                value = labels_buf[row][col]
                # If it has a value other than 0 (0 == No object seen)
                if not (value == 0):

                    # If the object isn't in the dictionary, add it.
                    if not value in list(objects.keys()):
                        objects[value] = [col, col, coordinates[value]]

                    # Otherwise, update the left or right most pixel location.
                    else:
                        left, right, coords = objects[value]
                        if col < left:
                            objects[value] = [col, right, coords]
                        elif col > right:
                            objects[value] = [left, col, coords]

        return objects


def getGameState(game):
    game_state   = game.get_state()
    
    return (game_state,
            extractObjects(game_state, resolution),
            actions,
            resolution,
            game_state.game_variables,
            game.is_episode_finished())



for i in range(episodes):
    print("Episode #" + str(i + 1))

    # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
    game.new_episode()
    
    old_position = None
    while not game.is_episode_finished():

        ##############################
        """ *** BEGIN OUR CODE *** """
        ##############################
    
        state        = getGameState(game)

        action       = agent.getAction(state)

        reward       = game.make_action(action)

        nextState    = getGameState(game)

        agent.update(state, action, nextState, reward)
                    
        ###############################
        """ *** END OF OUR CODE *** """
        ###############################

    if sleep_time > 0:
        sleep(sleep_time)

    # Check how the episode went.
    print("Episode finished.")
    print("Total reward:", game.get_total_reward())
    print("************************")

# It will be done automatically anyway but sometimes you need to do it in the middle of the program...
game.close()
