# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""
#People who helped: None

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
 
    start = problem.getStartState()
    fringe = util.Stack()
    visited = []
    node = (start, [])
    goal = []
    fringe.push(node)
    
    while True:
        #1
        if fringe.isEmpty(): 
            print "Search Failure"
            break
        #2
        node = fringe.pop()
        #3
        if problem.isGoalState(node[0]):
            goal = node[1]
            break
        #4,5     
        if node[0] not in visited:
            visited.append(node[0])
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                new_plan = []
                for element in node[1]:
                    new_plan.append(element)
                new_plan.append(successor[1])

                node_ = (successor[0] , new_plan)

                fringe.push(node_)
    return goal
    
    

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    start = problem.getStartState()
    fringe = util.Queue()
    visited = []
    node = (start, [])
    goal = []
    fringe.push(node)
    
    while True:
        #1
        if fringe.isEmpty(): 
            print "Search Failure"
            break
        #2
        node = fringe.pop()
        #3
        if problem.isGoalState(node[0]):
            goal = node[1]
            break
        #4,5     
        if node[0] not in visited:
            visited.append(node[0])
            successors = problem.getSuccessors(node[0])
            for successor in reversed(successors):
                new_plan = []
                for element in node[1]:
                    new_plan.append(element)
                new_plan.append(successor[1])

                node_ = (successor[0] , new_plan)

                fringe.push(node_)

    return goal

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    start = problem.getStartState()
    fringe = util.PriorityQueue()
    visited = []
    node = (start, [], 0)
    goal = []
    fringe.push(node, 0)
    
    while True:
        #1
        if fringe.isEmpty(): 
            print "Search Failure"
            break
        #2
        node = fringe.pop()
        #3
        if problem.isGoalState(node[0]):
            goal = node[1]
            break
        #4,5     
        if node[0] not in visited:
            visited.append(node[0])
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                #print "successor cost:", successor[2]
                new_plan = []
                for element in node[1]:
                    new_plan.append(element)
                new_plan.append(successor[1])
                cost = node[2]+successor[2]
                node_ = (successor[0] , new_plan, cost)

                fringe.push(node_, cost)
    return goal
    
    


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    start = problem.getStartState()
    fringe = util.PriorityQueue()
    visited = []
    node = (start, [], 0)
    goal = []
    fringe.push(node, 0)
    while True:
        #1
        if fringe.isEmpty(): 
            print "Search Failure"
            break
        #2
        node = fringe.pop()
        #3
        if problem.isGoalState(node[0]):
            goal = node[1]
            break
        #4,5     
        if node[0] not in visited:
            visited.append(node[0])
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                #print "successor cost:", successor[2]
                new_plan = []
                for element in node[1]:
                    new_plan.append(element)
                new_plan.append(successor[1])
                cost = node[2]+successor[2]                
                node_ = (successor[0] , new_plan, cost)
                total_cost = cost+heuristic(successor[0], problem)
                fringe.push(node_, total_cost)
    return goal

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
