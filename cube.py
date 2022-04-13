from __future__ import annotations

import sys
from copy import deepcopy
from datetime import datetime, timedelta
from enum import IntEnum, auto
from typing import Dict, List, Set

# fmt: off
MOVE_SIZES = [
    2, 3, 3, 3, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 2, 2, 1, 3, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 3
]
# fmt: on

CUBE_SIZE = 4

PRINT_INTERVAL = timedelta(seconds=1)


class Coordinate:
    __slots__ = "x", "y", "z"

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, coord: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + coord.x, self.y + coord.y, self.z + coord.z)

    def __mul__(self, v: int) -> "Coordinate":
        return Coordinate(v * self.x, v * self.y, v * self.z)

    def is_valid(self) -> bool:
        return (
            self.x in range(CUBE_SIZE)
            and self.y in range(CUBE_SIZE)
            and self.z in range(CUBE_SIZE)
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Coordinate):
            return False

        return o.x == self.x and o.y == self.y and o.z == self.z


START_CUBE = Coordinate(0, 0, 2)


class Direction(IntEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    FORWARD = auto()
    BACK = auto()


NEXT_DIRECTIONS: Dict[Direction, List[Direction]] = {
    Direction.UP: [Direction.LEFT, Direction.RIGHT, Direction.FORWARD, Direction.BACK],
    Direction.DOWN: [
        Direction.LEFT,
        Direction.RIGHT,
        Direction.FORWARD,
        Direction.BACK,
    ],
    Direction.LEFT: [Direction.UP, Direction.DOWN, Direction.FORWARD, Direction.BACK],
    Direction.RIGHT: [Direction.UP, Direction.DOWN, Direction.FORWARD, Direction.BACK],
    Direction.FORWARD: [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT],
    Direction.BACK: [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT],
}

COORD_DELTA: Dict[IntEnum, Coordinate] = {
    Direction.UP: Coordinate(0, 1, 0),
    Direction.DOWN: Coordinate(0, -1, 0),
    Direction.LEFT: Coordinate(-1, 0, 0),
    Direction.RIGHT: Coordinate(1, 0, 0),
    Direction.FORWARD: Coordinate(0, 0, -1),
    Direction.BACK: Coordinate(0, 0, 1),
}


class Solver:

    __slots__ = (
        "occupied",
        "move_id",
        "directions",
        "max",
        "start_time",
        "last_stats",
        "attempts",
        "solutions",
    )

    def __init__(self) -> None:
        self.occupied: Set[Coordinate] = set()
        self.move_id = 0
        self.directions: List[Direction] = []
        self.max = 0
        self.start_time = datetime.now()
        self.last_stats = self.start_time
        self.attempts = 0
        self.solutions: List[List[Direction]] = []

    def solve(self) -> None:
        self.occupied = {START_CUBE}
        self._solve(START_CUBE)
        self.print_solutions()
        self.print_stats()

    def _solve(self, last_cube: Coordinate) -> None:
        self.attempts += 1

        now = datetime.now()
        if now - self.last_stats > PRINT_INTERVAL:
            self.last_stats = now
            self.print_stats()

        if len(self.directions) == len(MOVE_SIZES):
            solution = deepcopy(self.directions)
            self.solutions.append(solution)
            return

        new_coords_count = MOVE_SIZES[self.move_id]

        if self.directions:
            # not first move
            last_direction = self.directions[-1]
            next_directions = NEXT_DIRECTIONS[last_direction]
        else:
            next_directions = list(Direction)

        for direction in next_directions:
            new_coords: Set[Coordinate] = set()

            delta = COORD_DELTA[direction]

            next_last_cube = last_cube + (delta * new_coords_count)

            if not next_last_cube.is_valid():
                continue

            for i in range(1, new_coords_count + 1):
                new_coords.add(last_cube + (delta * i))

            if new_coords & self.occupied:
                continue

            next_last_cube = last_cube + (delta * new_coords_count)

            self.occupied |= new_coords
            self.move_id += 1

            self.directions.append(direction)
            self._solve(next_last_cube)
            self.directions.pop()

            self.move_id -= 1
            self.occupied -= new_coords

    def print_stats(self) -> None:
        seconds = (datetime.now() - self.start_time).total_seconds()
        speed = self.attempts / seconds

        print(
            f"{self.attempts:>12,} attempts"
            + f" | {seconds:5,.0f} sec"
            + f" | {speed:,.0f} attempts / sec"
            + f" | {len(self.solutions)} solutions found",
            file=sys.stderr,
        )

    def print_solutions(self) -> None:
        for solution in self.solutions:
            print(
                ", ".join(
                    f"{direction.name} {move_size}"
                    for direction, move_size in zip(solution, MOVE_SIZES)
                )
            )
            print("---")


if __name__ == "__main__":
    Solver().solve()
