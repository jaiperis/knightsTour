# checking the starting position
def pos_check(pos, dim, p_board):
    while True:
        try:
            pos0, pos1 = [int(x) for x in pos]
            avoid = ['X', '*', '_']
            if (1 <= pos0 <= dim[0]) and (1 <= pos1 <= dim[1]) and (p_board[pos1 - 1][pos0 - 1][-1] not in avoid):
                return [pos0, pos1]
            else:
                pos = input('Invalid move! Enter your next move: ').split()
        except (ValueError, IndexError):
            pos = input('Invalid move! Enter your next move: ').split()


# checking the dimensions with loop
def dim_check():
    while True:
        dim = input('Enter your board dimensions: ').split()
        try:
            dimensions = [int(x) for x in dim]
            if (dimensions[0] > 0) and (dimensions[1] > 0) and (len(dimensions) == 2):
                return dimensions
            else:
                print('Invalid dimensions!')
        except (ValueError, IndexError):
            print('Invalid dimensions!')


# creating the board lines
def board(dim, lg, pos):
    game_board = [['_' * lg for col in range(dim[0])] for row in range(dim[1])]
    while True:
        try:
            pos0, pos1 = [int(x) for x in pos]
            if (1 <= pos0 <= dim[0]) and (1 <= pos1 <= dim[1]):
                position = [pos0, pos1]
                break
            else:
                pos = input('Invalid move! Enter your next move: ').split()
        except (ValueError, IndexError):
            pos = input('Invalid move! Enter your next move: ').split()
    return game_board, position


# updating the X and adding *
def pos_update(pos, u_board, lg):
    for row in range(0, len(u_board)):
        u_board[row] = list(map(lambda x: x.replace((' ' * (lg - 1)) + 'X', (' ' * (lg - 1)) + '*'), u_board[row]))
        for i in '012345678U':
            u_board[row] = list(map(lambda x: x.replace(' ' * (lg - 1) + i, '_' * lg), u_board[row]))
    u_board[pos[1] - 1][pos[0] - 1] = (' ' * (lg - 1)) + 'X'


