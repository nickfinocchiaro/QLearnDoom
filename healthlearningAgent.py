################################################################################
################################################################################
# This file is no longer needed to run health.py. Use qlearningAgent.py instead.
################################################################################
################################################################################


from vizdoom import *
import random, util, math

class ApproximateQAgent():
    def __init__(self, **args):

        self.weights = util.Counter()
        self.epsilon = 0.05
        self.gamma   = 1
        self.alpha   = 0.4
        

    def stopTraining(self):
        self.alpha = 0.0
        self.epsilon = 0.0

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
        buffers, objects, actions, res, gvars, isTerminal = state

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

        if len(maxActions) == 0:
            return random.choice(actions)
        else:
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

        buffers, objects, actions, res, gvars, isTerminal = state
        
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


    def update(self, state, action, nextState, reward):
        """
        Update weights based off on transition
        """
        buffers, objects, actions, res, gvars, isTerminal = state
        
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
              
        features   = util.Counter()

        objectKeys = list(objects.keys())

        features["bias"] = 1.0

        left, right, forward = action
        
        health_list = []
        for key in objectKeys:
            name, dist = objects[key]
            if name == 'Medikit':
                health_list.append(dist)


        # Are health visible?
        if len(health_list) > 0:
            features["health-on-screen"] = 1.0
        else:
            features["health-on-screen"] = 0.0

        # How many health visible?
        #features["#-health-visible"] = len(health_list)

        
        # Add closest health feature
        if not health_list == []:
            closest_health = min(health_list)
            features["closest-health"] = closest_health
        else:
            features["closest-health"] = 10000

        #if not buffers.game_variables == None:
        #    features["health"] = buffers.game_variables[0]
    

            
        """
        # Max depth feature
        depth_buf = buffers.depth_buffer
        if not depth_buf == None:
            max_list = map(max, depth_buf)
            features["max-depth"] = max(max_list)
            #print("max_depth: ", max(max_list))
            

        print("LABELS")
        for l in buffers.labels:
            print("Object id:", l.object_id,
                  "object name:", l.object_name, "label:", l.value)

            #print("Object position X:", l.object_position_x,
            #      "Y:", l.object_position_y, "Z:", l.object_position_z)

        
        # Number of health within 50 distance
        #features['health-within-50'] = 0
        #for key in objectKeys:
        #    if objects[key] <= 50:
        #        features['health-within-50'] += 1

        
        # Closest health
        #if len(objectKeys) > 0:
        #    closest = float('inf')
        #    for key in objectKeys:
        #        if objects[key] < closest:
        #            closest = objects[key]
        #    features['closest-health'] = closest


        # Distance to all objects
        for key in objectKeys:    
            distance, name = objects[key]   
            features['distance-to-obj-' + str(key)] = distance

        # Amount of health left
        #if not buffers.game_variables == None:
        #    health = buffers.game_variables[0]
        #    features['health'] = health
        """
        
        return features

        
        


