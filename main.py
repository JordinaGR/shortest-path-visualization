from tkinter import *
from collections import deque as queue
import time
from tkinter.ttk import Combobox
from venv import create
from mazes import maze1, maze2
import sys

sys.setrecursionlimit(5000)

root = Tk()
root.config(bg='white')
root.minsize(1100, 600)
root.title('Shortes Path')
canvas = Canvas(root, width=700, height=700, bg='white')
canvas.pack(side=LEFT)
info_label = Label(root, text='', bg='white', fg='red', font=('arial', 15))
info_label.place(x=710, y=65)

a = maze1

n = 50
m = 50
resise_img = 700

whichChar = StringVar()
whichAlg = StringVar()
choseMaze = StringVar()

for j in range(n):
    for i in range(n):
        a[j] = list(a[j])

final_row = -1
final_col = -1

# colors
# wall = X
# wall edited from gui = x
# path = A
# cell = .
# start = S
# end = E
# cell which must go through = M

wall_colo = 'red'
path_colo = 'black'
ablep_colo = 'white'
start_colo = 'blue'
end_colo = '#CCCC00'
bfs_colo = '#C0C0C0'
bfs_colo2 = '#FF9933'

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

def reset_arrayA():
    for i in range(n):
        for j in range(m):
            if a[i][j] == 'A':
                a[i][j] = '.'

    return

def reset_variables():
    global dist, row, col, final_col, final_row, a

    reset_arrayA()

    for j in range(n):
        for i in range(n):
            a[j] = list(a[j])

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

def drawdata(x, y, col):
    global canvas
    
    canvas.create_rectangle(x*14, y*14, (x*14)+14, (y*14)+14, fill=col)
    #time.sleep(0.0005)
    #root.update_idletasks()

def print_matrix(matrix):
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 'X' or matrix[i][j] == 'x':
                drawdata(i, j, wall_colo)
            elif matrix[i][j] == '.':
                drawdata(i, j, ablep_colo)

            elif matrix[i][j] == 'S':
                drawdata(i, j, start_colo)

            elif matrix[i][j] == 'E':
                drawdata(i, j, end_colo)

            elif matrix[i][j] == 'A':
                drawdata(i, j, path_colo)

print_matrix(a)

def chose_maze_func():
    global chose_maze, a

    if choseMaze.get() == 'default':
        a = maze1
 
    elif choseMaze.get() == 'no walls':
        a = maze2

    else:
        pass

    for i in range(n):
        for j in range(m):
            if a[i][j] == 'x':
                a[i][j] = '.'

    reset_variables()
    print_matrix(a)

chose_maze_func()


def bfs(f, c, end):
    global final_row, final_col, canvas
    info_label.config(text='')
    q = queue()

    dist[f][c] = 0
    q.append((f, c))

    while (len(q) > 0):

        p = q.popleft()
        x = p[0]
        y = p[1]

        drawdata(x, y, bfs_colo)
        root.update_idletasks()

        for d in range(4):
            x2 = x + inc_x[d]
            y2 = y + inc_y[d]

            if (x2 >= 0 and x2 < n and y2 >= 0 and y2 < m and dist[x2][y2] == -1):
                dist[x2][y2] = dist[x][y] + 1
                if a[x2][y2] == end:
                    #print('Minium distance', dist[x2][y2])
                    info_label.config(text=f'Minium distance {dist[x2][y2]}')
                    final_row = x2
                    final_col = y2
                    time.sleep(0.5)
                    return True

                if a[x2][y2] == '.':
                    q.append((x2, y2))
                    drawdata(x2, y2, bfs_colo2)
                    root.update_idletasks()

    info_label.config(text="It's not reachable")
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

            if (x2 >= 0 and x2 < n and y2 >= 0 and y2 < m and dist[x2][y2] == var-1 and a[x2][y2] != 'X' and a[x2][y2] != 'x'):
                a[x2][y2] = 'A'
                var -= 1
                x = x2
                y = y2
                break
    return

flag = True
def dfs(x, y):
    global flag

    dist[x][y] = 0

    drawdata(x, y, bfs_colo)
    root.update_idletasks()
    
    for k in range(4):
        x2 = x + inc_x[k]
        y2 = y + inc_y[k]
        if (flag and x2 >= 0 and x2 < n and y2 >= 0 and y2 < m and a[x2][y2] != 'x' and a[x2][y2] != 'X' and dist[x2][y2] == -1):
            if (a[x2][y2] == 'E'):
                flag = False
                info_label.config(text='There\'s a path')
                return True
            else:
                dfs(x2, y2)
    
    if (flag):
        info_label.config(text='There\'s no path')
        return False

