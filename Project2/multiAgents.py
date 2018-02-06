# multiAgents.py
# --------------
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
        newGhostPositions = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newFoodCount = newFood.count()

        dist_ghost = 9999
        
        for ghost in newGhostPositions:
            this_ghost = manhattanDistance(newPos,ghost)
            if this_ghost < dist_ghost:
                dist_ghost = this_ghost
            
            
        min_food_dist = newFoodCount*9999
        Foods = newFood.asList()
        min_food = (0,0)
        for food in Foods:
            this_dist = manhattanDistance(food, newPos)
            if min_food_dist > this_dist:
                min_food_dist = this_dist  
                min_food = food
            
        "*** YOUR CODE HERE ***"
        return 100-10*newFoodCount-(25/(dist_ghost+1))+ successorGameState.getScore()-min_food_dist

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    """
    def Min(self, gameState, ghostIndex):
        evaluation = 999999
        if ghostIndex == gameState.getNumAgents():
            return 
       """ 
    def Value(self, gameState):

        if gameState.isLose():
            evaluation = (self.evaluationFunction(gameState),0)
            return evaluation
            
        if gameState.isWin():   
            evaluation = (self.evaluationFunction(gameState),0)
            return evaluation
       
        if self.index == gameState.getNumAgents():
            if self.depth==1: 
                return (self.evaluationFunction(gameState),0)
            else: 
                self.depth-=1
                self.index=0
            
        if self.index == 0:
            return self.MAX(gameState)
        else:
            return self.MIN(gameState)
        
    def MAX(self, gameState):
        evaluation = -999999
        bestAction = gameState.getLegalActions(self.index)[0]
        
        for action in gameState.getLegalActions(self.index):
            successorGameState = gameState.generateSuccessor(self.index, action)
            prev_index = self.index
            prev_depth = self.depth
            self.index+=1
            this_eval = self.Value(successorGameState)[0]
            if this_eval > evaluation: 
                evaluation = this_eval
                bestAction = action
            self.index=prev_index
            self.depth=prev_depth
        return (evaluation, bestAction)
    
    def MIN(self, gameState):
        evaluation = 999999
        bestAction = gameState.getLegalActions(self.index)[0]
        for action in gameState.getLegalActions(self.index):
            successorGameState = gameState.generateSuccessor(self.index, action)
            prev_index = self.index
            prev_depth = self.depth
            self.index+=1
            this_eval = self.Value(successorGameState)[0]
            if this_eval < evaluation: 
                evaluation = this_eval
                bestAction = action
            self.index=prev_index
            self.depth=prev_depth
        return (evaluation, bestAction)
                
       
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
        
        return self.Value(gameState)[1]    

