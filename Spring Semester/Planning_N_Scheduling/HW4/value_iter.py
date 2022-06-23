import os
import sys
import time
import numpy as np
from copy import deepcopy
from random import random, shuffle


ALGORITHM_NAME = "Value_Iteration"
Grid_Filename = "u_track.txt"
THIS_TRACK = "u_track"
START = "S"
GOAL = "F"
WALL = "#"
TRACK = "."
MAX_VELOCITY = 2
MIN_VELOCITY = -2
ACTION_COST = -1
CRASH_COST = -10.0  # how much crashing on the wall costs
GAMMA = 0.9  # discount rate, also known as gamma.
ERROR_THRES = 0.001  # end contition
PROB_ACCELER_FAILURE = 0.20  # Probability car will try to take action according to policy pi(s) = a and fail.
PROB_ACCELER_SUCCESS = 1 - PROB_ACCELER_FAILURE
NO_TRAINING_ITERATIONS = (
    10  # single training iteration runs through all possible states s
)
NO_RACES = 10
FRAME_TIME = 0.3  # How many seconds between frames printed to the console
MAX_STEPS = 500  # Maximum number of steps the car can take during time trial
MAX_TRAIN_ITER = 50  # Maximum number of training iterations


vel_range = range(MIN_VELOCITY, MAX_VELOCITY + 1)

# All possible actions the race car can take
actions = [(vy, vx) for vy in vel_range for vx in vel_range]
print("\nSize of all possible actions = ", len(actions))


def read_grid(filename):
    with open(filename, "r") as file:

        grid_data = file.readlines()

    file.close()

    grid = []

    # Adds a counter to each line in the grid_data list,
    for i, line in enumerate(grid_data):
        # ignore 1st line
        if i > 0:
            line = line.strip()

            if line == "":
                continue

            grid.append([x for x in line])

    return grid


def print_grid(grid, car_position=[0, 0]):
    """
    reads in the grid and currentposition of
    the car and prints the grid to the output
    :list grid
    :list car_position
    """
    # current position/location coordinates
    temp = grid[car_position[0]][car_position[1]]

    # car current location
    grid[car_position[0]][car_position[1]] = "X"

    time.sleep(FRAME_TIME)

    clear()

    # For each line in the grid
    for line in grid:

        text = ""

        for character in line:
            text += character

        print(text)

    grid[car_position[0]][car_position[1]] = temp


def clear():

    if sys.platform == "linux":
        os.system("clear")
    else:
        os.system("cls")  # windows enviroment clear terminal output


def get_random_start_position(grid):
    """
    This method reads in the grid and selects a random
    starting position on the racetrack (x, y). Note that
    (0,0) corresponds to the down left corner of the racetrack/grid.
    :list grid: list of lines

    :returns random starting coordinate (x,y) on the racetrack

    """
    # Collect all possible starting positions on the racetrack
    starting_positions = []

    # loop backwards
    for y, row in reversed(list(enumerate(grid))):

        for x, col in enumerate(row):

            # If we are at the starting position
            if col == START:

                # Add the coordiante to the list of available
                # starting positions in the grid
                starting_positions += [(y, x)]

    # Random shuffle the list of starting positions
    shuffle(starting_positions)

    return starting_positions[0]


def get_new_velocity(old_vel, accel, min_vel=MIN_VELOCITY, max_vel=MAX_VELOCITY):
    new_y = old_vel[0] + accel[0]
    new_x = old_vel[1] + accel[1]
    if new_x < min_vel:
        new_x = min_vel
    if new_x > max_vel:
        new_x = max_vel
    if new_y < min_vel:
        new_y = min_vel
    if new_y > max_vel:
        new_y = max_vel

    return new_y, new_x


def get_new_position(old_loc, vel, grid):
    y, x = old_loc[0], old_loc[1]
    vy, vx = vel[0], vel[1]

    return y + vy, x + vx


def get_nearest_open_cell(
    grid, y_crash, x_crash, vy=0, vx=(0), open=[TRACK, START, GOAL]
):
    """
    Locate the nearest open cell in order to handle crash scenario.
    Distance is calculated as the Manhattan distance.

    If velocity is provided, search in opposite direction of velocity so that
    there is no movement over walls
    parameters:
    -----------
    :list grid
    :int ycrash: y coordinate where crash happened
    :int xcrash: x coordinate where crash happened
    :int vy: velocity in y direction when crash occurred
    :int vx: velocity in x direction when crash occurred
    :list of strings open: Contains grid types

    :returns tuple of the nearest open y and x position on the racetrack
    """
    rows = len(grid)
    cols = len(grid[0])

    # Add expanded coverage for searching for nearest open cell
    max_radius = max(rows, cols)

    # a search radius for each scenario
    for radius in range(max_radius):

        if vy == 0:
            y_off_range = range(-radius, radius + 1)
        elif vy < 0:
            y_off_range = range(0, radius + 1)
        else:
            y_off_range = range(-radius, 1)

        for y_offset in y_off_range:

            y = y_crash + y_offset
            x_radius = radius - abs(y_offset)

            if vx == 0:
                x_range = range(x_crash - x_radius, x_crash + x_radius + 1)

            elif vx < 0:
                x_range = range(x_crash, x_crash + x_radius + 1)

            else:
                x_range = range(x_crash - x_radius, x_crash + 1)

            for x in x_range:

                if y < 0 or y >= rows:
                    continue
                if x < 0 or x >= cols:
                    continue

                if grid[y][x] in open:
                    return (y, x)

    return


