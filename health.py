#!/usr/bin/env python

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
#from healthlearningAgent import *
from qlearningAgent import *

import itertools as it
import math, doomUtils


# Create DoomGame instance. It will run the game and communicate with you.
game = DoomGame()

game.load_config("../../examples/config/health_gathering.cfg")

scenario = "health"
game.set_mode(Mode.PLAYER)
#game.set_ticrate(350)

# Enables buffers
game.set_labels_buffer_enabled(True)
game.set_depth_buffer_enabled(True)


# Initialize the game. Further configuration won't take any effect from now on.
#game.set_console_enabled(True)
game.init()

# Define some actions. Each list entry corresponds to declared buttons:
# MOVE_LEFT, MOVE_RIGHT, ATTACK
# 5 more combinations are naturally possible but only 3 are included for transparency when watching.
#actions = [[True, False, False], [False, True, False], [False, False, True]]
n = game.get_available_buttons_size()
all_actions = []
temp_actions = [list(a) for a in it.product([False, True], repeat=n)]
# Remove actions where you turn left and turn right at the same time
for a in temp_actions:
	if not (a[0] == True and a[1] == True):
		all_actions.append(a)	

#actions = [[True, False, False], [False, True, False], [False, False, True]]

# Run this many episodes
episodes = 20

# Sets time that will pause the engine after each action (in seconds)
# Without this everything would go too fast for you to keep track of what's happening.
sleep_time = 1 / DEFAULT_TICRATE # = 0.028


agent      = ApproximateQAgent()
resolution = (game.get_screen_width(), game.get_screen_height())
skiprate   = 1


for i in range(episodes):
    print("Episode #" + str(i + 1))
    if i > episodes / 2:
        agent.stopTraining()
        print("Ending training mode.")
        print("Entering testing mode.")
        
    # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
    game.new_episode()

    while not game.is_episode_finished():

        ##############################
        """ *** BEGIN OUR CODE *** """
        ##############################
        
        state = doomUtils.getGameState(game, scenario, all_actions)

        # Print health about every two seconds.
        if state[0].number % 60 == 0:
                print("Health: ", game.get_game_variable(GameVariable.HEALTH))
        
        action    = agent.getAction(state)

        reward    = game.make_action(action)        

        nextState = doomUtils.getGameState(game, scenario, all_actions)

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