# checking moves from position
def dir_check(pos, p_board, dim, lg):
    changes = [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
    row = pos[1] - 1
    col = pos[0] - 1
    int_count = 0
    # running through all possible changes
    for change in changes:
        r_change = row + change[0]
        c_change = col + change[1]
        if (0 <= r_change < dim[1]) and (0 <= c_change < dim[0]) and ('*' not in p_board[r_change][c_change]) and ('X' not in p_board[r_change][c_change]):
            # call for counting the spots option
            if lg == -1:
                # print(p_board[r_change][c_change])
                int_count += 1
            # call for updating the spots number
            else:
                ch_list = [c_change + 1, r_change + 1]
                p_board[r_change][c_change] = (' ' * (lg - 1)) + dir_check(ch_list, p_board, dim, -1)
    if lg == -1:
        return str(int_count)


# outputting board to user
def print_board(p_board, dim, lg):
    clean = {ord("'"): None, ord(','): None, ord('['): None, ord(']'): None}
    border = dim[0] * (lg + 1) + 3
    print(' ', '-' * border)
    for i in range(dim[1], 0, -1):
        line = str(i) + '| '
        for char in p_board[i - 1]:
            line += char + ' '
        print(line.translate(clean) + ' |')
    print(' ', '-' * border)
    inter = " " * lg
    print("  " + " " * lg + inter.join([str(x) for x in range(1, dim[0] + 1)]))


# ending the game
def end_game(pos, p_board, dim, lg):
    star_count = 1
    for row in p_board:
        star_count += row.count((' ' * (lg - 1)) + '*')
        # win
    if star_count == (dim[0] * dim[1]):
        return False, True
    # loss
    elif dir_check(pos, p_board, dim, -1) == '0':
        return False, False
    # continue
    else:
        return True, False


# counting loser's squares
def count_squares(p_board):
    total = 0
    for row in p_board:
        for square in row:
            if '_' not in square:
                total += 1
    return total


# automatically gets next position for AI
def auto_pos(p_board, track, int_count):
    max_num = ''
    col_row = []
    for row in range(0, len(p_board)):
        for col in range(0, len(p_board[0])):
            if (p_board[row][col][-1] in '01234567') and ([col, row] not in track[int_count]):
                if p_board[row][col][-1] > max_num:
                    max_num = p_board[row][col][-1]
                    col_row = [col + 1, row + 1]
    return col_row


# getting the index of count from a nested list
def nested_index(sol, int_count):
    for row in sol:
        for spot in row:
            if str(int_count) in spot:
                return [row.index(spot), sol.index(row)]


# back-tracking and recording bad spots
def back_track(p_board, lg, sol, track):
    global count
    # finding bad position and noting
    bad = nested_index(sol, count)
    track[count] = []
    count -= 1
    track[count].append(bad)
    p_board[bad[1]][bad[0]] = '_' * lg
    sol[bad[1]][bad[0]] = '_' * lg

    # updating board
    good = nested_index(sol, count)
    good_update = [good[0] + 1, good[1] + 1]
    pos_update(good_update, p_board, lg)
    return good_update


# making solution number
def sol_num(int_count, lg):
    num = ''
    while len(num) + len(str(int_count)) != lg:
        num += ' '
    return num + str(int_count)


# recursive AI function
def board_ai(pos, p_board, dim, lg, sol, track):
    global count
    sol[pos[1] - 1][pos[0] - 1] = sol_num(count, lg)
    dir_check(pos, p_board, dim, lg)

    # base case
    if (dir_check(pos, p_board, dim, -1) == '0') or (count == (dim[0] * dim[1])) or (auto_pos(p_board, track, count) == []):
        return pos

    # recursive case
    pos = auto_pos(p_board, track, count)
    pos_update(pos, p_board, lg)
    count += 1
    return board_ai(pos, p_board, dim, lg, sol, track)


# ask user to play game
def play_game():
    ans = input("Do you want to try the puzzle? (y/n): ")
    while True:
        if (ans != 'y') and (ans != 'n'):
            print("Invalid input!")
            ans = input("Do you want to try the puzzle? (y/n): ")
        else:
            return ans


# Functions above
# ============================
# Code to run below


# starter variables
int_dim = dim_check()
length = len(str(int_dim[0] * int_dim[1]))


# variables for ai
count = 1
track_dict = {}
for j in range(1, (int_dim[1] * int_dim[0]) + 1):
    track_dict[j] = []


# set up round
int_pos = input("Enter the knight's starting position: ").split()
board_list, int_pos = board(int_dim, length, int_pos)
play = play_game()
sol_list = board_list[:]
initial_pos = int_pos[:]
pos_update(int_pos, board_list, length)
possible = True
int_pos = board_ai(int_pos, board_list, int_dim, length, sol_list, track_dict)


# loop for AI
while True:
    # impossible
    if (count == 1) and (dir_check(int_pos, board_list, int_dim, -1) == str(len(track_dict[count]))):
        possible = False
        break
    # possible
    elif count == (int_dim[0] * int_dim[1]):
        possible = True
        break
    # backtrack and continue
    else:
        int_pos = back_track(board_list, length, sol_list, track_dict)
        # back tracking twice if spot is out of options
        if dir_check(int_pos, board_list, int_dim, -1) == str(len(track_dict[count])) and (count != 1):
            int_pos = back_track(board_list, length, sol_list, track_dict)
        # else it will just back track once
        int_pos = board_ai(int_pos, board_list, int_dim, length, sol_list, track_dict)


# adjust int_pos for player
int_pos = initial_pos
board_list, int_pos = board(int_dim, length, int_pos)
continue_game, result = end_game(int_pos, board_list, int_dim, length)
pos_update(int_pos, board_list, length)
track_dict = {}


if (play == 'y') and possible:
    # running the player game
    while continue_game:
        dir_check(int_pos, board_list, int_dim, length)
        print_board(board_list, int_dim, length)
        int_pos = input("Enter your next move: ").split()
        int_pos = pos_check(int_pos, int_dim, board_list)
        pos_update(int_pos, board_list, length)
        continue_game, result = end_game(int_pos, board_list, int_dim, length)

    # outputting result message
    # win
    if result:
        pos_update(int_pos, board_list, length)
        print_board(board_list, int_dim, length)
        print()
        print('What a great tour! Congratulations!')
    # loss
    else:
        pos_update(int_pos, board_list, length)
        print_board(board_list, int_dim, length)
        print()
        print('No more possible moves!')
        print(f'Your knight visited {count_squares(board_list)} squares!')
        print()
        print("Here's the solution!")
        print_board(sol_list, int_dim, length)

elif (play == 'n') and possible:
    print("Here's the solution!")
    print_board(sol_list, int_dim, length)

else:
    print('No solution exists!')