def act(
    old_y,
    old_x,
    old_vy,
    old_vx,
    accel,
    grid,
    deterministic=(False),
    bad_crash=False,
):

    # This method is deterministic if the same output is returned given
    # the same input information
    if not deterministic:

        # If action fails (car fails to take the prescribed action a)
        if random() > PROB_ACCELER_SUCCESS:
            accel = (0, 0)

    new_vy, new_vx = get_new_velocity((old_vy, old_vx), accel)

    temp_y, temp_x = get_new_position((old_y, old_x), (new_vy, new_vx), (grid))

    new_y, new_x = get_nearest_open_cell(grid, temp_y, temp_x, new_vy, new_vx)
    # If a crash happens
    if new_y != temp_y or new_x != temp_x:

        # If this is a crash in which we would have to return to the
        # starting position
        if bad_crash and grid[new_y][new_x] != GOAL:

            # Return to the start of the race track
            new_y, new_x = get_random_start_position(grid)

        # Velocity of the race car is set to 0.
        new_vy, new_vx = 0, 0

    # Return the new state
    return new_y, new_x, new_vy, new_vx


def get_policy_from_Q(cols, rows, vel_range, Q, actions):
    # Create an empty dictionary called pi
    pi = {}

    # For each state s in the grid
    for y in range(rows):
        for x in range(cols):
            for vy in vel_range:
                for vx in vel_range:
                    pi[(y, x, vy, vx)] = actions[np.argmax(Q[y][x][vy][vx])]

    return pi


def value_iteration(
    grid, bad_crash=False, reward=(100.0), no_training_iter=NO_TRAINING_ITERATIONS
):

    rows = len(grid)
    cols = len(grid[0])

    values = [
        [[[random() for _ in vel_range] for _ in vel_range] for _ in (line)]
        for line in grid
    ]

    # Set the finish line states to 0
    for y in range(rows):
        for x in range(cols):
            # Terminal state has a value of 0
            if grid[y][x] == GOAL:
                for vy in vel_range:
                    for vx in vel_range:
                        values[y][x][vy][vx] = reward

    # Q[y][x][vy][vx][ai]
    Q = [
        [
            [[[random() for _ in actions] for _ in vel_range] for _ in (vel_range)]
            for _ in line
        ]
        for line in grid
    ]

    # Set finish line state-action pairs to 100
    for y in range(rows):
        for x in range(cols):
            # Terminal state has a value of 100
            if grid[y][x] == GOAL:
                for vy in vel_range:
                    for vx in vel_range:
                        for ai, a in enumerate(actions):
                            Q[y][x][vy][vx][ai] = reward

    for t in range(no_training_iter):

        values_prev = deepcopy(values)

        # When this value gets below the error threshold, we stop training.
        delta = 0.0

        for y in range(rows):
            for x in range(cols):
                for vy in vel_range:
                    for vx in vel_range:

                        # car crashes into a wall
                        if grid[y][x] == WALL:

                            values[y][x][vy][vx] = CRASH_COST

                            # set all the other wall states to a negative value
                            continue

                        for ai, a in enumerate(actions):

                            # The reward is ACTION_COST for every state except
                            # for the finish line states
                            if grid[y][x] == GOAL:
                                r = reward
                            else:
                                r = ACTION_COST

                            # Get the new state s'. s' is based on the current
                            # state s and the current action a
                            new_y, new_x, new_vy, new_vx = act(
                                y,
                                x,
                                vy,
                                vx,
                                a,
                                grid,
                                deterministic=True,
                                bad_crash=bad_crash,
                            )

                            # V(s'): value of the new state when taking action
                            # a from state s. This is the one step look ahead.
                            value_of_new_state = values_prev[new_y][new_x][new_vy][
                                new_vx
                            ]

                            # Get the new state s'. s' is based on the current
                            # state s and the action (0,0)
                            new_y, new_x, new_vy, new_vx = act(
                                y,
                                x,
                                vy,
                                vx,
                                (0, 0),
                                grid,
                                deterministic=(True),
                                bad_crash=bad_crash,
                            )

                            # V(s'): value of the new state when taking action
                            # (0,0) from state s. This is the value if for some
                            # reason the race car attemps to accelerate but
                            # fails
                            value_of_new_state_if_action_fails = values_prev[new_y][
                                new_x
                            ][new_vy][new_vx]

                            # Expected value of the new state s'
                            # Note that each state-action pair has a unique
                            # value for s'
                            expected_value = (
                                PROB_ACCELER_SUCCESS * value_of_new_state
                            ) + (
                                PROB_ACCELER_FAILURE
                                * (value_of_new_state_if_action_fails)
                            )

                            Q[y][x][vy][vx][ai] = r + (GAMMA * expected_value)

                        argMaxQ = np.argmax(Q[y][x][vy][vx])

                        values[y][x][vy][vx] = Q[y][x][vy][vx][argMaxQ]

        # Make sure all the rewards to 100 in the terminal state
        for y in range(rows):
            for x in range(cols):
                # Terminal state has a value of 100
                if grid[y][x] == GOAL:
                    for vy in vel_range:
                        for vx in vel_range:
                            values[y][x][vy][vx] = reward

        # See if the V(s) values are stabilizing
        # Finds the maximum change of any of the states. Delta is a float.
        delta = max(
            [
                max(
                    [
                        max(
                            [
                                max(
                                    [
                                        abs(
                                            values[y][x][vy][vx]
                                            - values_prev[y][x][vy][vx]
                                        )
                                        for vx in vel_range
                                    ]
                                )
                                for vy in (vel_range)
                            ]
                        )
                        for x in range(cols)
                    ]
                )
                for y in range(rows)
            ]
        )

        if delta < ERROR_THRES:
            return get_policy_from_Q(cols, rows, vel_range, Q, actions)

    return get_policy_from_Q(cols, rows, vel_range, Q, actions)


