# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    # def minimax(self, state):
    #     depth = 0
    #
    #     self.
    #
    # # Pacman's moves
    # def maxValue(self, state, depth):
    #     moves = state.getLegalActions(0)
    #
    #     if self.terminalTest(state, depth, moves):
    #         return self.evaluationFunction(state)
    #
    #     utility = max([minValue(succState, )])
    #
    # # # Ghosts' moves
    # # def minValue(self, state, depth):
    # #     allMoves = [[state.getLegalActions(enemyIndex)] for enemyIndex in range(1, state.getNumAgents()-1)]
    # #
    # #     utility = min([state.generateSuccessor(state.generateSuccessor()) for moves in allMoves])
    # #     return utility
    #
    # def minValue(self, ):
    #
    # def terminalTest(self, state, depth, moves):
    #     if depth == self.depth or state.isWin() or not moves:
    #         return True
    #     return False




class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState)

    def minimax(self, gameState):
        depth = 0
        legal_moves = gameState.getLegalActions(0)

        v = max([(move, self.min_value(gameState.generateSuccessor(0, move), depth, 1)) for move in legal_moves],
                key=lambda x: x[1])
        return v[0]

    def max_value(self, gameState, depth):
        legal_moves = gameState.getLegalActions(0)

        if self.terminal_test(gameState, depth, legal_moves):
            return self.evaluationFunction(gameState)

        v = max([self.min_value(gameState.generateSuccessor(0, move), depth, 1) for move in legal_moves])
        return v

    def min_value(self, gameState, depth, ghostIndex):
        legal_moves = gameState.getLegalActions(ghostIndex)

        if self.terminal_test(gameState, depth, legal_moves):
            return self.evaluationFunction(gameState)

        if ghostIndex == gameState.getNumAgents()-1:
            return min([self.max_value(gameState.generateSuccessor(ghostIndex, move), depth + 1) for move in legal_moves])
        else:
            return min([self.min_value(gameState.generateSuccessor(ghostIndex, move), depth, ghostIndex + 1) for move in legal_moves])

    def terminal_test(self, gameState, depth, legal_moves):
        if depth == self.depth or gameState.isWin() or gameState.isLose() or not legal_moves:
            return True
        return False


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.ab_search(gameState)

    # --------------------------a-b algorithm----------------------------------
    def ab_search(self, gameState):
        depth = 0

        a = float('-inf')
        b = float('inf')

        legal_moves = gameState.getLegalActions(0)
        v_list = []

        for move in legal_moves:
            score = self.min_value(gameState.generateSuccessor(0, move), a, b, 1, depth)
            v_list.append((move, score))

            a = max(max(v_list, key=lambda x: x[1])[1], a)

        return max(v_list, key=lambda x: x[1])[0]

    def max_value(self, gameState, a, b, depth):
        legal_moves = gameState.getLegalActions(0)

        if self.terminal_test(gameState, depth, legal_moves):
            return self.evaluationFunction(gameState)

        v = float('-inf')
        for move in legal_moves:
            v = max(v, self.min_value(gameState.generateSuccessor(0, move), a, b, 1, depth))

            if v > b:
                return v

            a = max(a, v)

        return v

    def min_value(self, gameState, a, b, ghostIndex, depth):
        legal_moves = gameState.getLegalActions(ghostIndex)

        if self.terminal_test(gameState, depth, legal_moves):
            return self.evaluationFunction(gameState)

        v = float('inf')
        for move in legal_moves:
            successor = gameState.generateSuccessor(ghostIndex, move)

            if ghostIndex == gameState.getNumAgents()-1:
                v = min(v, self.max_value(successor, a, b, depth+1))
            else:
                v = min(v, self.min_value(successor, a, b, ghostIndex+1, depth))

            if v < a:
                return v

            b = min(b, v)

        return v

    def terminal_test(self, gameState, depth, legal_moves):
        if depth == self.depth or gameState.isWin() or gameState.isLose() or not legal_moves:
            return True
        return False


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

