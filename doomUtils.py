#
# Authors: Brian Thomas
#
# Some utility functions for a q-learning ViZDoom project
#


from vizdoom import *
import itertools as it
import math


"""
# Function: distance
# ----------------------
# Computes the distance between two objects in three dimensional space
#
# pos1: a list of coordinates in three dimensions [x, y, z]
# pos2: same as pos1
#
# returns: the distance between the two coordinates
"""
def distance(pos1, pos2):
    # Find the sum of the squares
    sumOfSquares = 0
    for i in range(0, 3):
        sumOfSquares += pow(pos1[i] - pos2[i], 2)
        
    # Return the square root of the sum of the squares.
    return math.sqrt(sumOfSquares)

"""
# Function: objectCoordinates
# ----------------------------
# Compiles a dictionary of all objects from the labels buffer.
# Keys are the labels.vale and data is a list of the coordinates in
# three dimensional space.
#
# game_state: a ViZDoom game state (game.get_state())
#
# returns: A dictionary containing the coordinates for every object
#          in the labels buffer.
"""
def objectCoordinates(game_state):
    coordinates = {}
    for l in game_state.labels:
        coordinates[l.value] = [l.object_position_x,
                                l.object_position_y,
                                l.object_position_z]

    return coordinates

"""
# Function: objectDistances
# ---------------------------
# Computes the distances between all objects in the labels buffer and
# the marine (value == 255). Game variables for X, Y, and Z position
# must be the first three game variables added.
#
# game_state: a ViZDoom game state (game.get_state())
# my_pos:     The position of the marine as a tuple (X, Y, Z)
# 
# returns: A dictionary containing the distances to each object
#          from the marine.
"""
def objectDistances(game_state, my_pos):
    coordinates = objectCoordinates(game_state)
    distances = {}
    
    for key in list(coordinates.keys()):
        distances[key] = distance(coordinates[key], my_pos)
                
    return distances


"""
# Function: extractObjects
# ------------------------
# Examines the labels buffer and extracts all objects from it. Objects are
# stored in a dictionary in the form [leftmost pixel of object,
#                                     rightmost pixel of object,
#                                     object coordinates]
#
# game_state: a ViZDoom game state (game.get_state())
# resolution: a tuple of the resolution (width, height)
#
# returns: A dictionary containing all objects on the screen.
"""
def extractObjects(game_state, resolution, my_pos):
    screen_width, screen_height = resolution
    distances   = objectDistances(game_state, my_pos)
    coordinates = objectCoordinates(game_state)    
    labels_buf  = game_state.labels_buffer

    labels  = {}
    objects = {}
    
    for l in game_state.labels:
        labels[l.value] = (l.object_id, l.object_name)
        
    if labels_buf == None:
        return objects
    else:
        # Examine every cell of the buffer.
        for row in range(0, screen_height, 4):
            for col in range(0, screen_width, 4):
                value = labels_buf[row][col]
                # If it has a value other than 0 (0 == No object seen)
                if not (value == 0):

                    # If the object isn't in the dictionary, add it.
                    if not value in list(objects.keys()):
                        objects[value] = [col, col,            #left, right pixel
                                          coordinates[value],  # object coordinates
                                          distances[value],    # object distance
                                          labels[value][0],    # object id
                                          labels[value][1]]    # object name

                    # Otherwise, update the left or right most pixel location.
                    else:
                        left, right, coords, dist, obj_id, obj_name = objects[value]
                        if col < left:
                            objects[value] = [col, right, coords,
                                              dist, obj_id, obj_name]
                        elif col > right:
                            objects[value] = [left, col, coords,
                                              dist, obj_id, obj_name]

        return objects


"""
# Function: getGameState
# ------------------------
# Extracts the state of the game from a ViZDoom game object.
#
# game: a ViZDoom game object
# scenario: The game scenario as a string. ("basic" or "health")
# all_actions: a list of all possible actions the marine can take.
# 
# returns: The state of the game in tuple form, consisting of the game state
#          information returned from ViZDoom's get_state(), all objects on
#          screen, a list of possible actions, the resolution, the game
#          variables, if you're in a terminal state, and the game scenario.
"""
def getGameState(game, scenario, all_actions):
    gs = game.get_state()
    resolution = (game.get_screen_width(), game.get_screen_height())

    my_pos = (game.get_game_variable(GameVariable.POSITION_X),
              game.get_game_variable(GameVariable.POSITION_Y),
              game.get_game_variable(GameVariable.POSITION_Z))

    prev = game.get_last_action()
    
    return (gs,                             #ViZDoom game state
            extractObjects(gs, resolution, my_pos), #Dictionary of visible objects
            all_actions,                    #All possible actions
            prev,                           #Last action performed
            resolution,                     #Resolution of the game screen
            game.is_episode_finished(),     #Terminal state?
            scenario)                       #The game scenario
