from minesweeper import Minesweeper
import numpy as np
import copy
import keyboard
import time
from random import randint
from wrapper import CWrapper


class msai():
    def __init__(self):
        # self.grid = [[ 0,  1, -1, -1, -1, -1, -1, -1],
        #              [ 0,  1, -1, -1, -1, -1, -1, -1],
        #              [ 1,  3, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1]]

        self.possible_variants = []
        self.wrapper = CWrapper()

    def _tiles_around(self, x, y):
        if x == 0:
            # first column
            if y == 0:
                # first line
                return [[x, y+1], [x+1, y], [x+1, y+1]]

            elif y == len(self.grid) - 1:
                # last line
                return [[x, y-1], [x+1, y-1], [x+1, y]]

            else:
                # mid lines
                return [[x, y-1], [x+1, y-1], [x+1, y], [x+1, y+1], [x, y+1]]

        elif x == len(self.grid[0]) - 1:
            # last column
            if y == 0:
                # first line
                return [[x, y+1], [x-1, y], [x-1, y+1]]

            elif y == len(self.grid) - 1:
                # last line
                return [[x-1, y], [x-1, y-1], [x, y-1]]

            else:
                # mid lines
                return [[x, y-1], [x-1, y-1], [x-1, y], [x-1, y+1], [x, y+1]]

        else:
            # mid columns
            if y == 0:
                # first line
                return [[x-1, y], [x-1, y+1], [x, y+1], [x+1, y+1], [x+1, y]]

            elif y == len(self.grid) - 1:
                # last line
                return [[x-1, y], [x-1, y-1], [x, y-1], [x+1, y-1], [x+1, y]]

            else:
                # mid lines
                return [[x-1, y], [x-1, y-1], [x, y-1], [x+1, y-1], [x+1, y], [x+1, y+1], [x, y+1], [x-1, y+1]]


    def _find_mines(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        unknown, mines = 0, 0
        mine = []
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] == -1:
                unknown += 1
                mine.append([y, x])
            elif self.grid[x][y] == 9 or self.grid[x][y] == 19:
                mines += 1

        
        if unknown == self.grid[y0][x0] - mines:
            return mine
        else:
            return None

    def _find_safe(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        unknown, mines = 0, 0
        safe = []
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] == -1:
                unknown += 1
                safe.append([y, x])
            elif self.grid[x][y] == 9 or self.grid[x][y] == 19:
                mines += 1

        
        if self.grid[y0][x0] - mines == 0:
            return safe
        else:
            return None

    def _remove_duplicates(self, list):
        newList = []
        for i in list:
            if i not in newList:
                newList.append(i)
        return newList

    def solve(self, grid, mine_count, ms):
        self.grid = grid
        mines = []
        safe = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] != -1 and self.grid[y][x] != 0:
                    if m := self._find_mines(x, y):
                        mines += m

                    elif s := self._find_safe(x, y):
                        safe += s

        mines = self._remove_duplicates(mines)
        safe = self._remove_duplicates(safe)

        for tile in mines:
            ms.click(tile[0], tile[1], False)

        for tile in safe:
            ms.click(tile[0], tile[1], True)

        if len(mines) + len(safe) == 0:
            n = len(self.grid)
            m = len(self.grid[0])

            if self.grid[0][0] == -1:
                ms.click(0, 0, True)
            # elif self.grid[0][m - 1] == -1:
            #     ms.click(m - 1, 0, True)
            # elif self.grid[n - 1][0] == -1:
            #     ms.click(0, n - 1, True)
            # elif self.grid[n - 1][m - 1] == -1:
            #     ms.click(m - 1, n - 1, True)

            else:
                moves = self.wrapper.getBestMove(self.grid)

                if moves:
                    for is_safe, tile in moves:
                        time.sleep(.05)
                        ms.click(tile[0], tile[1], is_safe)
                else:
                    if self.grid[0][m - 1] == -1:
                        ms.click(m - 1, 0, True)
                    elif self.grid[n - 1][0] == -1:
                        ms.click(0, n - 1, True)
                    elif self.grid[n - 1][m - 1] == -1:
                        ms.click(m - 1, n - 1, True)
                    else:
                        x, y = randint(0, m), randint(0, n)
                        while grid[x][y] != -1: 
                            x, y = randint(0, m), randint(0, n)
                        ms.click(x, y, True)

        # print("mines", mines, "\nsafe", safe)
        return self.grid

    def _has_adj_num(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        tiles_with_num = 0
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] > 0 and self.grid[x][y] < 9:
                tiles_with_num += 1

        
        if tiles_with_num == 0:
            return False
        else:
            return True

    def _missing_mine(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        mines = 0
        for tile in adj_tiles:
            y, x = tile

            if self.grid[x][y] == 9 or self.grid[x][y] == 19:
                mines += 1
        
        return self.grid[y0][x0] > mines

    def _can_be_mine(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)

        for tile in adj_tiles:
            x, y = tile
            if not self._missing_mine(x, y) and self.grid[y][x] != -1:
                return False

        return True


    def _adj_mines(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        mines = 0
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] == 9 or self.grid[x][y] == 19:
                mines += 1

        return mines

    def _adj_unknown(self, x0, y0):
        adj_tiles = self._tiles_around( x0, y0)
        
        unknown = 0
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] == -1:
                unknown += 1

        return unknown

    def _is_valid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] > 0 and self.grid[y][x] < 9:
                    mines = self._adj_mines(x, y)
                    if self.grid[y][x] < mines or self.grid[y][x] - mines > self._adj_unknown(x, y):
                        return False
        return True

    def set_grid(self, grid):
        self.grid = grid

    def _possibilities(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == -1 and self._has_adj_num(x, y):
                    for n in (19, 10):
                        self.grid[y][x] = n

                        if self._is_valid():
                            self._possibilities()
                        
                        self.grid[y][x] = -1
                    return

        self.append_list(copy.deepcopy(self.grid))

    def append_list(self, list):
        self.possible_variants.append(list)

    def calculate_possibilities(self):
        self.possible_variants = []
        self._possibilities()

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                for grid in self.possible_variants:
                    if grid[y][x] == 19:
                        grid[y][x] = 1
                    elif grid[y][x] == 10:
                        grid[y][x] = -1
                    else:
                        grid[y][x] = 0
                    
        probability_matrix = np.array([ [0] * len(self.grid[0]) ] * len(self.grid))

        for grid in self.possible_variants:
            probability_matrix = np.add(probability_matrix, np.array(grid))

        probability_matrix = probability_matrix.tolist()

        for i in range(len(probability_matrix)):
            for j in range(len(probability_matrix[0])):
                probability_matrix[i][j] /= len(self.possible_variants)
            
        # -1 100% safe
        # 1  100% mines

        mine, mineX, mineY = probability_matrix[0][0], 0, 0
        safe, safeX, safeY = probability_matrix[0][0], 0, 0

        for i in range(len(probability_matrix)):
            for j in range(len(probability_matrix[0])):
                if probability_matrix[i][j] > mine:
                    mine = probability_matrix[i][j]
                    mineX = j
                    mineY = i
                elif probability_matrix[i][j] < safe:
                    safe = probability_matrix[i][j]
                    safeX = j
                    safeY = i

        # print(mine, mineX, mineY)
        # print(safe, safeX, safeY)

        no_best_tile = probability_matrix.count(0) != len(probability_matrix)
        if no_best_tile:
            probability_matrix = self.possible_variants[0]
            for i in range(len(probability_matrix)):
                for j in range(len(probability_matrix[0])):
                    if probability_matrix[i][j] > mine:
                        mine = probability_matrix[i][j]
                        mineX = j
                        mineY = i
                    elif probability_matrix[i][j] < safe:
                        safe = probability_matrix[i][j]
                        safeX = j
                        safeY = i
        
        if -1 * mine >= safe:
            return True, [safeX, safeY]
        else:
            return False, [mineX, mineY]



    
if __name__ == "__main__":
    ai = msai()

    # grid = [[0, 0, 0, 0, 0, 1, 9, 1, 0, 0, 0, 1, 3, 9, 3, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 2, 9, 2, 0, 0],
    #         [0, 0, 0, 0, 0, 2, 3, 3, 1, 0, 1, 3, 9, 9, 9, 2, 0, 2, 9, 2, 0, 0, 1, 1, 1, 2, 9, 3, 2, 2],
    #         [0, 0, 0, 0, 0, 1, 9, 9, 1, 0, 2, 9, 9, 6, 9, 2, 0, 2, 9, 3, 1, 0, 2, 9, 2, 1, 1, 2, 9, 9],
    #         [1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 3, 9, 6, 9, 3, 1, 0, 1, 2, 9, 1, 1, 3, 9, 2, 0, 0, 1, 2, 2],
    #         [1, 9, 2, 9, 1, 0, 0, 0, 2, 9, 4, 3, 9, 9, 2, 0, 0, 0, 1, 1, 1, 1, 9, 3, 2, 0, 0, 1, 2, 2],
    #         [1, 1, 2, 1, 1, 0, 0, 0, 2, 9, 9, 4, 4, 3, 2, 1, 1, 1, 2, 3, 2, 3, 4, 9, 3, 1, 0, 1, 9, 9],
    #         [0, 0, 0, 0, 0, 1, 1, 1, 1, 3, 4, 9, 9, 1, 1, 9, 1, 2, 9, 9, 9, 3, 9, 9, 9, 1, 0, 1, 3, 9],
    #         [0, 0, 1, 2, 2, 2, 9, 2, 1, 1, 9, 4, 3, 2, 1, 1, 1, 2, 9, 5, 4, 9, 3, 4, 3, 2, 0, 1, 2, 2],
    #         [1, 2, 2, 9, 9, 3, 3, 9, 2, 2, 1, 2, 9, 2, 1, 0, 0, 1, 2, 9, 2, 1, 1, 1, 9, 1, 0, 2, 9, 2],
    #         [9, 3, 9, 4, 2, 2, 9, 4, 9, 2, 0, 2, 3, 9, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 0, 2, 9, 2],
    #         [2, 4, 9, 2, 0, 1, 1, 3, 9, 3, 1, 2, 9, 2, 1, 1, 9, 2, 9, 1, 2, 9, 3, 1, 1, 0, 0, 1, 2, 2],
    #         [9, 2, 2, 2, 2, 2, 2, 2, 1, 2, 9, 2, 1, 1, 1, 2, 3, 3, 2, 2, 3, 9, 3, 9, 3, 3, 2, 1, 1, 9],
    #         [1, 1, 1, 9, 2, 9, 9, 1, 0, 1, 2, 3, 2, 1, 1, 9, 3, 9, 2, 2, 9, 4, 4, 3, 9, 9, 9, 1, 1, 1],
    #         [0, 1, 2, 2, 2, 2, 2, 1, 0, 0, 1, 9, 9, 1, 1, 2, 4, 9, 3, 3, 9, 9, 3, 9, 4, 9, 3, 1, 0, 0],
    #         [1, 3, 9, 2, 1, 2, 2, 1, 0, 1, 3, 4, 3, 2, 1, 2, 9, 3, 9, 2, 3, 9, 3, 1, 2, 1, 2, 2, 2, 1],
    #         [-1, -1, 9, 2, 1, 9, 9, 1, 0, 1, 9, 9, 1, 1, 9, 2, 1, 2, 1, 1, 1, 1, 1, 0, 0, 0, 1, 9, 9, 1]]

    # ai.set_grid(grid)
    # print(ai.calculate_possibilities())


    ms = Minesweeper()
    while keyboard.is_pressed('q') == False and not ms.game_over():
        ai.solve(ms.get_grid(), 10, ms) 

    ms.game_over()