def execute_func():
    global must_cell_var, mustcord_x, mustcord_y, flag

    if which_alg.get() == 'BFS':
        x = bfs(row, col, 'E')
        if x:
            create_path()
            print_matrix(a)
    elif which_alg.get() == 'DFS':
        flag = True
        if dfs(row, col):
            print_matrix(a)

def reset_func():
    reset_variables()
    print_matrix(a)


def change_cells():
    global entry_x, entry_y, a, which_char, must_cell_var, mustcord_x, mustcord_y

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
            drawdata(x_cord, y_cord, start_colo)            
            drawdata(row, col, ablep_colo)
            reset_variables()
            return

        elif which_char.get() == 'End (yellow)':
            for i in range(n):
                for j in range(m):
                    if a[i][j] == 'E':
                        a[i][j] = '.'
                        a[x_cord][y_cord] = 'E'
                        drawdata(i, j, ablep_colo)
                        drawdata(x_cord, y_cord, end_colo)
                        reset_variables()
                        return

        elif which_char.get() == 'Wall/path (red/white)':
            if a[x_cord][y_cord] == '.':
                a[x_cord][y_cord] = 'x'
                drawdata(x_cord, y_cord, wall_colo)
                reset_variables()
                return
                
            elif a[x_cord][y_cord] == 'X' or a[x_cord][y_cord] == 'x':
                a[x_cord][y_cord] = '.'
                drawdata(x_cord, y_cord, ablep_colo)
                reset_variables()
                return
    
    reset_variables()

def bind_func(event):
    global mouse_x, mouse_y, entry_x, entry_y, which_char

    mouse_x = event.x
    mouse_y = event.y

    b = True

    for w in widget_list:
        if w is event.widget:
            b = False

    if mouse_x >= 14 and mouse_y >= 14 and mouse_x <= 686 and mouse_y <= 686 and which_char.get() != 'No' and b:
        cordx = mouse_x // 14
        cordy = mouse_y // 14

        entry_x.delete(0, END)
        entry_y.delete(0, END)

        entry_y.insert(0, cordy)
        entry_x.insert(0, cordx)

        change_cells()
    mouse_x = 0
    mouse_y = 0

def bind_auto(event):
    global mouse_x, mouse_y, entry_x, entry_y, which_char   
    mouse_x = event.x
    mouse_y = event.y

    b = True

    for w in widget_list:
        if w is event.widget:
            b = False

    if mouse_x >= 14 and mouse_y >= 14 and mouse_x <= 686 and mouse_y <= 686 and which_char.get() == 'Drag walls' and b:
        cordx = mouse_x // 14
        cordy = mouse_y // 14

        entry_x.delete(0, END)
        entry_y.delete(0, END)

        entry_y.insert(0, cordy)
        entry_x.insert(0, cordx)

        if a[cordx][cordy] == '.':
            drawdata(cordx, cordy, wall_colo)
            a[cordx][cordy] = 'x'
            reset_variables()

    mouse_x = 0
    mouse_y = 0

# graphics
execute = Button(root, text='FIND', bg='#45E180', width=6, command=execute_func)
execute.place(x=resise_img+10, y=10)

reset = Button(root, text='RESET', bg='white', width=6, command=reset_func)
reset.place(x=788, y=10)

chose_maze = Combobox(root, textvariable=choseMaze, width=10, values=['default', 'no walls'])
chose_maze.place(x=875, y=15)
chose_maze.current(['0'])

exe_chose_maze = Button(root, text='RESET\n MAZE', bg='white', width=6, command=chose_maze_func)
exe_chose_maze.place(x=985, y=10)

entry_x = Entry(root, width=5)
entry_y = Entry(root, width=5)

contr = Label(root, text="CONTROLS: ", bg='white', font=('arial', 12))
contr.place(x=resise_img+10, y=110)

which_char = Combobox(root, textvariable=whichChar, values=[
                      'Start (blue)', 'End (yellow)', 'Wall/path (red/white)', 'Drag walls'])
which_char.place(x=820, y=110)
which_char.current([3])

alg_label = Label(root, text="ALGORITHM: ", bg='white', font=('arial', 12))
alg_label.place(x=resise_img+10, y=150)

which_alg = Combobox(root, textvariable=whichAlg, values=['BFS', 'DFS'])
which_alg.place(x=820, y=150)
which_alg.current([1])

widget_list = [contr, alg_label, execute, reset, entry_x, entry_y, which_char, info_label, which_alg, exe_chose_maze, chose_maze]

root.bind('<Button 1>', bind_func)
root.bind('<B1-Motion>', bind_auto)

root.mainloop()