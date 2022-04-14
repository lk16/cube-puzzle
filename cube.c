#include <stdio.h>
#include <stdint.h>
#include <time.h>

#define total_moves (39)

const int moves_sizes[total_moves] = {
    2, 3, 3, 3, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 2, 2, 1, 3, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 3
};

const int cube_size = 4;

enum direction {
    UP = 0,
    DOWN = 5,
    LEFT = 1,
    RIGHT = 4,
    FORWARD = 3,
    BACK = 2
};


int get_x(int c) {
    return c & 3;
}

int get_y(int c) {
    return (c >> 2) & 3;
}

int get_z(int c) {
    return (c >> 4) & 3;
}

struct solver_t {
    uint64_t attempts;
    enum direction directions[total_moves];
    int move_id;
    uint64_t occupied;
    int solutions;
    int start_cube;
    int start_time;
};

void solver_init(struct solver_t *solver) {
    solver->attempts = 0;
    solver->move_id = 0;
    solver->occupied = 0;
    solver->solutions = 0;
    solver->start_cube = 0;
    solver->start_time = (int)time(NULL);
}

void solver_print_stats(struct solver_t *solver) {
    (void)solver;
    printf("TODO print stats\n");
}



void solver_solve(struct solver_t *solver, int last_cube) {
    (void)last_cube;

    solver->attempts++;

    if (solver->attempts % 100000 == 0) {
        solver_print_stats(solver);
    }

    // TODO



}

void solver_solve_all(struct solver_t *solver) {
    for (int coord_id = 0; coord_id < cube_size * cube_size * cube_size; coord_id++) {
        solver->occupied = (1 << coord_id);
        solver_solve(solver, coord_id);
    }


}


// class Solver:

//     def _solve(self, last_cube: Coordinate) -> None:
//         self.attempts += 1

//         now = datetime.now()
//         if self.attempts % 100_000 == 0:
//             self.print_stats()

//         if len(self.directions) == len(MOVE_SIZES):
//             solution = Solution(self.start_cube, deepcopy(self.directions))
//             self.solutions.append(solution)
//             return

//         new_coords_count = MOVE_SIZES[self.move_id]

//         if self.directions:
//             # not first move
//             last_direction = self.directions[-1]
//             next_directions = NEXT_DIRECTIONS[last_direction]
//         else:
//             next_directions = list(Direction)

//         for direction in next_directions:
//             new_coords: Set[Coordinate] = set()

//             delta = COORD_DELTA[direction]

//             next_last_cube = last_cube + (delta * new_coords_count)

//             if not next_last_cube.is_valid():
//                 continue

//             for i in range(1, new_coords_count + 1):
//                 new_coords.add(last_cube + (delta * i))

//             if new_coords & self.occupied:
//                 continue

//             next_last_cube = last_cube + (delta * new_coords_count)

//             self.occupied |= new_coords
//             self.move_id += 1

//             self.directions.append(direction)
//             self._solve(next_last_cube)
//             self.directions.pop()

//             self.move_id -= 1
//             self.occupied -= new_coords

//     def print_stats(self) -> None:
//         seconds = (datetime.now() - self.start_time).total_seconds()
//         speed = self.attempts / seconds

//         print(
//             f"{self.attempts:>12,} attempts"
//             + f" | {seconds:5,.0f} sec"
//             + f" | {speed:,.0f} attempts / sec"
//             + f" | {len(self.solutions):>3} solutions found"
//             + f" | searching for ({self.start_cube.x},{self.start_cube.y},{self.start_cube.z})",
//             file=sys.stderr,
//         )

//     def print_solutions(self) -> None:
//         for solution in self.solutions:
//             print(solution)
//             print("---")


// if __name__ == "__main__":
//     Solver().solve()

int main() {
    printf("Hello world\n");
    struct solver_t solver;
    solver_init(&solver);

    return 0;
}
