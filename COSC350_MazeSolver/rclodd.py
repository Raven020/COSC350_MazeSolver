import random
import time

moves = {"up": (-1, 0), "down": (1, 0),
         "right": (0, 1), "left": (0, -1)}
avaliableMoves = ["up","down","left","right"]
mazeHeight = 7
mazeWidth = 18
start = [1,1]
goal  = [5,16]

# maze that will be solved, S = Start, G = Goal, 1 = Wall, 0 = Open Space
maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, "S", 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, "G", 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
# rewards map, TDL required some "encouragement" so deadends have been decreased to increase likelihood of 
# agent finding the correct path
rewards_map = [[-0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9],
            [-0.9, -0.5, -0.1, -0.1, -0.9, -0.1, -0.1, -0.1, -0.1, -0.9, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.5, -0.9],
            [-0.9, -0.1, -0.9, -0.9, -0.1, -0.1, -0.9, -0.9, -0.1, -0.1, -0.1, -0.9, -0.1, -0.9, -0.1, -0.9, -0.9, -0.9],
            [-0.9, -0.1, -0.9, -0.1, -0.1, -0.9, -0.1, -0.5, -0.9, -0.1, -0.9, -0.9, -0.1, -0.9, -0.1, -0.9, -0.1, -0.9],
            [-0.9, -0.1, -0.9, -0.9, -0.1, -0.5, -0.9, -0.1, -0.9, -0.1, -0.9, -0.9, -0.1, -0.9, -0.1, -0.9, -0.1, -0.9],
            [-0.9, -0.1, -0.1, -0.1, -0.1, -0.9, -0.5, -0.1, -0.1, -0.1, -0.9, -0.5, -0.5, -0.9, -0.1, -0.1, -0.01, -0.9],
            [-0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9]
            ]
# Function to check if a move is valid or not
# A move is not valid if it is onto a wall or out of bounds
def validMove(state,action):
    global moves
    x = state[0] + moves[action][0]
    y = state[1] + moves[action][1]
    
    if x < 0 or x > mazeHeight or y < 0 or y > mazeWidth or maze[x][y] == 1:
        return False
    return True

# Function to generate a random move, left, right, down or up
def getAction(state):
    move = -1
    
    while True:
        move = random.randint(0,3)
        if validMove(state, avaliableMoves[move]):
            break
    return avaliableMoves[move]

# A function that returns the result of an action and the reward associated with it
def takeAction(state, action):
    global rewards_map
    x = state[0] + moves[action][0]
    y = state[1] + moves[action][1]

    return rewards_map[x][y], [x,y]

# TDL function to generate the values for each valid move
def tdl(state, goal):
    episodes = 10
    gamma = 0.1
    alpha = 0.5
    #Empty value map
    values = [[0] * mazeWidth for _ in range(mazeHeight)]

    start = list(state)
    for i in range(episodes):
        state = list(start)
        
        while True:
            action = getAction(state)
            reward, new_state = takeAction(state,action)
            # if taking random moves has found the goal, break while loop, start another episode
            if new_state == goal:
                break

            current = values[state[0]][state[1]]
            after = values[new_state[0]][new_state[1]]
            # TDL formula
            # V(S) = V(S) + aplha * (reward' + gamma * V(S') - V(S))
            values[state[0]][state[1]] += alpha * (reward + gamma * after - current)

            state = list(new_state)
    # return the value map       
    return values

# Function to find path to goal through value map
def getPath(state,goal,values):
    path = []
    travelled = []
    travelled.append(state)
    max_attempts = 50
    max_state = start
    
    # path finding function choose the greatest next move it can
    for j in range(max_attempts):
        max_val = -10.0
        max_state = [1,1]
        max_move = 0
        for i in range(4):
                if validMove(state, avaliableMoves[i]):
                    rewards, new_state = takeAction(state,avaliableMoves[i])
                    if (values[new_state[0]][new_state[1]] > max_val) and (new_state not in travelled):
                        max_val = values[new_state[0]][new_state[1]]
                        max_state = list(new_state)
                        max_move = i

        path.append(max_move)
        travelled.append(max_state)    

        state = list(max_state)
        if state == goal:
            return travelled

   # print("Max pathing attempts reach - exiting")
    return travelled

# Function for drawing where the agent has travelled
def drawAgent(travelled):
    for item in travelled:
        maze[item[0]][item[1]] = "E"
    printMaze()

# Function for printing the solved maze
def printMaze():
    mazeWithPlayer = maze
    print("<------ Start Maze ------>")
    for i in range(mazeHeight):
        for j in range(mazeWidth):
            print(maze[i][j], " ", end="")
        print("")
    print("<------ End Maze ------>")

# Driver code
def main():

    print("Author: Raven Clodd")
    print("Method Used: TDL")
    print("Description: generate negative values for each valid move in maze. As values get closer to the goal, values should get increasingly greater.") 
    print("path finding algorithm will then find a path choosing the next greatest valid move, ideally leading to the goal.")
    time.sleep(1)

    print("\nBegining search!")
    path = []
    attempts = 1
    while goal not in path:
        if attempts > 1:
            print("---- Attempt to find path to goal Failed, trying again ----")
        print("---- Taking Attempt no. ", attempts,"----")
        print("Assigning Values")
        values = tdl(start,goal)
        print("Finding Path")
        path = getPath(start, goal, values)
        if goal not in path:
            attempts += 1

    print("---- Goal Found!! ----")
    print("Attempts taken = ", attempts)
    print("E = Path to goal")
    print("No. of Moves = ", len(path))
    drawAgent(path)
    print("Path = ", path)



if __name__ == "__main__":
    main()
    


