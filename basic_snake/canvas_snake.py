from tkinter import *
import time
import random
import inspect, os
from decimal import Decimal as D
import time

# max at w=63, h=30
time_between = 300
can_width = 30
can_height = 30
xscale = 20
yscale = 20
foods = 5
length = 1
length_increase = 1
start_color = 0x00ff00
end_color = 0x0000ff

original_length = length*1
spots = []
color_dict = {'O':'#ffffff', 'F':'#ffff00', 'H':'#00ff00', 'T':'#00ffff'}
color_list = []
total_spots = can_width * can_height

def build_color_list():
    global color_list, start_color, end_color
    a = start_color
    b = end_color
    for i in range(0xff):
        a -= int(D(str(start_color))/D('255'))
        b += int(D(str(end_color))/D('255'))
        res = a + b
        color_list.append('#' + ("%06x" % res))
    color_list.append('#' + ("%06x" % end_color))

def start(arg):
    global started, stopped
    if not started:
        started = True
        stopped = False
        move()

def stop(event=None):
    global started, stopped
    stopped = True
    started = False

def move():
    global direction, started, stopped
    if started:
        update_board(direction, board)
        root.update()
    # After 1 second, call scanning again (create a recursive loop)
    if stopped:
        return
    root.after(time_between, move)


def right(arg):
    global direction
    direction = (0, 1)

def down(arg):
    global direction
    direction = (1, 0)

def left(arg):
    global direction
    direction = (0, -1)

def up(arg):
    global direction
    direction = (-1, 0)

def update_board(direction, board):
    global length, spots, color_list, color_dict
    my_text.delete(1.0, END)
    my_text.insert(END, length)
    board_width = len(board[0])
    board_height = len(board)
    empty_spots = []
    counter = 0

    for new_row in range(board_height):
        for new_col in range(board_width):
            if board[new_row][new_col][0] == 'O':
                empty_spots.append((new_row, new_col))
            if board[new_row][new_col][1] != 0:

                if board[new_row][new_col][0] == 'H':
                    pos = new_row, new_col
                    board[new_row][new_col][0] = 'T'
                board[new_row][new_col][1] += 1
            counter+=1
    live, board = check_head(pos, board, direction, board_width, board_height, empty_spots)
    if live == False:
        stop()
        my_text.delete(1.0, END)
        my_text.insert(END, length)
        print(length)
    counter = 0
    for new_row in range(board_height):
        for new_col in range(board_width):
            if board[new_row][new_col][0] == 'F':
                w.itemconfig(spots[counter], fill=color_dict['F'])
            val = board[new_row][new_col][1]
            if val !=0:
                if board[new_row][new_col][1] > length:
                    board[new_row][new_col] = ['O', 0]
                    color = '#ffffff'
                else:
                    index = int(255*board[new_row][new_col][1]/length)
                    color = color_list[index]
                w.itemconfig(spots[counter], fill=color)
            counter+=1

def new_food(empty_spots):
    global board, spots, color_dict, total_spots, foods, length
    if total_spots - foods - length > 0:
        pos = random.randrange(0, len(empty_spots))
        board[empty_spots[pos][0]][empty_spots[pos][1]] = ['F', 0]


def check_head(pos, board, direction, board_width, board_height, empty_spots):
    global length
    if (0 > pos[0]+direction[0] or board_height == pos[0]+direction[0]):
        return False, board
    if  (0 > pos[1]+direction[1] or board_width == pos[1]+direction[1]):
        return False, board
    if board[pos[0]+direction[0]][pos[1]+direction[1]][1] != 0:
        return False, board
    if board[pos[0]+direction[0]][pos[1]+direction[1]][0] == 'F':
        length+=length_increase

        if total_spots - foods - length > 0:
            new_food(empty_spots)
    board[pos[0]+direction[0]][pos[1]+direction[1]] = ['H', 1]
    return True, board

def initialize_board():
    global spots
    w.delete('all')
    counter = 0
    for new_row in range(can_height):
        for new_col in range(can_width):
            # color = color_dict[board[new_row][new_col][0]]
            spots.append(counter)
            if board[new_row][new_col][1] != 0:
                index = int(255*board[new_row][new_col][1]/length)
                color = color_list[index]
            else:
                color = color_dict[board[new_row][new_col][0]]
            spots[counter] = w.create_rectangle(new_col*xscale, new_row*yscale, new_col*xscale+xscale, new_row*yscale+yscale, fill=color)
            counter+=1

def reset(event=None):
    global direction, started, stopped, board, can_width, can_height, foods, length, original_length, time_between
    direction = (0, 1)
    started = False
    stopped = True
    length = original_length
    board = [[['O', 0] for x in range(can_width)] for y in range(can_height)]
    board[can_height//2][can_width//2] = ['H', 1]

    empty_spots = []
    for row in range(can_height):
        for col in range(can_width):
            if board[row][col][0] == 'O':
                empty_spots.append((row, col))
    for food in range(foods):
        new_food(empty_spots)

    initialize_board()

direction = (0, 1)
started = False
stopped = True
board = [[['O', 0] for x in range(can_width)] for y in range(can_height)]
board[can_height//2][can_width//2] = ['H', 1]

empty_spots = []
for row in range(can_height):
    for col in range(can_width):
        if board[row][col][0] == 'O':
            empty_spots.append((row, col))
for food in range(foods):
    new_food(empty_spots)
build_color_list()

root = Tk()
root.state('zoomed')
widget = Button(root, command=reset, bg='red3', text = 'RESET')
widget.pack()
my_text = Text(root, width=5, height=1)
my_text.pack()

w = Canvas(root, width=xscale*can_width, height=yscale*can_height, highlightthickness=0, bg='#000000')
w.pack()

initialize_board()

root.bind_all("<space>", start)
root.bind_all("<Right>", right)
root.bind_all("<Down>", down)
root.bind_all("<Left>", left)
root.bind_all("<Up>", up)

root.bind_all("<Return>", start)
root.bind_all("d", right)
root.bind_all("s", down)
root.bind_all("a", left)
root.bind_all("w", up)

root.bind_all('R', reset)
root.bind_all('P', stop)
root.mainloop()
