# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
"""

    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Initial state is ",problem.getStartState())


    #print("Start's successors:",problem.getSuccessors(problem.getStartState()))
    #folosim o stiva
    frontier = util.Stack();
    expanded = []
    initial_state = problem.getStartState()
    frontier.push((initial_state,[])) #starea initiala ; nu s-au facut inca actiuni

    while(not frontier.isEmpty()):
        popped_element = frontier.pop()
        current_state,actions = popped_element

        if(current_state not in expanded): #verificam sa nu fie deja expandata starea
            expanded.append(current_state)
            if(problem.isGoalState(current_state)):#daca e goal returnam actiunile facute sa ajungem in aceasta stare
                return actions

            for successor in problem.expand(current_state): #pt fiecare stare urmatoare
                next_pos, next_action, cost = successor
                frontier.push((next_pos,actions+[next_action]))
                #adaugam in frontiera pozitia urmatoare si actiunile pana ajungem la pozitia urmatoare
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "* YOUR CODE HERE *"

    #se foloseste o coada
    #frontiera contine pozitia unde se afla acum si action-urile facute ca sa se ajunga acolo
    frontier = util.Queue();
    expanded = []
    initial_state = problem.getStartState()
    frontier.push((initial_state, []))

    while (not frontier.isEmpty()):
        popped_element = frontier.pop()
        current_state, actions = popped_element

        if (current_state not in expanded):  #daca nu a fost expandat se expandeaza
            expanded.append(current_state)
            if (problem.isGoalState(current_state)): #verificam daca nu e goal
                return actions

            for successor in problem.expand(current_state): #o lista cu toate starile viitoare posibile ; contine pozitia, actiunile si costul
                next_pos, next_action, cost = successor
                frontier.push((next_pos, actions + [next_action]))
                #se adauga in coada urmatoarea pozitie si actiunile de pana acum + actiunea pt a ajunge la urm pozitie

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "* YOUR CODE HERE *"
    frontier = util.PriorityQueue()
    expanded = []

    initial_state = problem.getStartState()
    frontier.push((initial_state,[],0 ),0)

    while(not frontier.isEmpty()):
        popped_element = frontier.pop()
        current_state,actions,total_cost = popped_element

        if current_state not in expanded:
            expanded.append(current_state)

            if(problem.isGoalState(current_state)):
                return actions
            for successors in problem.expand(current_state):
                next_pos, next_action, next_cost = successors
                new_cost = total_cost + next_cost

                # f(successor) = g(successor) + h(successor)
                # g(s) = costul total
                # h(s) = valoarea euristicii in nodul s

                f = new_cost + heuristic(next_pos,problem)
                frontier.push((next_pos,actions + [next_action], new_cost),f)




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
