#this is the first version of the program, it's really bad. The other one is way better

import PIL.Image
from PIL import ImageDraw, ImageTk
from tkinter import *
from collections import deque as queue
import time
from tkinter.ttk import Combobox

root = Tk()
root.config(bg='white')
root.minsize(1100, 600)

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

path = a[::]

a_img = PIL.Image.new("RGB", (m*25, n*25), 'white')
dib_a = ImageDraw.Draw(a_img)

path_img = PIL.Image.new("RGB", (m*25, n*25), 'white')
dib_path = ImageDraw.Draw(path_img)

final_row = -1
final_col = -1

mapa_a = ImageTk.PhotoImage(PIL.Image.open("images/a.png"))
mapa_path = ImageTk.PhotoImage(PIL.Image.open("images/path.png"))

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


def dibuixa_casella(y, x, col, img):
    img.polygon([(25*x, 25*y), (25*x + 24, 25*y),
                 (25*x + 24, 25*y + 24), (25*x, 25*y + 24)], 'white', outline=0)
    img.polygon([(25*x, 25*y), (25*x + 24, 25*y),
                 (25*x + 24, 25*y + 24), (25*x, 25*y + 24)], col)


def dibuixa_punt(y, x, col, img):
    img.polygon([(25*x, 25*y), (25*x + 24, 25*y),
                 (25*x + 24, 25*y + 24), (25*x, 25*y + 24)], 'white', outline=0)
    img.ellipse([25*x + 5, 25*y + 5, 25*x + 19, 25*y + 19], col)


def draw_matrix(a, img):
    for i in range(n):
        for j in range(m):
            if a[i][j] == 'X':
                dibuixa_casella(i, j, 'red', img)

            elif a[i][j] == '.':
                dibuixa_punt(i, j, 'white', img)

            elif a[i][j] == 'S':
                dibuixa_casella(i, j, 'blue', img)

            elif a[i][j] == 'F':
                dibuixa_casella(i, j, 'yellow', img)

            elif a[i][j] == 'A':
                dibuixa_punt(i, j, 'black', img)


def bfs(f, c):
    global final_row, final_col, img, text_widget
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
    global path

    var = dist[final_row][final_col]
    x = final_row
    y = final_col

    while True:
        if x == row and y == col:
            path[row][col] = 'S'
            break

        for i in range(4):
            x2 = x + inc_x[i]
            y2 = y + inc_y[i]

            if (x2 >= 0 and x2 < n and y2 >= 0 and y2 < m and dist[x2][y2] == var-1 and a[x2][y2] != 'X'):
                path[x2][y2] = 'A'
                var -= 1
                x = x2
                y = y2
                break
    return


def reset_arrayA():
    global a
    for i in range(n):
        for j in range(m):
            if a[i][j] == 'A':
                a[i][j] = '.'

    return


def reset_variables():
    global path, dist, row, col, final_col, final_row, a

    reset_arrayA()
    path = a[::]

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


def generate_maps():
    global foto_mapa, path_img, mapa_path

    draw_matrix(a, dib_a)
    image_a = a_img.resize((resise_img, resise_img))
    image_a.save('images/a.png')

    x = bfs(row, col)
    if x is True:
        create_path()
        draw_matrix(path, dib_path)
        path_imagee = path_img.resize((resise_img, resise_img))
        path_imagee.save('images/path.png')

    else:
        path_imagee = a_img.resize((resise_img, resise_img))
        path_imagee.save('images/path.png')

    mapa_a = ImageTk.PhotoImage(PIL.Image.open("images/a.png"))
    mapa_path = ImageTk.PhotoImage(PIL.Image.open("images/path.png"))
    reset_variables()


generate_maps()
mapa_a = ImageTk.PhotoImage(PIL.Image.open("images/a.png"))
mapa_path = ImageTk.PhotoImage(PIL.Image.open("images/path.png"))


def execute_func():
    global mapa_path, foto_mapa

    generate_maps()

    foto_mapa.grid_forget()
    foto_mapa = Label(image=mapa_path)
    foto_mapa.grid(row=0, column=0)

    reset_arrayA()


def reset_print_map():
    global mapa_a, foto_mapa

    foto_mapa.grid_forget()
    foto_mapa = Label(image=mapa_a)
    foto_mapa.grid(row=0, column=0)


def reset_func():
    global path, dist, row, col, final_col, final_row, a

    reset_arrayA()
    path = a[::]

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

    reset_print_map()


def edit_matrix():
    global entry_x, entry_y, a, which_char, foto_mapa, mapa_a

    try:
        x_cord = int(entry_x.get())
        y_cord = int(entry_y.get())

    except:
        x_cord = 1
        y_cord = 1

    if x_cord <= 48 and x_cord > 0 and y_cord <= 48 and y_cord > 0 and (a[x_cord][y_cord] != 'S' and a[x_cord][y_cord] != 'F'):
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

        # actualitzar path, dist...
        # generar i guardar una imatge (a)
        # mostrar la imatge (a)

        reset_variables()

        draw_matrix(a, dib_a)
        image_a = a_img.resize((resise_img, resise_img))
        image_a.save('images/a.png')

        mapa_a = ImageTk.PhotoImage(PIL.Image.open("images/a.png"))


def edit_a_func():
    global foto_mapa, mapa_a
    edit_matrix()

    foto_mapa.grid_forget()
    foto_mapa = Label(image=mapa_a)
    foto_mapa.grid(row=0, column=0)


def get_origin(event):
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

        entry_y.insert(0, cordx)
        entry_x.insert(0, cordy)

        if a[cordx][cordy] == '.':
            a[cordx][cordy] = 'X'
        
        elif a[cordx][cordy] == 'X':
            a[cordx][cordy] = '.'

        edit_a_func()
    mouse_x = 0
    mouse_y = 0




# graphics
foto_mapa = Label(image=mapa_a)
foto_mapa.grid(row=0, column=0)

execute = Button(root, text='FIND', bg='white', command=execute_func, width=6)
execute.place(x=resise_img+10, y=10)

reset = Button(root, text='RESET', bg='white', command=reset_func, width=6)
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

change_button = Button(root, text='CHANGE', bg='white', command=edit_a_func)
change_button.place(x=990, y=135)

info = Label(root, text='Punta nord-oest és (1, 1) i sud-est (48, 48) \n sense contar les parets vermelles.',
             bg='white', font=('arial', 10))
info.place(x=resise_img+10, y=170)

widget_list = [execute, reset, explanation, entry_x, entry_y, which_char, change_button, info]

root.bind("<Button 1>", get_origin)

root.mainloop()
