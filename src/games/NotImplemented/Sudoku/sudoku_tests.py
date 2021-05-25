# randomize rows, columns and numbers (of valid base pattern)
import random
from random import sample


base = 3
side = base * base


# pattern for a baseline valid solution
def pattern(r, c): return (base * (r % base) + r // base + c) % side


def shuffle(s): return sample(s, len(s))


rBase = range(base)
rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
print(rows)
cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
print(cols)
nums = shuffle(range(1, base * base + 1))

print('-----------')
print(f'nums_patter: {[pattern(r, c) for c in cols for r in rows]}')
print('(-------)')
# produce board using randomized baseline pattern
board = [[nums[pattern(r, c)] for c in cols] for r in rows]

for line in board: print(line)
print('------')


def shortSudokuSolve(board):
    size = len(board)
    block = int(size**0.5)
    board = [n for row in board for n in row]
    span = {(n, p): {(g, n) for g in
                     (n > 0) * [p // size, size + p % size, 2 * size + p % size // block + p // size // block * block]}
            for p in range(size * size) for n in range(size + 1)}
    empties = [i for i, n in enumerate(board) if n == 0]
    used = set().union(*(span[n, p] for p, n in enumerate(board) if n))
    empty = 0
    while 0 <= empty < len(empties):
        pos = empties[empty]
        used -= span[board[pos], pos]
        board[pos] = next((n for n in range(board[pos] + 1, size + 1) if not span[n, pos] & used), 0)
        used |= span[board[pos], pos]
        empty += 1 if board[pos] else -1
        if empty == len(empties):
            solution = [board[r:r + size] for r in range(0, size * size, size)]
            yield solution
            for e in solution:
                print(e)
            empty -= 1


# shortSudokuSolve([b for b in board if random.randint(0, 10) <= 5])


print(board[2])
# board[2] = [g*3 + r for g in shuffle(range(3)) for r in shuffle(range(3))]
print([pattern(r, c) for c in cols for r in rows])
print(board[2])
