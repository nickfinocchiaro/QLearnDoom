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
game.load_config("../../examples/config/basic.cfg")
scenario = "basic"

# Sets resolution. Default is 320X240
game.set_screen_resolution(ScreenResolution.RES_640X480)

# Enables depth buffer.
game.set_depth_buffer_enabled(True)

# Enables labeling of in game objects labeling.
game.set_labels_buffer_enabled(True)

# Enables buffer with top down map of the current episode/level.
game.set_automap_buffer_enabled(True)

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
episodes = 10

# Sets time that will pause the engine after each action (in seconds)
# Without this everything would go too fast for you to keep track of what's happening.
sleep_time = 1 / DEFAULT_TICRATE # = 0.028


screen_width = game.get_screen_width()
screen_height = game.get_screen_height()
resolution = (screen_width, screen_height)
agent = ApproximateQAgent()


for i in range(episodes):
    print("Episode #" + str(i + 1))
    if i == int(episodes / 2):
        agent.stopTraining()
        print("Ending training mode.")
        print("Entering testing mode.")
    

    
    # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
    game.new_episode()
    

    while not game.is_episode_finished():

        ##############################
        """ *** BEGIN OUR CODE *** """
        ##############################

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
