from vizdoom import *
import util

class ApproximateQAgent():
    def __init__(self, **args):
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights
        
    def getQValue(self, state, features, action):
        """
        Returns Q(state, action)
        Should return 0.0 if we have never seen a state
        or the Q node value otherwise
        """
        keys = features.sortedKeys()
        qSum = 0
        for key in keys:
            qSum += self.getWeights()[key] * features[key]

        return qSum


    def computeValueFromQValues(self, state, actions):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """

        maxQValue = float('-inf')

        # If the state is a terminal state, return 0.0
        if self.isTerminal(state):
            return 0.0

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

        # if state == 'TERMINAL STATE': return None
        if self.isTerminal(state):
            return action

        # If the action taken is to be random:
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)

        # Otherwise, compute the best action from the q values.
        else:
            action = self.computeActionFromQValues(state)

        return action

        



    def isTerminal(self, state):
        """
        Determines if a state is a terminal state
        """
        
        return game.is_episode_finished() # Nick


    def update(self, state, features, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here
        
        NOTE: You should never call this function,
        it will be called on your behalf
        """

        # Calculate "difference", to be used in weight calculation
        gamma = self.discount
        maxQ  = self.computeValueFromQValues(nextState)
        Qsa   = self.getQValue(state, action)

        difference = (reward + gamma * maxQ) - Qsa

        # Update weights
        featureKeys = features.sortedKeys()
        weightKeys  = self.weights.sortedKeys()

        for fkey in featureKeys:
            self.weights[fkey] = (self.weights[fkey] +
                                  self.alpha * difference *
                                  features[fkey])
               
    def getFeatures(self, state, objects, action):
        """
        Returns simple features for a basic reflex Pacman:
        - whether food will be eaten
        - how far away the next food is
        - whether a ghost collision is imminent
        - whether a ghost is one step away
        """

        #FUNCTION STUB
        features = util.Counter()

        features["bias"] = 1.0

        objectKeys = features.sortedKeys()
        
        if 127 in objectKeys: num = 1
        else: num = 0
        features["#-of-enemies"] = num


        return features
