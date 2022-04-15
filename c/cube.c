#include <stdio.h>
#include <stdint.h>
#include <sys/time.h>

#define CUBE_SIZE (4)

#define NUM_COORDS (CUBE_SIZE * CUBE_SIZE * CUBE_SIZE)

#define UP (0)
#define LEFT (1)
#define BACK (2)
#define FORWARD (3)
#define RIGHT (4)
#define DOWN (5)

#define NUM_DIRECTIONS (6)

const int direction_diff[NUM_DIRECTIONS] = {
    CUBE_SIZE, // UP
    -CUBE_SIZE * CUBE_SIZE, // LEFT
    1, // BACK
    -1, // FORWARD
    CUBE_SIZE * CUBE_SIZE, // RIGHT
    -CUBE_SIZE // DOWN
};

const char *direction_names[NUM_DIRECTIONS] = {
    "UP",
    "LEFT",
    "BACK",
    "FORWARD",
    "RIGHT",
    "DOWN"
};

#define TOTAL_MOVES (39)

const int moves_sizes[TOTAL_MOVES] = {
    2, 3, 3, 3, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 2, 2, 1, 3, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 3
};

int get_x(int c) {
    return (c >> 4) & 3;
}

int get_y(int c) {
    return (c >> 2) & 3;
}

int get_z(int c) {
    return c & 3;
}

double get_current_time() {
    struct timeval tv;
    gettimeofday(&tv, NULL);

    return ((double)tv.tv_sec) + (((double)tv.tv_usec) / 1000000);
}

struct solver_t {
    uint64_t attempts;
    int directions[TOTAL_MOVES];
    int move_id;
    uint64_t occupied;
    int solutions_found;
    int start_cube;
    double start_time;
};

void solver_init(struct solver_t *solver) {
    solver->attempts = 0;
    solver->move_id = 0;
    solver->occupied = 0;
    solver->solutions_found = 0;
    solver->start_cube = 0;
    solver->start_time = 0.0;
}

void solver_print_stats(struct solver_t *solver) {
    double seconds = get_current_time() - solver->start_time;
    double speed = ((double)solver->attempts) / seconds;

    fprintf(
        stderr,
        "%12ld attempts"
        " | %7.4f sec"
        " | %8.0f attempts / sec"
        " | %3d solutions found"
        " | searching for (%d,%d,%d)\n",
        solver->attempts,
        seconds,
        speed,
        solver->solutions_found,
        get_x(solver->start_cube),
        get_y(solver->start_cube),
        get_z(solver->start_cube)
    );
}

void solver_print_solution(struct solver_t *solver) {
    printf(
        "START: %d,%d,%d MOVES: ",
        get_x(solver->start_cube),
        get_y(solver->start_cube),
        get_z(solver->start_cube)
    );

    for (int move_id = 0; move_id < TOTAL_MOVES; move_id++) {
        if (move_id != 0) {
            printf(", ");
        }

        printf(
            "%s %d",
            direction_names[solver->directions[move_id]],
            moves_sizes[move_id]
        );
    }

    printf("\n");
}

void solver_solve(struct solver_t *solver, int last_cube) {
    solver->attempts++;

    if (solver->attempts % 10000000 == 0) {
        solver_print_stats(solver);
    }

    if (solver->move_id == TOTAL_MOVES) {
        solver->solutions_found++;
        solver_print_solution(solver);
        return;
    }

    int move_size = moves_sizes[solver->move_id];

    for (int direction = 0; direction < NUM_DIRECTIONS; direction++) {
        if (solver->move_id != 0) {
            int last_move = solver->directions[solver->move_id - 1];

            if (direction == last_move || direction == (5 - last_move)) {
                continue;
            }
        }

        int is_valid_move = 1;

        switch (direction) {
            case UP:
                if (get_y(last_cube) + move_size >= CUBE_SIZE) {
                    is_valid_move = 0;
                }
                break;
            case DOWN:
                if (get_y(last_cube) - move_size < 0) {
                    is_valid_move = 0;
                }
                break;
            case LEFT:
                if (get_x(last_cube) - move_size < 0) {
                    is_valid_move = 0;
                }
                break;
            case RIGHT:
                if (get_x(last_cube) + move_size >= CUBE_SIZE) {
                    is_valid_move = 0;
                }
                break;
            case FORWARD:
                if (get_z(last_cube) - move_size < 0) {
                    is_valid_move = 0;
                }
                break;
            case BACK:
                if (get_z(last_cube) + move_size >= CUBE_SIZE) {
                    is_valid_move = 0;
                }
                break;
        }

        if (!is_valid_move) {
            continue;
        }

        uint64_t move_occupy_set = 0;
        for (int step = 1; step <= move_size; step++) {
            int new_coord = last_cube + (direction_diff[direction] * step);
            move_occupy_set |= (1ull << new_coord);
        }

        if (solver->occupied & move_occupy_set) {
            continue;
        }

        int next_last_cube = last_cube + (direction_diff[direction] * move_size);

        solver->occupied |= move_occupy_set;
        solver->directions[solver->move_id] = direction;
        solver->move_id++;
        solver_solve(solver, next_last_cube);
        solver->move_id--;
        solver->occupied &= (~move_occupy_set);
    }
}

void solver_solve_all(struct solver_t *solver) {
    solver->start_time = get_current_time();
    for (int start_cube = 0; start_cube < NUM_COORDS; start_cube++) {
        solver->start_cube = start_cube;
        solver->occupied = (1ull << start_cube);
        solver_solve(solver, start_cube);
    }
    solver_print_stats(solver);
}

int main() {
    struct solver_t solver;
    solver_init(&solver);
    solver_solve_all(&solver);
    return 0;
}
