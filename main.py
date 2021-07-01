from tkinter import *
from collections import deque as queue
import time
from tkinter.ttk import Combobox

root = Tk()
root.config(bg='white')
root.minsize(1100, 600)
canvas = Canvas(root, width=700, height=700, bg='white')
canvas.pack(side=LEFT)

a = ['XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
     'XS..............X...........................XX..XX',
     'XXX.....X.................XX................X....X',
     'X..........X............................X........X',
     'X...X.................X....X..................X..X',
     'X........XXXX.X............................X.....X',
     'X....X............................X..............X',
     'X..X..X............................X.............X',
     'X....X..................X.X................X.....X',
     'X......X............................XX......XX...X',
     'X......X..................X................XX...XX',
     'X..X.....X...X..............X.............X......X',
     'X............X............................X......X',
     'X........X..................X....................X',
     'X..X.....X..................X...........XXX......X',
     'X.......X..................X.....................X',
     'X........X..............X...X......XX..........XXX',
     'X.......X..X..................X..............X...X',
     'XX.........X..................X..................X',
     'X..............X..................XX......X.....XX',
     'XXX.....X.................XX......X.......X......X',
     'X..........X.X................X..X...............X',
     'X...X.......X....X...............X............X..X',
     'X........XXXX.X............................X.....X',
     'X....X..................X........................X',
     'X..X..X.........X........X.........X.............X',
     'X....X.......................X....X.X......X.....X',
     'X......X.......X.....XX......X......X.......XX...X',
     'X......X............................X......XX...XX',
     'X..X.........X............................X......X',
     'X............X...........X..X.............X......X',
     'X........XX.......XXX.................X..........X',
     'X..X.....X........X...................X.XXX......X',
     'X.......X...................XX.......X...........X',
     'X........X.....XXX....................X......XXXXX',
     'X.......X........................X......X....X...X',
     'XX....................XX................X........X',
     'X.......X...........X...................X....X...X',
     'X......X............X...............X......XX...XX',
     'X..X.........X............................X......X',
     'X............X..............XXX...........X......X',
     'X........X.....X..............X.......X..........X',
     'X..X.....X.....X......................X.XXX......X',
     'X.......X................X........X..X...........X',
     'X........X............................X......XXXXX',
     'X.......X...............................X....X...X',
     'XX.....................X......X..................X',
     'X.......X...............................X....X...X',
     'XX.........X............................X.......FX',
     'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']

n = 50
m = 50
resise_img = 700
whichChar = StringVar()

for j in range(n):
    for i in range(n):
        a[j] = list(a[j])

final_row = -1
final_col = -1

# cordenades inici
row = -1
col = -1
for i in range(n):
    for j in range(m):
        if a[i][j] == 'S':
            row = i
            col = j

inc_x = [1, -1, 0, 0]
inc_y = [0, 0, 1, -1]
dist = [[-1 for i in range(m)] for i in range(n)]

def drawdata(x, y, col):
    global canvas
    
    canvas.create_rectangle(x*14, y*14, (x*14)+14, (y*14)+14, fill=col)
    #time.sleep(0.0005)
    root.update_idletasks()

def print_matrix(matrix):
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 'X':
                drawdata(i, j, 'red')
            elif matrix[i][j] == '.':
                drawdata(i, j, 'white')

            elif matrix[i][j] == 'S':
                drawdata(i, j, 'blue')

            elif matrix[i][j] == 'F':
                drawdata(i, j, 'yellow')

            elif matrix[i][j] == 'A':
                drawdata(i, j, 'black')

print_matrix(a)

def bfs(f, c):
    global final_row, final_col
    q = queue()

    dist[f][c] = 0
    q.append((f, c))

    while (len(q) > 0):

        p = q.popleft()
        x = p[0]
        y = p[1]

        for d in range(4):
            x2 = x + inc_x[d]
            y2 = y + inc_y[d]

            if (x2 >= 0 and x2 < n and y2 >= 0 and y2 < m and dist[x2][y2] == -1):
                dist[x2][y2] = dist[x][y] + 1
                if a[x2][y2] == 'F':
                    print('distància minima', dist[x2][y2])
                    final_row = x2
                    final_col = y2
                    return True

                if a[x2][y2] == '.':
                    q.append((x2, y2))

    return False


def create_path():
    var = dist[final_row][final_col]
    x = final_row
    y = final_col

    while True:
        if x == row and y == col:
            a[row][col] = 'S'
            break

        for i in range(4):
            x2 = x + inc_x[i]
            y2 = y + inc_y[i]

            if (x2 >= 0 and x2 < n and y2 >= 0 and y2 < m and dist[x2][y2] == var-1 and a[x2][y2] != 'X'):
                a[x2][y2] = 'A'
                var -= 1
                x = x2
                y = y2
                break
    return

def reset_arrayA():
    for i in range(n):
        for j in range(m):
            if a[i][j] == 'A':
                a[i][j] = '.'

    return

def reset_variables():
    global dist, row, col, final_col, final_row, a

    reset_arrayA()

    dist = [[-1 for i in range(m)] for i in range(n)]

    row = -1
    col = -1
    for i in range(n):
        for j in range(m):
            if a[i][j] == 'S':
                row = i
                col = j

    final_row = -1
    final_col = -1


def execute_func():
    x = bfs(row, col)
    if x:
        create_path()
        print_matrix(a)

def reset_func():
    reset_variables()
    print_matrix(a)


def change_cells(event):
    global entry_x, entry_y, a, which_char

    try:
        x_cord = int(entry_x.get())
        y_cord = int(entry_y.get())

    except:
        x_cord = 1
        y_cord = 1

    if x_cord <= 48 and x_cord > 0 and y_cord <= 48 and y_cord >0 and (a[x_cord][y_cord] != 'S' and a[x_cord][y_cord] != 'F'):
        if which_char.get() == 'Start (blue)':
            a[x_cord][y_cord] = 'S'
            a[row][col] = '.'

        elif which_char.get() == 'Finish (yellow)':
            for i in range(n):
                for j in range(m):
                    if a[i][j] == 'F':
                        a[i][j] = '.'
                        a[x_cord][y_cord] = 'F'
                        break

        elif which_char.get() == 'Wall/path (red/white)':
            if a[x_cord][y_cord] == '.':
                a[x_cord][y_cord] = 'X'
            elif a[x_cord][y_cord] == 'X':
                a[x_cord][y_cord] = '.'



# graphics
execute = Button(root, text='FIND', bg='white', width=6, command=execute_func)
execute.place(x=resise_img+10, y=10)

reset = Button(root, text='RESET', bg='white', width=6, command=reset_func)
reset.place(x=788, y=10)

explanation = Label(
    root, text="Enter coordinates (x, y), function and click the button.", bg='white', font=('arial', 12))
explanation.place(x=resise_img+10, y=105)

entry_x = Entry(root, width=5)
entry_x.place(x=resise_img+10, y=140)

entry_y = Entry(root, width=5)
entry_y.place(x=760, y=140)

which_char = Combobox(root, textvariable=whichChar, values=[
                      'No', 'Start (blue)', 'Finish (yellow)', 'Wall/path (red/white)'])
which_char.place(x=820, y=140)
which_char.current([0])

change_button = Button(root, text='CHANGE', bg='white', command=change_cells)
change_button.place(x=990, y=135)

info = Label(root, text='Punta nord-oest és (1, 1) i sud-est (48, 48) \n sense contar les parets vermelles.',
             bg='white', font=('arial', 10))
info.place(x=resise_img+10, y=170)

widget_list = [execute, reset, explanation, entry_x, entry_y, which_char, change_button, info]

root.mainloop()
