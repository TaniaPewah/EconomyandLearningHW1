import random
import numpy as np
if1Counter = 0
elif2Counter = 0
elif3Counter = 0
elif4Counter = 0
elif5Counter = 0
elseCounter = 0
class Player(object):
    def __init__(self, num, func):
        self.number = num
        self.choice = 'None'
        self.resultNum = -9999
        self.func = func
        self.eliminatedOnRound = -1
        self.active = True

    def show(self):
        print("player num:", self.number, "choice:", self.choice, "ourNum:", self.resultNum)

def f1(X1,X2,T):
    if (X1>90):
        choice = 'S'
    else:
        choice = 'R'
    return choice


def f2(X1,X2,T):
    if (X2>110):
        choice = 'R'
    else:
        choice = 'S'
    return choice


def f3(X1,X2,T):
    if (X2 < 70) or (X1 > 70):
        choice = 'S'
    else:
        choice = 'R'
    return choice

def f4 (X1,X2,T):
    if (X2 < 120):
        choice = 'S'
    else:
        choice = 'R'
    return choice

def f5 (X1,X2,T):
    if (T < 6) or (X2-45 < X1):
        choice = 'S'
    else:
        choice = 'R'
    return choice


def f6(X1,X2,T):
    choice ='S'
    if (T >= 5):
        if (X2 < 70) or (X1 > 70):
            choice = 'S'
        else:
            choice = 'R'
    elif (T <= 3):
        if (X2 < 80) or (X1 > 70):
            choice = 'S'
        else:
            choice = 'R'
    return choice

def f7(X1,X2,T):
    if (X2 < 75) and (X1 > 70):
        choice = 'S'
    else:
        choice = 'R'
    return choice

def f8(X1,X2,T):
    global elseCounter
    global elif2Counter
    global elif3Counter
    global elif4Counter
    global elif5Counter
    global if1Counter
    if (T == 2) and (X1 >= X2):
        choice = 'S'
    elif (T == 2) and (X1 < X2):
        choice = 'R'
    else:
        numX1win = sum(np.random.normal(X2, 45, 200) < X1)

        #if X1 won more than half of times and (T >= 10)
        #num of players is 8
        if (numX1win > 100) and (T >= 4):
            if1Counter += 1
            choice = 'S'
        elif (numX1win < 30):
            elif2Counter += 1
            choice = 'R'
        elif (numX1win > 190):
            elif3Counter += 1
            choice = 'S'
        elif (numX1win < 100) and (T < 4):
            elif4Counter += 1
            choice = 'R'
        #elif (T < (-0.03158*numX1win + 8)): # num of players is 8
        #    elif5Counter += 1
        #    choice = 'R'
        else:
            elseCounter += 1
            choice = 'S'
    return choice

T = 8
iterations = 4000
iterationCounter = 0

Players = [Player(1, f1), Player(2, f2), Player(3, f3), Player(4, f4),
           Player(5, f5), Player(6, f6), Player(7, f7), Player(8, f8)]
ActivePlayers = Players
resultsVector = [0, 0, 0, 0, 0, 0, 0, 0]
print([player.active for player in ActivePlayers])


def calcResult(choice):
    if choice == 'S':
        ourNum = X1
    else:
        ourNum = np.random.normal(X2, 45, 1)  # sample from Normal distribution
    return ourNum


def eliminatePlayer(min_result):
    new_players = list(filter(lambda player: player.resultNum == min_result, ActivePlayers))
    """
    print("min players : ")
    for player in new_players:
        print(player.resultNum)
    """

    player_to_eliminate = random.randint(0, len(new_players) - 1)
    #print("player_to_eliminate from all minimum results array : ", player_to_eliminate)
    #print("eliminating result : ", new_players[player_to_eliminate].resultNum)
    num_to_eliminate = new_players[player_to_eliminate].number
    #print("num_to_eliminate : ", num_to_eliminate)
    return num_to_eliminate


def printNewRoundData(min_result):
    print("new round----------------------------------------------------")
    print("number of active players:", len(ActivePlayers))
    print("player results:")
    for player in ActivePlayers:
        print(player.resultNum)

    print("min num : ", min_result)


def setupPlayersForNewIteration():
    for player in Players:
        player.active = True
        player.eliminatedOnRound = -1


while (iterationCounter < iterations):
    #print("iteration ", iterationCounter)
    X1 = random.randint(0, 150)
    X2 = random.randint(0, 150)

    setupPlayersForNewIteration()
    ActivePlayers = Players
    T = 9

    while (T > 0):

        #  for every player activate the descision function
        for player in ActivePlayers:
            player.choice = player.func(X1, X2, T)

        for player in ActivePlayers:
            player.resultNum = calcResult(player.choice)

        resultNums = (player.resultNum for player in ActivePlayers)

        minNum = min(resultNums)
        # printNewRoundData(minNum)

        # if there are at least 2 active players
        if len(ActivePlayers) > 1:
            num_to_eliminate = eliminatePlayer(minNum)
            for player in Players:
                if player.number == num_to_eliminate:
                    player.active = False
                    player.eliminatedOnRound = T
                    break
            ActivePlayers = list(filter(lambda player: player.number != num_to_eliminate, ActivePlayers))

        T -= 1

    for player in Players:
        #print("player num: ", player.number, " eliminated on round: ", player.eliminatedOnRound)
        if player.eliminatedOnRound == -1:
            resultsVector[player.number - 1] += 1

    iterationCounter += 1

print("printing overall results of winners")
print(resultsVector)
print(if1Counter)
print(elif2Counter)
print(elif3Counter)
print(elif4Counter)
print(elif5Counter)
print(elseCounter)