class AlphaBetaAgent(MultiAgentSearchAgent):
    def Value(self, gameState, alpha, beta):
        if gameState.isLose():
            evaluation = (self.evaluationFunction(gameState),0)
            return evaluation
            
        if gameState.isWin():   
            evaluation = (self.evaluationFunction(gameState),0)
            return evaluation
       
        if self.index == gameState.getNumAgents():
            if self.depth==1: 
                return (self.evaluationFunction(gameState),0)
            else: 
                self.depth-=1
                self.index=0
            
        if self.index == 0:
            return self.MAX(gameState, alpha, beta)
        else:
            return self.MIN(gameState, alpha, beta)
        
    def MAX(self, gameState, alpha, beta):
        evaluation = -999999
        bestAction = gameState.getLegalActions(self.index)[0]
        
        for action in gameState.getLegalActions(self.index):
            successorGameState = gameState.generateSuccessor(self.index, action)
            prev_index = self.index
            prev_depth = self.depth
            self.index+=1
            this_eval = self.Value(successorGameState, alpha, beta)[0]
            if this_eval > evaluation: 
                evaluation = this_eval
                bestAction = action
            self.index=prev_index
            self.depth=prev_depth
            if this_eval>alpha: alpha = this_eval
            if alpha>beta:break
        return (evaluation, bestAction)
    
    def MIN(self, gameState, alpha, beta):
        evaluation = 999999
        bestAction = gameState.getLegalActions(self.index)[0]
        for action in gameState.getLegalActions(self.index):
            successorGameState = gameState.generateSuccessor(self.index, action)
            prev_index = self.index
            prev_depth = self.depth
            self.index+=1
            this_eval = self.Value(successorGameState, alpha, beta)[0]
            if this_eval < evaluation: 
                evaluation = this_eval
                bestAction = action
            self.index=prev_index
            self.depth=prev_depth
            if this_eval<beta: beta = this_eval
            if alpha>beta:break            
        return (evaluation, bestAction)
                
       
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
        return self.Value(gameState, -999990, 999999)[1]    
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    """
    def Min(self, gameState, ghostIndex):
        evaluation = 999999
        if ghostIndex == gameState.getNumAgents():
            return 
       """ 
    def Value(self, gameState):
        if gameState.isLose():
            evaluation = (self.evaluationFunction(gameState),0)
            return evaluation

        if gameState.isWin():   
            evaluation = (self.evaluationFunction(gameState),0)
            return evaluation

        if self.index == gameState.getNumAgents():
            if self.depth==1: 
                return (self.evaluationFunction(gameState),0)
            else: 
                self.depth-=1
                self.index=0

        if self.index == 0:
            return self.MAX(gameState)
        else:
            return self.EXP(gameState)

    def MAX(self, gameState):
        evaluation = -999999
        bestAction = gameState.getLegalActions(self.index)[0]

        for action in gameState.getLegalActions(self.index):
            successorGameState = gameState.generateSuccessor(self.index, action)
            prev_index = self.index
            prev_depth = self.depth
            self.index+=1
            this_eval = self.Value(successorGameState)[0]
            if this_eval > evaluation: 
                evaluation = this_eval
                bestAction = action
            self.index=prev_index
            self.depth=prev_depth
        return (evaluation, bestAction)

    def EXP(self, gameState):
        evaluation = 0
        bestAction = gameState.getLegalActions(self.index)[0]
        num_actions = len(gameState.getLegalActions(self.index))
        
        for action in gameState.getLegalActions(self.index):
            successorGameState = gameState.generateSuccessor(self.index, action)
            prev_index = self.index
            prev_depth = self.depth
            self.index+=1
            this_eval = self.Value(successorGameState)[0]
            evaluation+=this_eval
            self.index=prev_index
            self.depth=prev_depth
        
        evaluation/=float(num_actions)
        return (evaluation, bestAction)


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

        return self.Value(gameState)[1]    

def betterEvaluationFunction(currentGameState):
    """
    Design a better evaluation function here.

    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newGhostPositions = successorGameState.getGhostPositions()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newFoodCount = newFood.count()
    newCapsules = successorGameState.getCapsules()
    dist_ghost = 9999
    
    for ghost in newGhostPositions:
        this_ghost = manhattanDistance(newPos,ghost)
        if this_ghost < dist_ghost:
            dist_ghost = this_ghost
        
        
    min_food_dist = newFoodCount*9999
    Foods = newFood.asList()
    min_food = (0,0)
    for food in Foods:
        this_dist = manhattanDistance(food, newPos)
        if min_food_dist > this_dist:
            min_food_dist = this_dist  
            min_food = food
    
    min_capsule_dist = 9999*len(newCapsules)
    min_capsule = (0,0)
    for capsule in newCapsules:
        this_dist = manhattanDistance(capsule, newPos)
        if min_capsule_dist > this_dist:
            min_capsule_dist = this_dist  
            min_capsule = capsule
        
    "*** YOUR CODE HERE ***"
    return 100-800*newFoodCount-(50/(dist_ghost+1))+ 10*successorGameState.getScore()+400/(min_food_dist+1)-50*min_capsule_dist
    """
    What it does:
    Pacman will be attracted to the closest food according to newFoodCount and min_food_dist; on the other hand, it will be 
    inluenced by the distance of the closest ghost. (the program uses the reciprocal of the ghost distance so 
    that it won't affect pacman when the ghost is far a way) The program also make pacman search for power capsule
    in an early stage so that it is more likely to eat some ghosts for a higher score.
    """
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

