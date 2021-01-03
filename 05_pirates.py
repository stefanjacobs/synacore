rooms = [[None for x in range(4)] for y in range(4)]

# initialize rooms according to layout from challenge
rooms[0][0] = "*"
rooms[0][1] = "4"
rooms[0][2] = "+"
rooms[0][3] = "22"
rooms[1][0] = "8"
rooms[1][1] = "*"
rooms[1][2] = "4"
rooms[1][3] = "-"
rooms[2][0] = "-"
rooms[2][1] = "11"
rooms[2][2] = "-"
rooms[2][3] = "9"
rooms[3][0] = "1"
rooms[3][1] = "*"
rooms[3][2] = "18"
rooms[3][3] = "*"

# initialize start state
startState = dict()
startState["x"] = 0
startState["y"] = 3
startState["v"] = -1
startState["math"] = rooms[0][3]
startState["actions"] = []

# initialize goal state
goalState = dict()
goalState["x"] = 3
goalState["y"] = 0
goalState["v"] = 30

# initialize actions
actions = dict()
actions["north"] = [0, -1]
actions["south"] = [0, 1]
actions["west"] = [-1, 0]
actions["east"] = [1, 0]

# Algorithm:
# 1. Put start state in queue
# 2. While True:
# 3.   State = Pop()
# 4.   Is State the goal State? --> Break
# 5.   Apply all Actions to the state and enqueue them
import copy

q = []
q.append(startState)
while True:
    state = q.pop(0)

    # evaluate math expression to value for state
    try:
        state["v"] = eval(state["math"])
        state["math"] = str(state["v"])
    except SyntaxError:
        state["v"] = -1
    if state["v"] == goalState["v"] \
        and state["x"] == goalState["x"] \
        and state["y"] == goalState["y"]:
        # found solution
        break

    if state["x"] == 3 and state["y"] == 0:
        # when we are in the final room, do not exit it again, as the orb will evaporate
        continue

    # solution not yet found, apply all actions:
    for k, v in actions.items():
        x = state["x"] + v[0]
        y = state["y"] + v[1]
        if x in (0, 1, 2, 3) and y in (0, 1, 2, 3) and ((x, y) != (0, 3)):
            newState = dict()
            newState["x"] = x
            newState["y"] = y
            newState["math"] = state["math"] + rooms[x][y]
            newState["actions"] = copy.deepcopy(state["actions"])
            newState["actions"].append(k)
            q.append(newState)


print("searching done, we have a solution!")
print(state)