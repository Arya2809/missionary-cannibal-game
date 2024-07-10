import queue

def print_state(state):
    left_bank = "M " * state[0] + "C " * state[1]
    boat = "-->" if state[2] == 1 else "<--"
    right_bank = "M " * (total_missionaries - state[0]) + "C " * (total_cannibals - state[1])
    print(f"{left_bank} | {boat} | {right_bank}")

def print_instructions():
    print("\nGeneral Instructions:")
    print("There are some number of Missionaries and Cannibals (you need to enter the numbers) on the left side of the river")
    print("The task is to move all the Missionaries and all the Cannibals to the right side of the river")
    print("'Left side -> Right side' this means the boat is Travelling from left side of the river to the Right side of the river")
    print("'Left side <- Right side' this means the boat is Travelling from Right side of the river to the Left side of the river")
    print("'M' denotes Missionary and 'C' denotes Cannibal")
    print("\nRules:")
    print("1. The boat can carry at most two people at a time")
    print("2. If the number of Cannibals is greater than the number of Missionaries then the Cannibals would eat the Missionaries")
    print("3. The boat cannot cross the river by itself with no people on board\n")
    print("Game Start\n")

def get_user_input(state):
    direction = "Left side -> Right side" if state[2] == 1 else "Left side <- Right side"
    print(f"\n{direction} river travel")
    num_missionaries = int(input("Enter number of Missionaries travel => "))
    num_cannibals = int(input("Enter number of Cannibals travel => "))
    print()
    return (num_missionaries, num_cannibals)

def is_valid_move(move, state):
    if move[0] + move[1] <= 2 and 0 < move[0] + move[1] <= 2:  # Check if total number of passengers is 1 or 2
        if state[2] == 1:  # Boat is on the left side
            if state[0] >= move[0] and state[1] >= move[1]:
                return True
        else:  # Boat is on the right side
            if total_missionaries - state[0] >= move[0] and total_cannibals - state[1] >= move[1]:
                return True
    return False

def is_goal_state(state):
    return state == (0, 0, 0)

def is_valid_state(state):
    if state[0] < 0 or state[1] < 0 or state[0] > total_missionaries or state[1] > total_cannibals:
        return False
    if state[0] < state[1] and state[0] > 0:
        return False
    if total_missionaries - state[0] < total_cannibals - state[1] and total_missionaries - state[0] > 0:
        return False
    return True

def successors(state):
    m, c, b = state
    moves = []
    if b == 1:  # Boat is on the left side
        for i in range(total_missionaries + 1):
            for j in range(total_cannibals + 1):
                if i + j > 0 and is_valid_move((i, j), state) and i >= j:  # Ensure no more cannibals than missionaries on the boat
                    moves.append((i, j, 1))
    else:  # Boat is on the right side
        for i in range(-min(m, 2), min(total_missionaries - m, 2) + 1):  # Ensure we don't exceed the number of missionaries
            for j in range(-min(c, 2), min(total_cannibals - c, 2) + 1):  # Ensure we don't exceed the number of cannibals
                if i + j < 0 and is_valid_move((-i, -j), state):
                    moves.append((-i, -j, 0))
    return moves

def heuristic(state):
    return abs(state[0] - state[1])

def astar(start_state):
    open_queue = queue.Queue()
    open_queue.put((heuristic(start_state), start_state, []))
    closed_set = set()

    while not open_queue.empty():
        _, current_state, actions = open_queue.get()

        if is_goal_state(current_state):
            return actions

        closed_set.add(current_state)

        for move in successors(current_state):
            next_state = (current_state[0] + move[0], current_state[1] + move[1], move[2])
            if next_state not in closed_set and is_valid_state(next_state):
                open_queue.put((heuristic(next_state), next_state, actions + [move]))

    return None

def main():
    global total_missionaries, total_cannibals

    print("\nMissionaries and Cannibals Game")
    print_instructions()

    # Get user input for initial number of missionaries and cannibals and validate
    while True:
        total_missionaries = int(input("Enter the total number of missionaries => "))
        total_cannibals = int(input("Enter the total number of cannibals => "))
        if total_missionaries >= 3 and total_missionaries >= total_cannibals:
            break
        else:
            print("Error: Initial number of missionaries must be at least 3 and cannot be less than the number of cannibals. Please try again.")

    start_state = (total_missionaries, total_cannibals, 1)  # Initial state: missionaries, cannibals, boat on the left side
    print("\n")
    print_state(start_state)

    while not is_goal_state(start_state):
        move = get_user_input(start_state)
        if is_valid_move(move, start_state):
            if start_state[2] == 1:  # Boat travels from left to right
                start_state = (start_state[0] - move[0], start_state[1] - move[1], 1 - start_state[2])
            else:  # Boat travels from right to left
                start_state = (start_state[0] + move[0], start_state[1] + move[1], 1 - start_state[2])
            print_state(start_state)
            if (start_state[0] < start_state[1] and start_state[0] > 0) or (total_missionaries - start_state[0] < total_cannibals - start_state[1] and total_missionaries - start_state[0] > 0):
                print("Cannibals eat missionaries:\nYou lost the game!")
                return

            if start_state[0] == 0 and start_state[1] == 0:
                print("Congratulations! You have reached the goal state.")
                return
        else:
            print("Invalid move! Try again.")

main()
