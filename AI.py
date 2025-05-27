from random import *
from time import *
import ast
#tracer(0,0)
training_time =100# amount of games we play. 
c = 0 # finds the average amount of games Ai wins or ties. 
turn = 1 # alternates player or opponent turns
turnamount = 0 # finds amount ofturns played in a game.
tile_array = [0,0,0,0,0,0,0,0,0] # stores game position 
game_moves = [] # stores all positions and moves played in game. used for the learning process
probabilty_table = {}# stores every position encountered.
OpponentWon = 0
depthValue = 2
severity = 99999999999999999999
debug_val = None
tie = 0
with open('AI_memory.txt','r') as g: # takes the text file and puts in the table.
    probabilty_table = ast.literal_eval(g.read())
def turns_finder(input):# creates a new position if we have not encountered it before.
    return_array = []
    moves = []
    for x in range(0,len(input)):
        if input[x] ==0:
            moves.append(x)
    for y in range(0,len(moves)):
        return_array.append([moves[y],1])
    return return_array
def RandomAI(position):
    random_array = []
    for x in range(9):
        if position[x] == 0:
            random_array.append(x)
    position[random_array[randint(0,len(random_array)-1)]] = 1
    return position
def BlockerAI(position): # our opponent AI. if It can a block a win, it will, or if it can win, it will. 
    global OpponentWon 
    block = -1
    random_array = []
    for x in range(9):
        position2 = position
        if position2[x] == 0:
            position2[x] = 1
            checkWin(position2,True)
            if OpponentWon == 1:
                OpponentWon = 0
                return position2
            else:
                position2[x] = 2
                checkWin(position,True)
                if OpponentWon == 2:
                    OpponentWon = 0
                    block = x 
                    position2[x] = 0
                position2[x] = 0 
    if block > -1:
        position2 = position
        position2[block] = 2
        return position2
    else: 
        position2 = position
        for x in range(9):
            if position2[x] == 0:
                random_array.append(x)
        position2[random_array[randint(0,len(random_array)-1)]] = 1
        return position2
def minimax(position,depth, depthTurn,alpha,beta):
    global OpponentWon
    position2 = position
    checkWin(position2,True)
    if OpponentWon == 1:
        OpponentWon = 0
        #print(position2)
        #print(10)
        #print("win")
        return 10
    if OpponentWon == 2:
        OpponentWon = 0
        #print(position2)
        #print(-10)
        #print("lose")
        return -10
    if OpponentWon == 3:
        OpponentWon = 0
        #print(position2)
        #print(0)
        #print("tie")
        return 0
    if depth == 0:
        #print(position2)
        #print(0)
        #print("depth")
        return 0
    if depthTurn == 1:
        depthTurn = 2
        best = -1000
        for x in range(9):
            if position2[x] == 0:
                position2[x] = 1
                best = max(best, minimax(position2,depth-1,depthTurn,alpha,beta))
                position2[x] = 0
                alpha = max(alpha,best)
                if beta <= alpha:
                    break
    else:
        depthTurn = 1
        best = 1000
        for y in range(9):
            if position2[y] == 0:
                position2[y] = 2
                best = min(best, minimax(position2,depth-1,depthTurn,alpha,beta))
                position2[y] = 0
                beta = min(beta,best)
                if beta <= alpha:
                    break
    #print(position2)
    #print(best)
    #print("search")
    return best
def BlockerAI2(position):
    global depthValue
    position2 = position
    bestval = -1000
    savedMove = []
    for x in range(9):
        if position2[x] == 0:
            position2[x] = 1
            moveVal = minimax(position2,depthValue,2,-1000,1000)
            if moveVal > bestval:
                savedMove = []
                savedMove.append(x)
                bestval = moveVal
            if moveVal == bestval:
                savedMove.append(x)
                bestval = moveVal
            position2[x] = 0
    position2[savedMove[randint(0,len(savedMove)-1)]] = 1
    #print("Search Complete")
    return position2
def tile(tileX,tileY,size=30): # draws tile in graphic screen
    #penup()
    #goto(tileX,tileY)
    #pendown()
    for i in range(4):
        pass
        #forward(size)
        #left(90)
    #end_fill()
    #penup()
    #update()
    pass
for x in range(3): # create 9 tiles
    for y in range(3):
        #tile(30*(x),30*(y))
        pass
