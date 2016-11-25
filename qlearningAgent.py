# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# We Are extending this code from problem set 3 of the Berkeley problem sets
# for our ViZdoom AI project. Please see licensing information above. 
#
#

from vizdoom import *
import random, util, math

class ApproximateQAgent():
    def __init__(self, **args):

        self.weights = util.Counter()
        self.epsilon = 0.05
        self.gamma   = 0.8
        self.alpha   = 0.2
        
    def getWeights(self):
        return self.weights
        
    def getQValue(self, state, action):
        """
        Returns Q(state, action)
        Should return 0.0 if we have never seen a state
        or the Q node value otherwise
        """

        featureVector = self.getFeatures(state, action)
        
        keys = featureVector.sortedKeys()
        qSum = 0
        for key in keys:
            qSum += self.getWeights()[key] * featureVector[key]

        return qSum


    def computeValueFromQValues(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        buffers, objects, actions, res, gvars, isTerminal = state
        
        maxQValue = float('-inf')

        # If the state is a terminal state, return 0.0
        if isTerminal:
            return 0.0

        # Determine the maximum q value for all actions
        for a in actions:
            maxQValue = max(maxQValue, self.getQValue(state, a))

        # Return the maximum q value
        return maxQValue

    def computeActionFromQValues(self, state):
        """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """
        buffers, objects, actions, res, gvars, isTerminal = state#, dist = state

        maxQValue  = self.computeValueFromQValues(state)
        maxActions = []

        # If the state is a terminal state, return None
        if isTerminal:
            return None

        # Make a list of all actions that have qVal = maxQVal
        for a in actions:
            qVal = self.getQValue(state, a)
            if qVal == maxQValue:
                maxActions.append(a)

        return random.choice(maxActions)
                
    def getAction(self, state):
        """
        Compute the action to take in the current state.  With
        probability self.epsilon, we should take a random action and
        take the best policy action otherwise.  Note that if there are
        no legal actions, which is the case at the terminal state, you
        should choose None as the action.
        """

        action = None

        buffers, objects, actions, res, gvars, isTerminal = state#, dist = state
        
        # if state == 'TERMINAL STATE': return None
        if isTerminal:
            return action

        # If the action taken is to be random:
        if util.flipCoin(self.epsilon):
            action = random.choice(actions)

        # Otherwise, compute the best action from the q values.
        else:
            action = self.computeActionFromQValues(state)
        
        return action



    #def isTerminal(self, game):
        """
        Determines if a state is a terminal state
        """
        #return game.is_episode_finished() 

    def update(self, state, action, nextState, reward):
        """
        Update weights based off on transition
        """
        buffers, objects, actions, res, gvars, isTerminal = state#, dist = state
        
        # Calculate "difference", to be used in weight calculation
        maxQ  = self.computeValueFromQValues(nextState)
        Qsa   = self.getQValue(state, action)

        difference = (reward + self.gamma * maxQ) - Qsa

        # Update weights
        featureVector = self.getFeatures(state, action)
        featureKeys   = featureVector.sortedKeys()
        weightKeys    = self.weights.sortedKeys()

        for fkey in featureKeys:
            self.weights[fkey] = (self.weights[fkey] +
                                  self.alpha * difference *
                                  featureVector[fkey])
               
    def getFeatures(self, state, action):
        buffers, objects, actions, res, gvars, isTerminal = state
        
        screen_width, screen_height = res

        center_screen  = screen_width / 2
              
        features   = util.Counter()
        #features["bias"] = 1.0

        objectKeys = list(objects.keys())
        
        closestObject = float('inf')


        
        # Objects in range (at center of screen to be shot)
        enemy_left   = False
        enemy_center = False #_in_range = False
        enemy_right  = False

        for key in objectKeys:
            left, right, coords = objects[key]
            # Ignore if the object is self.
            if not key == 255:
                # Left
                if center_screen in range(0, left):
                    enemy_left = True
            
                # Center
                if center_screen in range(left, right):
                    enemy_center = True
                
                # Right
                if center_screen in range(right, screen_width):
                    enemy_right = True
                

        """
        for key in objectKeys:    
            x, width, y, depth = objects[key]
            offset = width / 2

            # Left
            if x in range(0, center - offset):
                enemy_left
            # Center
            if x in range(center - offset, center + offset):
                obj_in_range = True
        """
        # Am I moving in the wrong direction?
        features["moving-wrong-direction"] = 0
        if enemy_left and action == [True, False, False]:
            features["moving-wrong-direction"] = 1
        if enemy_right and action == [False, True, False]:
            features["moving-wrong-direction"] = 1
            
        # Did I shoot at nothing? If yes, value is 1. No, value is 0.
        if (not enemy_center) and (action == [False, False, True]):
            features["shot-at-nothing"] = 1
        else:
            features["shot-at-nothing"] = 0

        """
        # If no objects at center, does action move an object to the center?
        features["moves-obj-to-center"] = 0
        # If the object is already at center, assign 1 to this feature.
        if obj_in_range:
            features["moves-obj-to-center"] = 1
        else:
            
            for key in objectKeys:
                x, width, y, depth = objects[key]
                offset = width / 2

                if (x in range(0, center - offset) and
                    action == [False, True, False]):
                    features["moves-obj-to-center"] = 1
                if (x in range(center + offset, screen_width) and
                    action == [True, False, False]):
                    features["moves-obj-to-center"] = 1
        """
        
        """
        # 'shot-obj' either 1 or 0 if marine will shoot an object if taking
        # the action in the given state.
        if action == [False, False, True] and features['#-objs-at-center'] > 0:
            features['shot-obj'] = 1
        else:
            features['shot-obj'] = 0
        features.divideAll(10.0)
        """
        return features