def do_time_trial(grid, policy, bad_crash=False, animate=True, max_steps=MAX_STEPS):
    grid_display = deepcopy(grid)

    # starting position on the race track
    starting_pos = get_random_start_position(grid)
    y, x = starting_pos
    vy, vx = 0, 0

    stop_clock = 0

    for i in range(max_steps):

        if animate:
            print_grid(grid_display, car_position=[y, x])

        a = policy[(y, x, vy, vx)]

        if grid[y][x] == GOAL:
            return i

        y, x, vy, vx = act(y, x, vy, vx, a, grid, bad_crash=bad_crash)

        if vy == 0 and vx == 0:
            stop_clock += 1
        else:
            stop_clock = 0

        if stop_clock == 5:
            return max_steps

    return max_steps


def main():
    crash_scenario = "closest_empty_cell"
    no_training_iter = int(
        input("Give a  number(int) of training iterations for first time : ")
    )
    print("\n training...")

    racetrack = read_grid(Grid_Filename)

    races = NO_RACES  # times to start a race

    while no_training_iter < MAX_TRAIN_ITER:

        # Keep track of the total number of steps
        total_steps = 0

        bad_crash = False

        # retrieve the policy
        policy = value_iteration(
            racetrack, bad_crash=bad_crash, no_training_iter=no_training_iter
        )

        for each_race in range(races):
            total_steps += do_time_trial(
                racetrack, policy, bad_crash=(bad_crash), animate=True
            )

        print("Number of Training Iterations: " + str(no_training_iter))
        print(
            "Average Number of Steps the car took "
            + str(total_steps / races)
            + " steps\n"
        )
        print("\n training. ...")

        # Delay
        time.sleep(FRAME_TIME + 5)

        # SAVE STATS INTO FILESS
        stats_file = THIS_TRACK
        stats_file += "_"
        stats_file += ALGORITHM_NAME + "_iter"
        stats_file += str(no_training_iter) + "_cr"
        stats_file += str(crash_scenario) + "_stats.txt"

        outfile_stat = open(stats_file, "w")

        outfile_stat.write(
            "------------------------------------------------------------------\n"
        )
        outfile_stat.write(ALGORITHM_NAME + " Summary Statistics\n")
        outfile_stat.write(
            "------------------------------------------------------------------\n"
        )
        outfile_stat.write("Track: ")
        outfile_stat.write(THIS_TRACK)
        outfile_stat.write("\nNumber of Training Iterations: " + str(no_training_iter))
        if crash_scenario == 1:
            outfile_stat.write("\nCrash Scenario: Return to the nearest cell" "\n")

        outfile_stat.write(
            "Average Number of Steps the Car Took "
            + str(total_steps / races)
            + " steps\n"
        )

        # Show functioning of the program
        trace_file = THIS_TRACK
        trace_file += "_"
        trace_file += ALGORITHM_NAME + "_iter"
        trace_file += str(no_training_iter) + "_cr"
        trace_file += str(crash_scenario) + "_trace.txt"

        if no_training_iter <= 5:

            outfile_tr = open(trace_file, "w")

            # Print trace runs that demonstrate proper functioning of the code
            outfile_tr.write(str(policy))

            outfile_tr.close()

        outfile_ts.close()

        no_training_iter += 5


main()