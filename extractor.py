#
# Authors: Brian Thomas and Nick Finocchiaro
#
# Last Updated: 11/26/2016
#
# Feature extractors for an approximate q-learning agent in a ViZDoom project.
#

from vizdoom import *
import time, util, doomUtils

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

    elif scenario == "defend the center":
        return getDefendTheCenterFeatures(state, action)


    
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
        if obj_name == 'DoomImp':
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
    



def getHealthGatheringSupremeFeatures(state, action):
    features   = util.Counter()
    
    buffers, objects, all_actions, prev_action, res, isTerminal, scenario = state
    
    screen_width, screen_height = res
    
    objectKeys = list(objects.keys())
        
    # Am I turning or moving forward?
    turning_left, turning_right, moving_forward = action
    turning = turning_left or turning_right

    # Separate objects into medikits and poisons
    medikits = {}
    poisons  = {}
    for key in objectKeys:
        if (objects[key][5] == "CustomMedikit") or (objects[key][5] == "Medikit"):
            medikits[key] = objects[key]
        elif objects[key][5] == "Poison":
            poisons[key] = objects[key]

    # Are medikits and poisons visible?
    mKeys = list(medikits.keys())
    pKeys = list(poisons.keys())
    medikits_visible = poisons_visible = False
    if not len(mKeys) == 0:
        medikits_visible = True

    if not len(pKeys) == 0:
        poisons_visible  = True

    # Which medikit is closest?
    closest_medikit = (None, float('inf'))
    for key in mKeys:
        left, right, coords, dist, obj_id, obj_name = objects[key]
        if dist < closest_medikit[1]:
            closest_medikit = (key, dist)
            

    # Which poison is closest?
    closest_poison = (None, float('inf'))
    for key in pKeys:
        left, right, coords, dist, obj_id, obj_name = objects[key]
        if dist < closest_poison[1]:
            closest_poison = (key, dist)

 
    center = screen_width / 2        
    # Is the closest medikit to the left, center, or right?
    if medikits_visible:
        medikit_left = medikit_center = medikit_right = False
        left, right, coords, dist, obj_id, obj_name = medikits[closest_medikit[0]]
        if center in range(0, left):
            medikit_right  = True
        elif center in range(left, right):
            medikit_center = True
        elif center in range(right, screen_width):
            medikit_left   = True


    # Is the closest poison to the left, center, or right?
    if poisons_visible:
        poison_left = poison_center = poison_right = False
        left, right, coords, dist, obj_id, obj_name = poisons[closest_poison[0]]
        if center in range(0, left):
            poison_right  = True
        elif center in range(left, right):
            poison_center = True
        elif center in range(right, screen_width):
            poison_left   = True


    # average depth on left and right sides
    depth_buf = buffers.depth_buffer
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

    # Am I blocked on the left or right?
    blocked_by_walls = blocked_on_left = blocked_on_right = False
    if left_depth < 5:
        blocked_on_left = True
    if right_depth < 5:
        blocked_on_right = True
    blocked_by_walls =  blocked_on_left or blocked_on_right


    poison_too_close = False
    if closest_poison[1] < 70:
        poison_too_close = True

         
    # If a poison is too close
    if poison_too_close:
        if poison_left and turning_right and (not moving_forward):
            features["avoiding-poison"] = 10
        if poison_right and turning_left and (not moving_forward):
            features["avoiding-poison"] = 10
            
    # If medikits are visible, and I'm not blocked  am I moving towards them?
    if medikits_visible and (not blocked_by_walls):
        if medikit_left and turning_left:
            features["moving-toward-health"] = 1
        if medikit_center and moving_forward and not turning:
            features["moving-toward-health"] = 1
        if medikit_right and turning_right:
            features["moving-toward-health"] = 1

    # If medikits are visible and I'm blocked, am I moving around the walls?
    elif medikits_visible and blocked_by_walls:
        if left_side_open and turning_left:
            features["avoiding-walls"] = 1
        elif right_side_open and turning_right:
            features["avoiding-walls"] = 1
            
    # If no medikits are visible, am I turning to find medikits?
    elif not medikits_visible:
        features["finding-health"] = 0
        if left_side_open and turning_left:
            features["finding-health"] = 1
        if right_side_open and turning_right:
            features["finding-health"] = 1
        
    return features



def getDefendTheCenterFeatures(state, action):
    buffers, objects, all_actions, prev_action, res, isTerminal, scenario = state
    
    screen_width, screen_height = res
    
    center_screen  = int(screen_width / 2)
    
    features   = util.Counter()

    turning_left, turning_right, shooting = action
    

    
    # Separate objects into different categories
    marines = []
    demons  = []
    for key in objects:
        left, right, coords, dist, obj_id, obj_name = objects[key]
        if obj_name == "MarineChainsaw":
            marines.append(objects[key])

        elif obj_name == "Demon":
            demons.append(objects[key])


    # Are marines or demons visible?
    marines_visible = demons_visible = False
    if len(marines) > 0:
        marines_visible = True
    if len(demons) > 0:
        demons_visible = True


    # Which marine is closest?
    closest_marine = None
    if marines_visible:
        closest_marine = marines[0]
        for m in marines:
            left, right, coords, dist, obj_id, obj_name = m
            if dist < closest_marine[3]:
                closest_marine = m

    # Which demon is closest?
    closest_demon = None
    if demons_visible:
        closest_demon = demons[0]
        for d in demons:
            left, right, coords, dist, obj_id, obj_name = d
            if dist < closest_demon[3]:
                closest_demon = d

    # is there a big threat on the screen?
    big_threat = None
    if marines_visible and closest_marine[3] < 300:
        big_threat = closest_marine
        
    if demons_visible  and closest_demon[3]  < 400:
        big_threat = closest_demon


    if big_threat == None:
        threatened = False
    else:
        threatened = True

     
    # If there is a big threat, is it to the left, center, or right?
    threat_left = threat_center = threat_right = False
    if threatened:
        left, right, coords, dist, obj_id, obj_name = big_threat
        # If an enemy is to the right
        if center_screen in range(0, left):
            threat_right = True
        # If an enemy is in my sights? (center)
        elif center_screen in range(left, right):
            threat_center = True
        # If an enemy is to the right?
        elif center_screen in range(right, screen_width):
            threat_left = True


    ammo_remaining = False
    if buffers.game_variables[0] > 0:
        ammo_remaining = True

    if ammo_remaining:
        if threat_left and turning_left:
            features["moving-toward-threat"] = 1
        if threat_right and turning_right:
            features["moving-toward-threat"] = 1

        
        if threat_center and shooting:
            features["moving-toward-threat"] = 1
            features["shot-at-threat"] = 1
            features["looking-for-threats"] = 1

    
        
        if (not threatened) and turning_left:
            features["looking-for-threats"] = 1


    
 
    return features