def nextTurn(): # alternates turns.
    global turn
    if turn == 1:
        turn = 2
    else:
        turn = 1
def reset(): # reset vairables related to the game after the game has ended.
    global tile_array,turn,turnamount,OpponentWon
    #clear()
    for x in range(3):
        for y in range(3):
            pass #tile(30*(x),30*(y))
    tile_array = [0,0,0,0,0,0,0,0,0]
    turn = 1
    turnamount = 0
    OpponentWon = 0
    #update()
d = 0
def checkWin(tile_array = tile_array,future = False): # check if we win, lose or draw. future is used by oppent for seeing to the future.
    global c, OpponentWon, tie, d
    if tile_array[0] ==  tile_array[1] ==  tile_array[2] == 1:
       # goto(-30,0)
        #print("Player " + str(1) + " wins")
        if future == True:
            OpponentWon = 1 
        else:
            learn(2)
            c+=1
            reset()
            return True
    if tile_array[0] ==  tile_array[1] ==  tile_array[2] == 2:
        #goto(-30,-30)
        #print("Player " + str(2) + " wins")
        if future == True:
            OpponentWon = 2
        else:
            learn(1)
            reset()
            return True
    if tile_array[3] ==  tile_array[4] ==  tile_array[5] == 1:
              # goto(-30,0)
        #print("Player " + str(1) + " wins")
        if future == True:
            OpponentWon = 1 
        else:
            learn(2)
            c+=1
            reset()
            return True
    if tile_array[3] ==  tile_array[4] ==  tile_array[5] == 2:
        #goto(-30,-30)
        #print("Player " + str(2) + " wins")
        if future == True:
            OpponentWon = 2
        else:
            learn(1)
            reset()
            return True
    if tile_array[6] ==  tile_array[7] ==  tile_array[8] == 1:
              # goto(-30,0)
        #print("Player " + str(1) + " wins")
        if future == True:
            OpponentWon = 1 
        else:
            learn(2)
            c+=1
            reset()
            return True
    if tile_array[6] ==  tile_array[7] ==  tile_array[8] == 2:
        #goto(-30,-30)
        #print("Player " + str(2) + " wins")
        if future == True:
            OpponentWon = 2
        else:
            learn(1)
            reset()
            return True
    if tile_array[0] ==  tile_array[4] ==  tile_array[8] == 1:
              # goto(-30,0)
        #print("Player " + str(1) + " wins")
        if future == True:
            OpponentWon = 1 
        else:
            learn(2)
            c+=1
            reset()
            return True
    if tile_array[0] ==  tile_array[4] ==  tile_array[8] == 2:
        #goto(-30,-30)
        #print("Player " + str(2) + " wins")
        if future == True:
            OpponentWon = 2
        else:
            learn(1)
            reset()
            return True
    if tile_array[6] ==  tile_array[4] ==  tile_array[2] == 1:
              # goto(-30,0)
        #print("Player " + str(1) + " wins")
        if future == True:
            OpponentWon = 1 
        else:
            learn(2)
            c+=1
            reset()
            return True
    if tile_array[6] ==  tile_array[4] ==  tile_array[2] == 2:
        #goto(-30,-30)
        #print("Player " + str(2) + " wins")
        if future == True:
            OpponentWon = 2
        else:
            learn(1)
            reset()
            return True
    if tile_array[0] ==  tile_array[3] ==  tile_array[6] == 1:
              # goto(-30,0)
        #print("Player " + str(1) + " wins")
        if future == True:
            OpponentWon = 1 
        else:
            learn(2)
            c+=1
            reset()
            return True
    if tile_array[0] ==  tile_array[3] ==  tile_array[6] == 2:
        #goto(-30,-30)
        #print("Player " + str(2) + " wins")
        if future == True:
            OpponentWon = 2
        else:
            learn(1)
            reset()
            return True
    if tile_array[1] ==  tile_array[4] ==  tile_array[7] == 1:
              # goto(-30,0)
        #print("Player " + str(1) + " wins")
        if future == True:
            OpponentWon = 1 
        else:
            learn(2)
            c+=1
            reset()
            return True
    if tile_array[1] ==  tile_array[4] ==  tile_array[7] == 2:
        #goto(-30,-30)
        #print("Player " + str(2) + " wins")
        if future == True:
            OpponentWon = 2
        else:
            learn(1)
            reset()
            return True
    if tile_array[2] ==  tile_array[5] ==  tile_array[8] == 1:
              # goto(-30,0)
        #print("Player " + str(1) + " wins")
        if future == True:
            OpponentWon = 1 
        else:
            learn(2)
            c+=1
            reset()
            return True
    if tile_array[2] ==  tile_array[5] ==  tile_array[8] == 2:
        #goto(-30,-30)
        #print("Player " + str(2) + " wins")
        if future == True:
            OpponentWon = 2
        else:
            learn(1)
            reset()
            return True
    if turnamount == 9:
        if  not future:
            #goto(-30,-30)
            reset()
            learn(0)
            tie = 1
            d+=1
            return True
        else:
            OpponentWon = 3
