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
from qlearningAgent import *

import itertools as it
import sys


# Create DoomGame instance. It will run the game and communicate with you.
game = DoomGame()


# Now it's time for configuration!
# load_config could be used to load configuration instead of doing it here with code.
# If load_config is used in-code configuration will work. Note that the most recent changes will add to previous ones.
# game.load_config("../../examples/config/basic.cfg")

# Sets path to ViZDoom engine executive which will be spawned as a separate process. Default is "./vizdoom".
game.set_vizdoom_path("../../bin/vizdoom")

# Sets path to iwad resource file which contains the actual doom game. Default is "./doom2.wad".
game.set_doom_game_path("../../scenarios/freedoom2.wad")
# game.set_doom_game_path("../../scenarios/doom2.wad")  # Not provided with environment due to licences.

# Sets path to additional resources wad file which is basically your scenario wad.
# If not specified default maps will be used and it's pretty much useless... unless you want to play good old Doom.
game.set_doom_scenario_path("../../scenarios/basic.wad")

# Sets map to start (scenario .wad files can contain many maps).
game.set_doom_map("map01")

# Sets resolution. Default is 320X240
#game.set_screen_resolution(ScreenResolution.RES_640X480)
game.set_screen_resolution(ScreenResolution.RES_160X120)

# Sets the screen buffer format. Not used here but now you can change it. Defalut is CRCGCB.
game.set_screen_format(ScreenFormat.RGB24)

# Enables depth buffer.
game.set_depth_buffer_enabled(True)

# Enables labeling of in game objects labeling.
game.set_labels_buffer_enabled(True)

# Enables buffer with top down map of the current episode/level.
game.set_automap_buffer_enabled(True)

# Sets other rendering options
game.set_render_hud(False)
game.set_render_minimal_hud(False) # If hud is enabled
game.set_render_crosshair(False)
game.set_render_weapon(True)
game.set_render_decals(False)
game.set_render_particles(False)
game.set_render_effects_sprites(False)

# Adds buttons that will be allowed. 
game.add_available_button(Button.MOVE_LEFT)
game.add_available_button(Button.MOVE_RIGHT)
game.add_available_button(Button.ATTACK)

# Adds game variables that will be included in state.
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
#game.add_available_game_variable(GameVariable.POSITION_X)
#game.add_available_game_variable(GameVariable.POSITION_Y)
#game.add_available_game_variable(GameVariable.POSITION_Z)



# Causes episodes to finish after 200 tics (actions)
game.set_episode_timeout(200)

# Makes episodes start after 10 tics (~after raising the weapon)
game.set_episode_start_time(10)

# Makes the window appear (turned on by default)
game.set_window_visible(True)

# Turns on the sound. (turned off by default)
game.set_sound_enabled(True)

# Sets the livin reward (for each move) to -1
game.set_living_reward(-1)

# Sets ViZDoom mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR, PLAYER mode is default)
game.set_mode(Mode.PLAYER)

# Initialize the game. Further configuration won't take any effect from now on.
#game.set_console_enabled(True)
game.init()

# Define some actions. Each list entry corresponds to declared buttons:
# MOVE_LEFT, MOVE_RIGHT, ATTACK
# 5 more combinations are naturally possible but only 3 are included for transparency when watching.
actions = [[True, False, False], [False, True, False], [False, False, True]]
#n = game.get_available_buttons_size()
#actions = [list(a) for a in it.product([0, 1], repeat=n)]


# Run this many episodes
episodes = 30

# Sets time that will pause the engine after each action (in seconds)
# Without this everything would go too fast for you to keep track of what's happening.
sleep_time = 1 / DEFAULT_TICRATE # = 0.028


screen_width = game.get_screen_width()
screen_height = game.get_screen_height()
resolution = (screen_width, screen_height)
agent = ApproximateQAgent()



def extractObjects(buffers, resolution):
    objects = util.Counter()
    screen_width, screen_height = resolution
    

    labels_buf = buffers.labels_buffer
    depth_buf  = buffers.depth_buffer

    temp = util.Counter()
    
    if not labels_buf == None:    
        # Extract objects from the labels buffer
        for row in range(0, screen_height):
            for col in range(0, screen_width):
                value = labels_buf[row][col]
                if not (value == 0 or value == 255):
                    depth = depth_buf[row][col]
                    if temp[value] == 0:
                        temp[value] = [col, col, row, depth]
                    else:
                        left, right, row, depth = temp[value]
                        if col < left:
                            temp[value] = [col, right, row, depth]
                        elif col > right:
                            temp[value] = [left, col, row, depth]
                            
        for key in temp.sortedKeys():
            left, right, y, depth = temp[key]
            center = int((left + right) / 2)
            width  = right - left 
            objects[key] = (center, width, y, depth)
                    # Create a Counter with 'value' as key
                    # and associated data is (x, y, depth)
                    #objects[value] = (col, row, depth)

    return objects


def getGameState(game):
    game_state = game.get_state()
    
    return (game_state,
            extractObjects(game_state, resolution),
            actions,
            resolution,
            game_state.game_variables,
            game.is_episode_finished())


print(resolution)
for i in range(episodes):
    print("Episode #" + str(i + 1))

    # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
    game.new_episode()

    while not game.is_episode_finished():

        ##############################
        """ *** BEGIN OUR CODE *** """
        ##############################
        
        # Gets the state
        state = getGameState(game)
        
        action    = agent.getAction(state)
        reward    = game.make_action(action)        

        nextState = getGameState(game)

        agent.update(state, action, nextState, reward)
                    
        
        ###############################
        """ *** END OF OUR CODE *** """
        ###############################

        
        # Makes a random action and get remember reward.
        #r = game.make_action(choice(actions))
        
        # Makes a "prolonged" action and skip frames:
        # skiprate = 4
        # r = game.make_action(choice(actions), skiprate)

        # The same could be achieved with:
        # game.set_action(choice(actions))
        # game.advance_action(skiprate)
        # r = game.get_last_reward()

	"""
        # Prints state's game variables and reward.
        print("State #" + str(n))
        print("Game variables:", vars)
        print("Reward:", r)
        print("=====================")
	"""
        if sleep_time > 0:
            sleep(sleep_time)

    # Check how the episode went.
    print("Episode finished.")
    print("Total reward:", game.get_total_reward())
    print("************************")

# It will be done automatically anyway but sometimes you need to do it in the middle of the program...
game.close()

