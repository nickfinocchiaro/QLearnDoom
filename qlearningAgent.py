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
import random, util, extractor, math

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

        featureVector = extractor.getFeatures(state, action)
        
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
        buffers, objects, all_actions, res, gvars, isTerminal, scenario = state
        
        maxQValue = float('-inf')

        # If the state is a terminal state, return 0.0
        if isTerminal:
            return 0.0

        # Determine the maximum q value for all actions
        for a in all_actions:
            maxQValue = max(maxQValue, self.getQValue(state, a))

        # Return the maximum q value
        return maxQValue

    def computeActionFromQValues(self, state):
        """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """
        buffers, objects, all_actions, res, gvars, isTerminal, scenario = state

        maxQValue  = self.computeValueFromQValues(state)
        maxActions = []

        # If the state is a terminal state, return None
        if isTerminal:
            return None

        # Make a list of all actions that have qVal = maxQVal
        for a in all_actions:
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

        buffers, objects, all_actions, res, gvars, isTerminal, scenario = state
        
        # if state == 'TERMINAL STATE': return None
        if isTerminal:
            return action

        # If the action taken is to be random:
        if util.flipCoin(self.epsilon):
            action = random.choice(all_actions)

        # Otherwise, compute the best action from the q values.
        else:
            action = self.computeActionFromQValues(state)
        
        return action


    def update(self, state, action, nextState, reward):
        """
        Update weights based off on transition
        """
        buffers, objects, all_actions, res, gvars, isTerminal, scenario = state
        
        # Calculate "difference", to be used in weight calculation
        maxQ  = self.computeValueFromQValues(nextState)
        Qsa   = self.getQValue(state, action)

        difference = (reward + self.gamma * maxQ) - Qsa

        # Update weights
        featureVector = extractor.getFeatures(state, action)
        featureKeys   = featureVector.sortedKeys()
        weightKeys    = self.weights.sortedKeys()

        for fkey in featureKeys:
            self.weights[fkey] = (self.weights[fkey] +
                                  self.alpha * difference *
                                  featureVector[fkey])

