from vizdoom import *
import util

class ApproximateQAgent():
    def __init__(self, **args):
        self.weights = util.Counter()

    def getQValue(self, state, action):
        """
        Returns Q(state, action)
        Should return 0.0 if we have never seen a state
        or the Q node value otherwise
        """

        #FUNCTION STUB
        
        return 0

    def computeValueFromQValues(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """

        #FUNCTION STUB
         
        return 0

    def computeActionFromQValues(self, state):
        """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """

        #FUNCTION STUB
        
        return 0

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

        #FUNCTION STUB

        return 0



    def isTerminal(self, state):
        """
        Determines if a state is a terminal state
        """

        #FUNCTION STUB

        return 0


    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here
        
        NOTE: You should never call this function,
        it will be called on your behalf
        """

        #FUNCTION STUB

        return 0
               
    def getFeatures(self, state, action):
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

        vars = state.game_variables

        print "Game Variables:", vars
