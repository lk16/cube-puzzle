import sys
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, auto
from typing import Dict, List, Set

CUBES = [
    3,
    1,
    3,
    1,
    1,
    1,
    1,
    2,
    1,
    1,
    1,
    1,
    1,
    2,
    1,
    3,
    1,
    2,
    2,
    3,
    1,
    2,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    3,
    1,
    3,
    1,
    3,
    3,
    3,
    2,
]


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int
    z: int

    def __add__(self, coord: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + coord.x, self.y + coord.y, self.z + coord.z)

    def __mul__(self, v: int) -> "Coordinate":
        return Coordinate(v * self.x, v * self.y, v * self.z)

    def is_valid(self) -> bool:
        return self.x in range(4) and self.y in range(4) and self.z in range(4)


START_CUBE = Coordinate(0, 0, 0)


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
    def __init__(self) -> None:
        self.occupied: Set[Coordinate] = set()
        self.cubes_offset = 0
        self.directions: List[Direction] = []
        self.max = 0
        self.start_time = datetime.now()
        self.attempts = 0

    def solve(self) -> None:
        self.occupied = {START_CUBE}
        self._solve(START_CUBE)

    def _solve(self, last_cube: Coordinate) -> None:
        if len(self.directions) > self.max:
            print(f"max: {len(self.directions)}", file=sys.stderr)
            self.max = len(self.directions)

        self.attempts += 1

        if self.attempts % 1_000_000 == 0:
            seconds = (datetime.now() - self.start_time).total_seconds()
            speed = self.attempts / seconds

            print(
                f"{self.attempts / 1_000_000:>7.0f} M attempts | {seconds:6.1f} seconds | {speed:.0f} attempts / sec",
                file=sys.stderr,
            )

        if self.cubes_offset == len(CUBES):
            self.print_solution()
            return

        new_coords_count = CUBES[self.cubes_offset]

        if self.directions:
            # not first move
            last_direction = self.directions[-1]
            next_directions = NEXT_DIRECTIONS[last_direction]
        else:
            next_directions = list(Direction)

        for direction in next_directions:
            new_coords: Set[Coordinate] = set()

            delta = COORD_DELTA[direction]

            for i in range(1, new_coords_count + 1):
                new_coords.add(last_cube + (delta * i))

            if not all(coord.is_valid() for coord in new_coords):
                continue

            if new_coords & self.occupied:
                continue

            next_last_cube = last_cube + (delta * new_coords_count)

            self.occupied |= new_coords
            self.cubes_offset += 1

            self.directions.append(direction)
            self._solve(next_last_cube)
            self.directions.pop()

            self.cubes_offset -= 1
            self.occupied -= new_coords

    def print_solution(self) -> None:
        print(" ".join(direction.name for direction in self.directions))


if __name__ == "__main__":
    Solver().solve()
