#
# Authors: Brian Thomas
#
# Last Updated: 11/26/2016
#
# Feature extractors for an approximate q-learning agent in a ViZDoom project.
#

from vizdoom import *
import util, doomUtils

def getFeatures(state, action):
    buffers, objects, all_actions, res, gvars, isTerminal, scenario = state

    if scenario == "basic":
        return getBasicFeatures(state, action)
    
    elif scenario == "health":
        return getHealthFeatures(state, action)

def getBasicFeatures(state, action):
    buffers, objects, all_actions, res, gvars, isTerminal, scenario = state
    
    screen_width, screen_height = res
    
    center_screen  = screen_width / 2
    
    features   = util.Counter()
    #features["bias"] = 1.0
    
    objectKeys = list(objects.keys())
    
    #closestObject = float('inf')
    
    enemy_left   = False
    enemy_center = False
    enemy_right  = False


    # Determine if there are enemies to the left, right, and center
    for key in objectKeys:
        left, right, coords = objects[key]
        # Ignore if the object is self (value of self is 255).
        if not key == 255:
            # If an enemy is to the left
            if center_screen in range(0, left):
                enemy_left = True
            # If an enemy is in my sights? (center)
            if center_screen in range(left, right):
                enemy_center = True
            # If an enemy is to the right?
            if center_screen in range(right, screen_width):
                enemy_right = True
                

    # Am I moving in the correct direction?
    features["moving-in-correct-direction"] = 0
    if enemy_left and action == [True, False, False]:
        features["moving-in-correct-direction"] = 1
    if enemy_right and action == [False, True, False]:
        features["moving-in-correct-direction"] = 1
            
    # Did I shoot at nothing? If yes, value is 1. No, value is 0.
    # List all actions that shoot.
    shoot_actions = []
    for a in all_actions:
        if a[2] == True:
            shoot_actions.append(a)
                
    if (not enemy_center) and (action in shoot_actions):
        features["shot-at-nothing"] = 1
    else:
        features["shot-at-nothing"] = 0

            
    return features


                
def getHealthFeatures(state, action):
    features   = util.Counter()
    
        
    buffers, objects, actions, res, gvars, isTerminal, scenario = state
    
    screen_width, screen_height = res
    
    objectKeys = list(objects.keys())
        
    # Am I turning or moving forward?
    turning_left, turning_right, moving_forward = action
    turning = turning_left or turning_right

    # Are medikits visible?
    if len(objectKeys) == 0:
        medikits_visible = False
    else:
        medikits_visible = True

    # My position
    gv = buffers.game_variables
    my_pos = (gv[0], gv[1], gv[2])
            
    closest_medikit = (None, float('inf'))
    # What is the closest medikit?
    for key in objectKeys:
        distance_to_medikit = doomUtils.distance(my_pos, objects[key][2])
        if distance_to_medikit < closest_medikit[1]:
            closest_medikit = (key, distance_to_medikit)

    if not closest_medikit[0] == None:
        # Is the closest medikit to the left, center, or right?
        medikit_left   = False
        medikit_center = False
        medikit_right  = False
        center = screen_width / 2
        obj_left  = objects[closest_medikit[0]][0]
        obj_right = objects[closest_medikit[0]][1]
        if center in range(0, obj_left):
            medikit_right  = True
        elif center in range(obj_left, obj_right):
            medikit_center = True
        elif center in range(obj_right, screen_width):
            medikit_left   = True

    features["moving-toward-health"] = 0
    # Are Medikits visible?
    if medikits_visible:
        if medikit_left and turning_left:
            features["moving-toward-health"] = 1
        if medikit_center and moving_forward and not turning:
            features["moving-toward-health"] = 1
        if medikit_right and turning_right:
            features["moving-toward-health"] = 1
            
    # Else, no medikits are visible.
    else:
        # Am i turning (to find health)?
        if turning and not moving_forward:
            features["moving-toward-health"] = 1

        
            
        
    return features