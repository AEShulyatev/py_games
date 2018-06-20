from tkinter import *
import random
WIDTH = 800
HEIGHT = 600
X_CHAR = WIDTH//2
Y_CHAR = WIDTH//2
BULL_SPEED = 5
IN_GAME = True
CHAR_SIZE = 40
BULL_SIZE_1 = 10
BULL_SIZE_2 = 5
bullets = dict()


def draw():
    x = random.choice((random.randrange(0, X_CHAR-CHAR_SIZE, CHAR_SIZE),
                       random.randrange(X_CHAR+CHAR_SIZE, WIDTH-CHAR_SIZE//2, CHAR_SIZE)))
    y = random.choice((random.randrange(0, Y_CHAR - CHAR_SIZE, CHAR_SIZE),
                       random.randrange(Y_CHAR + CHAR_SIZE, HEIGHT - CHAR_SIZE // 2, CHAR_SIZE)))
    return c.create_oval(x, y, x+CHAR_SIZE, y+CHAR_SIZE, fill=random.choice(('orange', 'yellow', 'purple')))


def movement(self):
    print(c.coords(self))
    x1, y1, x2, y2 = c.coords(self)
    if y1 == Y_CHAR:
        posx, posy = x1 if X_CHAR <= x1 else x2, y1
        bullets[c.create_oval(posx, posy, posx + BULL_SIZE_1, posy + BULL_SIZE_2, fill='red')] = 0 if x1 >= X_CHAR else 2
    elif x1 == X_CHAR:
        posx, posy = x1, y1 if Y_CHAR <= y1 else y2
        bullets[c.create_oval(posx, posy, posx + BULL_SIZE_2, posy + BULL_SIZE_1, fill='red')] = 1 if y1 <= Y_CHAR else 3
    if random.choice((1, 0)):
        c.move(self, random.choice((1, -1))*CHAR_SIZE, 0)
    else:
        c.move(self, 0, random.choice((1, -1))*CHAR_SIZE)
    if c.coords(self)[3] < 0:
        c.move(self, 0, -c.coords(self)[1])
    if c.coords(self)[1] > HEIGHT:
        c.move(self, 0, HEIGHT - c.coords(self)[3])
    if c.coords(self)[2] < 0:
        c.move(self, 0, -c.coords(self)[0]*2)
    if c.coords(self)[0] > WIDTH:
        c.move(self, 0, WIDTH - c.coords(self)[2])


def checker(self):
    global BULL_SPEED
    l, t, r, b = c.coords(self)
    for bull in bullets:
        lb, tb, rb, bb = c.coords(bull)
        if (lb <= l <= rb and tb <= t <= bb) or (lb <= r <= rb and tb <= b <= bb) or (lb <= r <= rb and tb <= t <= bb) or (lb <= l <= rb and tb <= b <= bb):
            del_bull = bull
            BULL_SPEED += 1
            a = draw()
            enemies.append(a)
            break
    try:
        bullets.pop(del_bull)
        c.delete(del_bull)
        enemies.pop(0 if enemies[0] == self else 1)
        c.delete(self)
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
character = c.create_rectangle(X_CHAR, Y_CHAR, X_CHAR+CHAR_SIZE, Y_CHAR+CHAR_SIZE, fill='black')
enemies = [draw(), draw()]


def main():
    movement(enemies[0])
    movement(enemies[1])
    checker(enemies[0])
    checker(enemies[1])
    del_b = list()
    for bull in bullets:
        del_b.extend(movement_bull(bull))
    for bull in del_b:
        bullets.pop(bull)
        c.delete(bull)
    root.after(100, main)


c.grid()
c.focus_set()
main()
root.mainloop()
