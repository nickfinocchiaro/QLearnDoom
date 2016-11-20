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
        #buffers, objects, actions = state
        featureVector = self.getFeatures(state, action)
        
        keys = featureVector.sortedKeys()
        qSum = 0
        for key in keys:
            qSum += self.getWeights()[key] * featureVector[key]

        return qSum


    def computeValueFromQValues(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        buffers, objects, actions, res, gvars = state
        
        maxQValue = float('-inf')

        # If the state is a terminal state, return 0.0
        #if self.isTerminal(game):
        #    return 0.0

        # Determine the maximum q value for all legal actions
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
        buffers, objects, actions, res, gvars = state

        maxQValue  = self.computeValueFromQValues(state)
        maxActions = []

        # If the state is a terminal state, return None
        #if self.isTerminal(game):
        #    return None

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

        HINT: You might want to use util.flipCoin(prob)
        HINT: To pick randomly from a list, use random.choice(list)
        """

        action = None

        buffers, objects, actions, res, gvars = state
        
        # if state == 'TERMINAL STATE': return None
        #if self.isTerminal(game):
        #    return action

        # If the action taken is to be random:
        if util.flipCoin(self.epsilon):
            action = random.choice(actions)

        # Otherwise, compute the best action from the q values.
        else:
            action = self.computeActionFromQValues(state)
        
        return action



    def isTerminal(self, game):
        """
        Determines if a state is a terminal state
        """
        return game.is_episode_finished() 

    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here
        
        NOTE: You should never call this function,
        it will be called on your behalf
        """
        buffers, objects, actions, res, gvars = state
        
        # Calculate "difference", to be used in weight calculation
        maxQ  = self.computeValueFromQValues(nextState)
        Qsa   = self.getQValue(state, action)

        difference = (reward + self.gamma * maxQ) - Qsa

        # Update weights
        featureVector = self.getFeatures(state, action)
        featureKeys = featureVector.sortedKeys()
        weightKeys  = self.weights.sortedKeys()

        for fkey in featureKeys:
            self.weights[fkey] = (self.weights[fkey] +
                                  self.alpha * difference *
                                  featureVector[fkey])
               
    def getFeatures(self, state, action):
        """
        Returns simple features for a basic reflex Pacman:
        - whether food will be eaten
        - how far away the next food is
        - whether a ghost collision is imminent
        - whether a ghost is one step away
        """

        buffers, objects, actions, res, gvars = state
        width, height = res

        halfwidth  = int (width / 2)
        buf        = 5
        
        features   = util.Counter()
        #features["bias"] = 1.0

        objectKeys = objects.sortedKeys()

        for key in objectKeys:
            if objects[key][0] in range(0, halfwidth - buf):
                features['enemy-on-left'] = 1.0
            elif objects[key][0] in range(halfwidth - buf, halfwidth + buf):
                features['enemy-at-center'] = 1.0
            elif objects[key][0] in range(halfwidth + buf, width):
                features['enemy-on-right'] = 1.0

        for idx, a in enumerate(action):
            if not a == 0:
                features['action-' + str(idx)] = 1.0
            
            
        return features

        
        


