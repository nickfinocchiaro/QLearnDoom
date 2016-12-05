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
import doomUtils
import itertools as it
import sys

# Create DoomGame instance. It will run the game and communicate with you.
game = DoomGame()

# Now it's time for configuration!
game.load_config("../../examples/config/defend_the_line.cfg")
scenario = "defend the line"

# Sets resolution. Default is 320X240
game.set_screen_resolution(ScreenResolution.RES_320X240)

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
all_actions = [[True, False, False], [False, True, False],
               [False, False, True]]


# Run this many episodes
episodes = 30

# Sets time that will pause the engine after each action (in seconds)
# Without this everything would go too fast for you to keep track of what's happening.
sleep_time = 1 / DEFAULT_TICRATE # = 0.028


screen_width = game.get_screen_width()
screen_height = game.get_screen_height()
resolution = (screen_width, screen_height)
agent = ApproximateQAgent()


for i in range(episodes):
    print("Episode #" + str(i + 1))

    # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
    game.new_episode()
    

    while not game.is_episode_finished():

        ##############################
        """ *** BEGIN OUR CODE *** """
        ##############################

        for l in game.get_state().labels:
            print("Object id:", l.object_id, "object name:", l.object_name, "label:", l.value)
            print("Object position X:", l.object_position_x, "Y:", l.object_position_y, "Z:", l.object_position_z)

        state        = doomUtils.getGameState(game, scenario, all_actions)

        action       = agent.getAction(state)
        
        reward       = game.make_action(action)

        nextState    = doomUtils.getGameState(game, scenario, all_actions)

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
