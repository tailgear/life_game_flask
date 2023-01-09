import random
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class GameOfLife(metaclass=SingletonMeta):
    def __init__(self, width=20, height=20):
        self.__width = width
        self.__height = height
        self.world = self.generate_universe()
        self.counter = 0

    def next_generation(self):

        if self.counter > 0:
            # clear dead 
            for i in range(len(self.world)):
                for j in range(len(self.world[0])):
                    if self.world[i][j] == -1:
                        self.world[i][j] = 0

            # new live or dead
            for i in range(len(self.world)):
                for j in range(len(self.world[0])):

                    if self.world[i][j] == 1:
                        if self.__get_near(self.world, [i, j]) not in (2, 3):
                            self.world[i][j] = -1
                        continue

                    if self.__get_near(self.world, [i, j]) == 3:
                        self.world[i][j] = 1
                        continue

        self.counter += 1

    def generate_universe(self):
        return [[random.randint(0, 1) for x in range(self.__width)] for y in range(self.__height)]

    @staticmethod
    def __get_near(universe, pos, system=None):
        if system is None:
            system = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

        count = 0
        for i in system:
            if universe[(pos[0] + i[0]) % len(universe)][(pos[1] + i[1]) % len(universe[0])] in (1, -1):
                count += 1
        return count