def click(x,y): # for graphic screen, not neccasary now.
    global tile_array,turnamount
    for mouse in range(9):
        Y = int(mouse/3)
        X = (mouse%3)
        if x > 30*X and x< 30*(X+1) and y > 30*Y and y< 30*(Y+1):
            if tile_array[mouse] != 0:
                break
            turnamount+=1
            tile_array[mouse] = turn
            nextTurn()
            update1()
            if checkWin() == True:
                return
            tile_array = AI(tile_array)
            turnamount+=1
            nextTurn()
            update1()
            checkWin()
def update1(): # update the screen
    for check in range(len(tile_array)):
        Y = int(check/3)
        X = int(check%3)
        if tile_array[check] == 1:
            ##penup()
            #goto(15+ X*30,Y*30)
            #write("X")
            pass
        if tile_array[check] == 2:
            ##penup()
            #goto(15+ X*30,Y*30)
            #write("O")
            pass
def AI(input): # our AI. checks if we encounter a position. creates a random variable and see which move it falls into, then plays that moves
    global probabilty_table,game_moves, debug_val, turnamount
    input2 = input
    maximum = 0
    game_moves.append([turnamount])
    key = ""
    probabilty_choices = [0]
    for x in range(9):
        key = str(key + str(input[x]))
    game_moves[len(game_moves)-1].append(key)
    if key in probabilty_table.keys():
        pass
    else:
        probabilty_table[key] = turns_finder(input) # not cause
    for y in range(len(probabilty_table[key])):
        probabilty_choices.append(probabilty_choices[y]+probabilty_table[key][y][1])
    maximum = probabilty_choices[len(probabilty_choices)-1] # 90% of time set to 0
    if turnamount == 1:
        debug_val = [probabilty_table[key],maximum]
    choice = uniform(0,maximum)
    for u in range(len(probabilty_choices)-1):
        if choice > probabilty_choices[u] and choice <= probabilty_choices[u+1]: 
            game_moves[len(game_moves)-1].append(u)
            input2[probabilty_table[key][u][0]] = 2
            return input2
def learn(state):
    global game_moves,probabilty_table,severity, debug_val
    if state == 0:
        return
    for x in range(len(game_moves)):
        if state == 1:
            try:
                probabilty_table[game_moves[x][1]][game_moves[x][2]][1]+= 10**(-1*((9-x)/severity)) # affects bug. 
            except IndexError:
                print(tile_array)
                print(game_moves)
                print(debug_val)
                exit()
        else:
            try:
                probabilty_table[game_moves[x][1]][game_moves[x][2]][1]-= 10**(-1*((9-x)/severity))
            except IndexError:
                print(tile_array)
                print(game_moves)
                print(debug_val)
                exit()
        if probabilty_table[game_moves[x][1]][game_moves[x][2]][1] <= 0:
            probabilty_table[game_moves[x][1]][game_moves[x][2]][1] = 0.0001
    game_moves = []
    debug_val = None
a = 0
starttime = time()
while a < training_time:
    while True:
        tile_array = BlockerAI2(tile_array)
        turnamount+=1
        #print(tile_array)
        if checkWin(tile_array) == True:
            break
        nextTurn()
        tile_array = AI(tile_array)
        turnamount+=1
        #print(tile_array)
        if checkWin(tile_array) == True:
            break
        nextTurn()
    tie = 0
    a+=1
    if a%100 == 0:
        print(a)
endtime = time()
print(endtime-starttime)
print(1-(c/training_time))
print((d/training_time))
print("done")
with open('AI_memory.txt','w') as f:
    f.write(str(probabilty_table))
#listen()
#onscreenclick(click)
#update1()