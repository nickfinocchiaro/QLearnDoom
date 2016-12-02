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
    buffers, objects, all_actions, prev_action, res, isTerminal, scenario = state

    if scenario == "basic":
        return getBasicFeatures(state, action)
    
    elif scenario == "health":
        return getHealthFeatures(state, action)

    elif scenario == "defend the line":
        return getDefendTheLineFeatures(state, action)

    elif scenario == "health gathering supreme":
        return getHealthGatheringSupremeFeatures(state, action)



    
def getBasicFeatures(state, action):
    buffers, objects, all_actions, prev_action, res, isTerminal, scenario = state
    
    screen_width, screen_height = res
    
    center_screen  = screen_width / 2
    
    features   = util.Counter()

    moving_left, moving_right, shooting = action
    
    objectKeys = list(objects.keys())
    
    
    enemy_left   = False
    enemy_center = False
    enemy_right  = False


    # Determine if there are enemies to the left, right, and center
    for key in objectKeys:
        left, right, coords, dist, obj_id, obj_name = objects[key]
        # Ignore if the object is self (value of self is 255).
        if obj_name == 'Cacodemon':
            # If an enemy is to the right
            if center_screen in range(0, left):
                enemy_right = True
            # If an enemy is in my sights? (center)
            if center_screen in range(left, right):
                enemy_center = True
            # If an enemy is to the right?
            if center_screen in range(right, screen_width):
                enemy_left = True
                

    # Am I moving in the wrong direction?
    if enemy_left and moving_right:
        features["moving-in-wrong-direction"] = 1
    if enemy_right and moving_left:
        features["moving-in-wrong-direction"] = 1
            
    # Did I shoot at nothing? If yes, value is 1. No, value is 0.
    # List all actions that shoot.
    if (not enemy_center) and shooting:
        features["shot-at-nothing"] = 1
    else:
        features["shot-at-nothing"] = 0

            
    return features


                
def getHealthFeatures(state, action):
    features   = util.Counter()
    
    buffers, objects, all_actions, prev_action, res, isTerminal, scenario = state
    
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

        
    # What is the closest medikit?
    closest_medikit = (None, float('inf'))
    for key in objectKeys:
        left, right, coords, dist, obj_id, obj_name = objects[key]
        if dist < closest_medikit[1]:
            closest_medikit = (key, dist)

    # If there is a medikit that's closest.
    if not (closest_medikit[0] == None):
        # Is the closest medikit to the left, center, or right?
        medikit_left = medikit_center = medikit_right = False
        center = screen_width / 2
        obj_left  = objects[closest_medikit[0]][0]
        obj_right = objects[closest_medikit[0]][1]
        if center in range(0, obj_left):
            medikit_right  = True
        elif center in range(obj_left, obj_right):
            medikit_center = True
        elif center in range(obj_right, screen_width):
            medikit_left   = True

    # If medikits are visible, am I moving towards them?
    if medikits_visible:
        if medikit_left and turning_left:
            features["moving-toward-health"] = 1
        if medikit_center and moving_forward and not turning:
            features["moving-toward-health"] = 1
        if medikit_right and turning_right:
            features["moving-toward-health"] = 1

            
    # If no medikits are visible, am I turning to find medikits?
    if not medikits_visible:
        depth_buf = buffers.depth_buffer

        # average depth on left and right sides
        left_depth  = 0
        right_depth = 0
        for pixel in range(0, screen_height):
            left_depth += depth_buf[pixel][0]
            right_depth += depth_buf[pixel][screen_width - 1]
        left_depth  /= float(screen_height)
        right_depth /= float(screen_height)

        if right_depth > left_depth:
            right_side_open = True
            left_side_open  = False
        else:
            right_side_open = False
            left_side_open  = True
            
        features["finding-health"] = 0
        if turning_left and left_side_open:
            features["finding-health"] = 1
        if turning_right and right_side_open:
            features["finding-health"] = 1
            
        
    return features


def getDefendTheLineFeatures(state, action):
    ################################
    #FUNCTION STUB FOR NICK
    ###############################

    features = util.Counter()
    return features
    
def getHealthGatheringSupremeFeatures(state, action):
    ##################################
    #FUNCTION STUB FOR BRIAN
    ##################################

    features = util.Counter()
    return features
