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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
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

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action) #STAREA URMATOARE
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #return childGameState.getScore()
        score = childGameState.getScore() - currentGameState.getScore()  #vaoarea scorului este diferenta scorului pentru starea childGame si starea curenta

        ghostManhattanDist = []  #Distanta manhattan de la urmatoarea stare pana toate fantomele
        for ghost in newGhostStates:
            ghostManhattanDist.append(util.manhattanDistance(newPos, ghost.getPosition()))

        foodManhattanDist = []  #Distanta manhattan de la urmatoarea stare pana toate bucatile de mancare
        for foodPosition in newFood.asList():
            foodManhattanDist.append(util.manhattanDistance(newPos, foodPosition))

        if (newPos == currentGameState.getPacmanPosition()):  # Nu vreau ca pacman sa stea pe loc
            score = score - 100

        #cu cat pacman este mai departe de o fantoma, cu atat ar trebui sa ii creasca scorul, asa ca adaugam distanta respectiva la scor
        for distance in ghostManhattanDist:
            score = score + distance

        if len(foodManhattanDist) > 0: #verific daca mai exista bucati de mancare in joc
            score = score - min(foodManhattanDist)  #Cu cat pacman este mai departe de o bucata de mancare, cu atat i se scade scorul ; scadem distanta pana la cea mai apropiata buata de mancare
        else: #daca nu mai sunt le-a mancat pacan pe toate si ii cresc scorul
            score = score + 1000

        return score

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

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        action, score = self.minimax(0, 0, gameState)  # Primeste actiunile si scorul pt pacman
        return action  #Returneaza actiunea ce trebuie facuta

    def minimax(self, curr_depth, agent_index, gameState):
        #Pentru pacman, cel mai bun scor e cel maxim, iar pentru fantome cel minim

        #Daca toti agentii si-au terminat miscarea dintr-o tura
        if agent_index >= gameState.getNumAgents():
            agent_index = 0 #revin la primul agent si maresc adancimea
            curr_depth += 1

        # Returneaza rezultatul cand se atinge adancimea maxima
        if curr_depth == self.depth:
            return None, self.evaluationFunction(gameState)

        #O sa pastsrez best_action si best_score
        best_score, best_action = None, None

        if agent_index == 0:  #Pentru randul lui pacman
            for action in gameState.getLegalActions(agent_index):  #Parcurgem fiecare actiune legala a lui pacman
                # Calculam scorul urmatorilor agenti, adica al tuturor fantomelor
                next_game_state = gameState.getNextState(agent_index, action)
                _, score = self.minimax(curr_depth, agent_index + 1, next_game_state)
                #Daca score e mai mare decat best_score curent, il actualizam
                if best_score is None or score > best_score:
                    best_score = score
                    best_action = action
        else:  #Pentru randul fantomelor
            for action in gameState.getLegalActions(agent_index):  # Parcurgem fiecare actiune legala a fantomelor
                # Calculam scorul urmatorului agent
                next_game_state = gameState.getNextState(agent_index, action)
                _, score = self.minimax(curr_depth, agent_index + 1, next_game_state)
                #alegem scorul minim
                if best_score is None or score < best_score:
                    best_score = score
                    best_action = action

        # Daca nu mai avem stari urmatoare posibile, returnam valoare de la evaluationFunction
        if best_score is None:
            return None, self.evaluationFunction(gameState)

        return best_action, best_score  # Returnam best_action si best_score



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        inf = float('inf')
        action, score = self.alpha_beta(0, 0, gameState, -inf, inf)  #pe alfa si beta le am luat -inf si inf
        return action  # Returnam doar actiunea gasita in urma algoritmului

    def alpha_beta(self, curr_depth, agent_index, gameState, alpha, beta):
        #daca alpha > beta putem sa ne oprim din generat stari urmatoare posibile si sa "taiem" arborele

        # Daca toti agentii si-au terminat miscarea dintr-o tura
        if agent_index >= gameState.getNumAgents(): #revin la primul agent si maresc adancimea
            agent_index = 0
            curr_depth += 1

        # Returneaza rezultatul cand se atinge adancimea maxima
        if curr_depth == self.depth:
            return None, self.evaluationFunction(gameState)

        #O sa pastsrez best_action si best_score
        best_score, best_action = None, None

        if agent_index == 0:  #daca e randul lui pacman
            for action in gameState.getLegalActions(agent_index):
                # Parcurgem fiecare actiune legala a lui pacman
                # Calculam scorul urmatorilor agenti, adica al tuturor fantomelor
                next_game_state = gameState.getNextState(agent_index, action)
                _, score = self.alpha_beta(curr_depth, agent_index + 1, next_game_state, alpha, beta)


                #Daca score e mai mare ca best_score, il actalizam
                if best_score is None or score > best_score:
                    best_score = score
                    best_action = action

                # Actualizam valoarea pt alpha
                alpha = max(alpha, score)

                # Daca alpha ajungem mai mare ca beta\, nu mai continuam si "taiem" arborele
                if alpha > beta:
                    break
        else:  #Daca e randul fantomelor
            for action in gameState.getLegalActions(agent_index):  # Parcurgem fiecare actiune legala a fantomelor
                # Calculam scorul urmatorului agent
                next_game_state = gameState.getNextState(agent_index, action)
                _, score = self.alpha_beta(curr_depth, agent_index + 1, next_game_state, alpha, beta)

                #Daca score e mai mic ca best_score, il actualizam pe best_score
                if best_score is None or score < best_score:
                    best_score = score
                    best_action = action

                # Actualizam valoarea entru beta
                beta = min(beta, score)

                # Daca alpha ajungem mai mare ca beta, nu mai continuam si "taiem" arborele
                if beta < alpha:
                    break

        # Daca nu mai avem stari urmatoare posibile, returnam valoare de la evaluationFunction
        if best_score is None:
            return None, self.evaluationFunction(gameState)
        return best_action, best_score  # Returnam best_action si best_score


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
