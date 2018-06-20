from tkinter import *
import random

WIDTH = 800
HEIGHT = 600
X_CHAR = WIDTH // 2
Y_CHAR = HEIGHT // 2
BULL_SPEED = 2
CHAR_SIZE = 40
BULL_SIZE_1 = 8
BULL_SIZE_2 = 4
bullets = dict()
SPEED_CHAR = 32
sum_1, sum_2 = 0, 0
pr_1, pr_2 = '00', '00'
P_S = 0


def draw():
    x = random.choice((random.randrange(0, abs(X_CHAR - CHAR_SIZE) + 1),
                       random.randrange(X_CHAR + CHAR_SIZE, abs(WIDTH - CHAR_SIZE) + 1)))
    y = random.choice((random.randrange(0, abs(Y_CHAR - CHAR_SIZE) + 1),
                       random.randrange(Y_CHAR + CHAR_SIZE, abs(HEIGHT - CHAR_SIZE // 2) + 1)))
    return c.create_oval(x, y, x + CHAR_SIZE, y + CHAR_SIZE, fill=random.choice(('orange', 'yellow', 'purple')))


def movement(self):
    global sum_1, sum_2, pr_1, pr_2
    x1, y1, x2, y2 = c.coords(self)
    if (Y_CHAR + CHAR_SIZE) >= y1 >= Y_CHAR:
        posx, posy = (x1 - 15) if X_CHAR <= x1 else (x2 + 15), y1 + CHAR_SIZE // 2
        bullets[
            c.create_oval(posx, posy, posx + BULL_SIZE_1, posy + BULL_SIZE_2, fill='red')] = 0 if x1 >= X_CHAR else 2
    elif (X_CHAR + CHAR_SIZE) >= x1 >= X_CHAR:
        posx, posy = x1 + CHAR_SIZE // 2, (y1 - 15) if Y_CHAR <= y1 else (y2 + 15)
        bullets[
            c.create_oval(posx, posy, posx + BULL_SIZE_2, posy + BULL_SIZE_1, fill='red')] = 1 if y1 <= Y_CHAR else 3
    rand_1 = random.choice((0, 1))
    rand_2 = random.choice((1, -1))
    num = enemies.index(self)
    if (sum_1 if num == 0 else sum_2) == 80:
        if rand_1:
            c.move(self, rand_2, 0)
        else:
            c.move(self, 0, rand_2)
        if num == 0:
            sum_1 = 1
            pr_1 = str(rand_1) + ('0' if rand_2 == -1 else '1')
        else:
            sum_2 = 1
            pr_2 = str(rand_1) + ('0' if rand_2 == -1 else '1')
    else:
        pr = pr_1 if num == 0 else pr_2
        rand_1, rand_2 = int(pr[0]), (-1 if pr[1] == '0' else 1)
        if rand_1:
            c.move(self, rand_2, 0)
        else:
            c.move(self, 0, rand_2)
        if num == 0:
            sum_1 += 1
        else:
            sum_2 += 1


def checker(self):
    global P_S
    l, t, r, b = x1, y1, x2, y2 = c.coords(self)
    if c.coords(self)[3] <= 0:
        c.coords(self, x1, HEIGHT - CHAR_SIZE, x2, HEIGHT)
    if c.coords(self)[1] >= HEIGHT:
        c.coords(self, x1, 0, x2, CHAR_SIZE)
    if c.coords(self)[2] <= 0:
        c.coords(self, WIDTH - CHAR_SIZE, y1, WIDTH, y2)
    if c.coords(self)[0] >= WIDTH:
        c.coords(self, 0, y1, CHAR_SIZE, y2)
    for bull in bullets:
        lb, tb, rb, bb = c.coords(bull)
        if (lb <= l <= rb and tb <= t <= bb) or (lb <= r <= rb and tb <= b <= bb) or (
                lb <= r <= rb and tb <= t <= bb) or (lb <= l <= rb and tb <= b <= bb):
            del_bull = bull
            enemies.append(draw())
            enemies.pop(0 if enemies[0] == self else 1)
            c.delete(self)
            break
    try:
        bullets.pop(del_bull)
        c.delete(del_bull)
        P_S += 1
        c.itemconfig(text, text=P_S)
    except:
        pass


def movement_bull(bull):
    if bullets[bull] == 0:
        c.move(bull, -BULL_SPEED, 0)
    elif bullets[bull] == 2:
        c.move(bull, BULL_SPEED, 0)
    elif bullets[bull] == 1:
        c.move(bull, 0, BULL_SPEED)
    elif bullets[bull] == 3:
        c.move(bull, 0, -BULL_SPEED)
    x1, y1, x2, y2 = c.coords(bull)
    if x1 < 0 or y2 > HEIGHT or x2 > WIDTH or y1 < 0:
        return [bull]
    return []


root = Tk()
root.title('Game')
c = Canvas(root, width=WIDTH, height=HEIGHT, bg='blue')
character = c.create_rectangle(X_CHAR, Y_CHAR, X_CHAR + CHAR_SIZE, Y_CHAR + CHAR_SIZE, fill='black')
print(c.coords(character))
enemies = [draw(), draw()]
text = c.create_text(WIDTH / 2, HEIGHT / 8,
                     text=P_S,
                     font="Arial 20",
                     fill="white")


def main():
    movement(enemies[0])
    movement(enemies[1])
    checker(enemies[0])
    checker(enemies[1])
    try:
        checker(character)
    except:
        c.itemconfig(text, text=P_S - 1)
        c.create_text(WIDTH / 2, HEIGHT / 2,
                      text="GAME OVER!",
                      font="Arial 20",
                      fill="red")
        return 0
    del_b = list()
    for bull in bullets:
        del_b.extend(movement_bull(bull))
    for bull in del_b:
        bullets.pop(bull)
        c.delete(bull)
    root.after(10, main)


# Напишем функцию обработки нажатия клавиш

c.grid()
c.focus_set()


def movement_handler(event):
    global X_CHAR, Y_CHAR
    if event.keysym == "w":
        c.move(character, 0, -SPEED_CHAR)
        Y_CHAR -= SPEED_CHAR
    elif event.keysym == "s":
        c.move(character, 0, SPEED_CHAR)
        Y_CHAR += SPEED_CHAR
    elif event.keysym == "a":
        c.move(character, -SPEED_CHAR, 0)
        X_CHAR -= SPEED_CHAR
    elif event.keysym == "d":
        c.move(character, SPEED_CHAR, 0)
        X_CHAR += SPEED_CHAR
    elif event.keysym == "Up":
        bullets[c.create_oval(X_CHAR + CHAR_SIZE // 2, Y_CHAR - 11, X_CHAR + CHAR_SIZE // 2 + BULL_SIZE_2,
                              Y_CHAR - 11 + BULL_SIZE_1, fill='green')] = 3
    elif event.keysym == "Down":
        bullets[c.create_oval(X_CHAR + CHAR_SIZE // 2, Y_CHAR + CHAR_SIZE + 11, X_CHAR + CHAR_SIZE // 2 + BULL_SIZE_2,
                              Y_CHAR + CHAR_SIZE + 11 + BULL_SIZE_1, fill='green')] = 1
    elif event.keysym == "Left":
        bullets[c.create_oval(X_CHAR - 11, Y_CHAR + CHAR_SIZE // 2, X_CHAR - 11 + BULL_SIZE_1,
                              Y_CHAR + CHAR_SIZE // 2 + BULL_SIZE_2, fill='green')] = 0
    elif event.keysym == "Right":
        bullets[c.create_oval(X_CHAR + CHAR_SIZE + 11, Y_CHAR + CHAR_SIZE // 2, X_CHAR + CHAR_SIZE + 11 + BULL_SIZE_1,
                              Y_CHAR + CHAR_SIZE // 2 + BULL_SIZE_2, fill='green')] = 2


c.bind("<KeyPress>", movement_handler)
main()
root.mainloop()
