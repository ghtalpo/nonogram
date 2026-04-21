cx = 0
cy = 0

def run_nono(font_size):
    import tkinter as tk

    root = tk.Tk()
    root.title("The Nonogram")

    from tkinter import font
    fontOpt1 = font.Font(family="DejaVu Sans Mono", size=font_size)

    def paint_hints():
        # paint chints
        for i in range(len(chints)):
            g = []
            first = True
            c = 0
            for row in range(len(rhints)):
                match buttons[row][i]['text']:
                    case '*':
                        c = c + 1
                    case '#':
                        c = c + 1
                    case _:
                        if c > 0:
                            g.append(c)
                        c = 0
            if c > 0:
                g.append(c)

            hint = [int(x) for x in chints[i].get().split()]
            # print(i, g, hint, g== hint)
            if g != hint:
                clabels[i].config(bg = '#f00')
            else:
                clabels[i].config(bg = '#0f0')
                # fill empty cells with '?'
                for row in range(len(rhints)):
                    if buttons[row][i]['text'] == ' ':
                        buttons[row][i].config(text = '?')

        # paint rhints
        for i in range(len(rhints)):
            g = []
            first = True
            c = 0
            for col in range(len(chints)):
                match buttons[i][col]['text']:
                    case '*':
                        c = c + 1
                    case '#':
                        c = c + 1
                    case _:
                        if c > 0:
                            g.append(c)
                        c = 0
            if c > 0:
                g.append(c)

            hint = [int(x) for x in rhints[i].get().split()]
            # print(i, g, hint, g== hint)
            if g != hint:
                rlabels[i].config(bg = '#f00')
            else:
                rlabels[i].config(bg = '#0f0')
                # fill empty cells with '?'
                for col in range(len(chints)):
                    if buttons[i][col]['text'] == ' ':
                        buttons[i][col].config(text = '?')

    def mark_trivials():
        # for chints
        # print('rows?', rows)
        for i in range(len(chints)):
            hint = [int(x) for x in chints[i].get().split()]
            s = sum(hint) + len(hint)-1
            rem = rows - s
            # print(i, s, rem)
            pos = 0
            for j in range(len(hint)):
                if hint[j] >= rem:
                    startp = pos + rem
                    endp = pos + hint[j]
                    # print(':', i,j,hint[j], startp, endp)

                    for row in range(startp, endp):
                        buttons[row][i].config(text = '#')
                pos += hint[j] + 1

        # for rhints
        # print('cols?', rows)
        for i in range(len(rhints)):
            hint = [int(x) for x in rhints[i].get().split()]
            s = sum(hint) + len(hint)-1
            rem = cols - s
            # print(i, s, rem)
            pos = 0
            for j in range(len(hint)):
                if hint[j] > rem:
                    startp = pos + rem
                    endp = pos + hint[j]
                    # print(':', i,j,hint[j], startp, endp)

                    for col in range(startp, endp):
                        buttons[i][col].config(text = '#')
                pos += hint[j] + 1


    def clear_all():
        for y in range(rows):
            for x in range(cols):
                buttons[y][x].config(text = ' ', fg='black', bg='lightgray')


    def convert_temp_to_permanent():
        for y in range(rows):
            for x in range(cols):
                match buttons[y][x]['text']:
                    case '?':
                        buttons[y][x].config(text = 'X')
                    case '*':
                        buttons[y][x].config(text = '#')


    def clear_temps():
        for y in range(rows):
            for x in range(cols):
                if buttons[y][x]['text'] == '?' or buttons[y][x]['text'] == '*':
                    buttons[y][x].config(text = ' ')


    def save_data():
        # save all here
        ch = [x.get() for x in chints]
        # print("chints", ch)
        rh = [x.get() for x in rhints]
        # print("rhints", rh)

        m = []
        for row in range(rows):
            r = []
            for col in range(cols):
                r.append(buttons[row][col]['text'])
                match buttons[row][col]['text']:
                    case '#':
                        buttons[row][col].config(fg='red', bg='black')
                    case '*':
                        buttons[row][col].config(fg='magenta', bg='darkgray')
                    case '?':
                        buttons[row][col].config(fg='brown')
                    case 'X':
                        buttons[row][col].config(fg='black')
            m.append(r)

        import json
        encoded = json.dumps({'rows':rows, 'cols':cols, 'chints': ch, 'rhints': rh, 'map': m, 'cheight': cheight})
        encoded += '\n'
        with open('nono.json', 'w') as f:
            f.writelines(encoded)
            f.close()


    def init():
        try:
            with open('nono.json', 'r') as f:
                lines = f.readlines()
                import json
                d = json.loads(''.join(lines))
                # print('??', d)
                rows = d['rows']
                cols = d['cols']
                ch = d['chints']
                rh = [' '.join(x.split()) for x in d['rhints']]
                rwidth = max([len(x) for x in rh])
                if len(rh) != rows:
                    raise "#rh(%d)!= rows(%d)" % (len(rh), rows)
                m = d['map']
                cheight = d['cheight']
                ch = ['\n'.join(x.split()) for x in ch]
                if len(ch) != cols:
                    raise "#ch(%d)!= cols(%d)" % (len(ch), cols)
                if len(m) != rows or len(m[0]) != cols:
                    m = []
                    for row in range(rows):
                        r = []
                        for col in range(cols):
                            r.append(' ')
                        m.append(r)

                return (rows, cols, ch, rh, m, cheight, rwidth)
        except:
            print('init all')
            rows = 7 * 5
            cols = 6 * 5
            cheight = 7
            ch = ['' for x in range(cols)]
            rh = ['' for x in range(rows)]
            rwidth = max([len(x) for x in rh])
            m = []
            for row in range(rows):
                r = []
                for col in range(cols):
                    r.append(' ')
                m.append(r)

            return (rows, cols, ch, rh, m, cheight, rwidth)

    (rows, cols, ch, rh, m, cheight, rwidth) = init()

    buttons = []

    mode_text = tk.StringVar(root, value='A')

    def click_xy(x, y):
        match mode_text.get():
            case 'A':
                match buttons[y][x]['text']:
                    case ' ':
                        buttons[y][x].config(text = '?')
                    case '?':
                        buttons[y][x].config(text = 'X')
                    case 'X':
                        buttons[y][x].config(text = '*')
                    case '*':
                        buttons[y][x].config(text = '#')
                    case '#':
                        buttons[y][x].config(text = ' ')
                    case _:
                        buttons[y][x].config(text = ' ')
            case _:
                buttons[y][x].config(text = mode_text.get())

    def update_cursor(cx, cy, nx, ny):
        # clear old button color
        match buttons[cy][cx]['text']:
            case '#':
                buttons[cy][cx].config(fg='red',bg='black')
            case '*':
                buttons[cy][cx].config(fg='magenta', bg='darkgray')
            case _:
                buttons[cy][cx].config(fg='black',bg='lightgray')

        # paint new button color
        buttons[ny][nx].config(bg = 'gold')

    def onKeyPress(event):
        global cx
        global cy
        match event.keysym:
            case 'Left':
                nx = (cx - 1 + cols) % cols
                update_cursor(cx, cy, nx, cy)
                (cx, cy) = (nx, cy)
            case 'Right':
                nx = (cx + 1 + cols) % cols
                update_cursor(cx, cy, nx, cy)
                (cx, cy) = (nx, cy)
            case 'Up':
                ny = (cy - 1 + rows) % rows
                update_cursor(cx, cy, cx, ny)
                (cx, cy) = (cx, ny)
            case 'Down':
                ny = (cy + 1 + rows) % rows
                update_cursor(cx, cy, cx, ny)
                (cx, cy) = (cx, ny)
            case _:
                match event.char:
                    case '1':
                        mode_text.set('?')
                    case '2':
                        mode_text.set('X')
                    case '3':
                        mode_text.set('*')
                    case '4':
                        mode_text.set('#')
                    case '5':
                        mode_text.set(' ')
                    case 'q':
                        buttons[cy][cx].config(text = '?')
                    case 'w':
                        buttons[cy][cx].config(text = 'X')
                    case 'e':
                        buttons[cy][cx].config(text = '*')
                    case 'r':
                        buttons[cy][cx].config(text = '#')
                    case 't':
                        buttons[cy][cx].config(text = ' ')
                    case 'p':
                        clear_temps()
                    case 'a':
                        check()
                    case 's':
                        mark_trivials()
                    case 'Z':
                        clear_all()
                    case 'o':
                        convert_temp_to_permanent()
                    case _:
                        mode_text.set('A')
                # text.insert('end', 'You pressed %s\n' % (event.char, ))

    root.bind('<KeyPress>', onKeyPress)

    clabels = []
    chints = []
    for col in range(cols):
        chints.append(tk.StringVar(root, value=ch[col]))
        l = tk.Label(
            root,
            textvariable=chints[col],
            width=2,
            height = 10,
            anchor="s",
            font=fontOpt1,
        )
        col0 = int(col/5) * 6 + col%5
        l.grid(row=0, column=1+col0)
        clabels.append(l)

    import tkinter.ttk
    for col in range(5,cols+5,5):
        col0 = int(col/5) * 6 + col%5
        tkinter.ttk.Separator(root, orient="vertical").grid(row=0,column=col0, sticky='ns', rowspan=1+6+int(rows/5)*6,padx=2)

    rlabels = []
    rhints = []
    for row in range(rows):
        rhints.append(tk.StringVar(root, value=rh[row]))
        l = tk.Label(
            root,
            textvariable=rhints[row],
            width=rwidth,
            anchor="e",
            font=fontOpt1,
        )
        row0 = int(row/5) * 6 + row%5
        l.grid(row=row0+1+cheight, column=0)
        rlabels.append(l)

    for row in range(5,rows+5,5):
        row0 = int(row/5) * 6 + row%5
        tkinter.ttk.Separator(root, orient="horizontal").grid(row=cheight+row0,column=0, sticky='ew', columnspan=1+6+int(cols/5)*6, pady=2)

    tk.Button(
        root,
        text=f"CHK",
        width=1,
        height=1,
        command=lambda: check(),
    ).grid(row=0, column=0)

    def check():
        paint_hints()
        save_data()

    for row in range(rows):
        r = []
        for col in range(cols):
            b = tk.Button(
                root,
                text=m[row][col],
                width=1,
                height=1,
                command=lambda x=col, y=row: click_xy(x, y),
                font=fontOpt1,
            )
            col0 = int(col/5) * 6 + col%5
            row0 = int(row/5) * 6 + row%5
            b.grid(row=row0+1+cheight, column=col0+1)

            bg = 'lightgray'
            if col == cy and row == cx:
                bg = 'cyan'
            b.config(bg=bg)
            r.append(b)
        buttons.append(r)

    mode_label = tk.Label(
        root,
        textvariable=mode_text,
        width=3,
        height = 8,
        anchor="s",
    )
    mode_label.grid(row=row+1+cheight+row, column=0)

    root.mainloop()

if __name__ == '__main__':
    import sys
    try:
        font_size = int(sys.argv[1])
        run_nono(font_size)
    except Exception as e:
        print(e)
        print('usage: python %s <font_size>' % sys.argv[0])

