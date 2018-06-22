# Вы играете за чёрный квадрат. Круги - ваши враги. Управление: WASD, стрелять - стрелочки.
from tkinter import *
import random
from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton,
                             QGridLayout, QWidget, QToolTip, QMessageBox, QLabel)
from PyQt5.QtGui import (QIcon, QFont)

WIDTH = 1800
HEIGHT = 900
X_CHAR = WIDTH // 2
Y_CHAR = HEIGHT // 2
CHAR_SIZE = 50
BULL_SIZE_1 = 12
BULL_SIZE_2 = 6
EN_SPEED = 1
BULL_SPEED = 4
bullets = dict()
no_shoots = dict()
k = 7  # между выстрелами проходит минимум k шагов
SPEED_CHAR = 32
P_S = 0
n = 3
sum = [0] * n
prev = ['00'] * n
enemies = list()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.text = QLabel('Enemies and bullets move much slower.\n '
                           'The only potential danger is to catch up with your projectile.')
        self.initUI(self.text)

    def initUI(self, text):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.text_main = QLabel('Choose Skill Level:', self)
        self.button1 = QPushButton('I`m too young to die.', self)
        self.button2 = QPushButton('Hey, not too rough.', self)
        self.button3 = QPushButton('Hurt me plenty.', self)
        self.button4 = QPushButton('Ultra-Violence.', self)
        self.button5 = QPushButton('Nightmare!', self)
        self.button6 = QPushButton('Play!', self)
        self.textfield = QLineEdit(self)
        self.textfield.setToolTip('Количество врагов')
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.text_main, 1, 1, 1, 2)
        self.grid.addWidget(self.button1, 2, 1)
        self.grid.addWidget(self.button2, 3, 1)
        self.grid.addWidget(self.button3, 4, 1)
        self.grid.addWidget(self.button4, 5, 1)
        self.grid.addWidget(self.button5, 6, 1)
        self.grid.addWidget(self.button6, 8, 1, 8, 2)
        self.grid.addWidget(self.textfield, 7, 1)
        self.grid.addWidget(text, 2, 2, 7, 2)
        self.setLayout(self.grid)
        self.button1.clicked.connect(self.easy)
        self.button2.clicked.connect(self.normal)
        self.button3.clicked.connect(self.hard)
        self.button4.clicked.connect(self.extreme)
        self.button5.clicked.connect(self.nightmare)
        self.button6.clicked.connect(self.play)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Game')
        self.show()

    def easy(self):
        global EN_SPEED, BULL_SPEED
        EN_SPEED = 1
        BULL_SPEED = 4
        self.text.setText('Enemies and bullets move much slower.\n '
                          'The only potential danger is to catch up with your projectile.')

    def normal(self):
        global EN_SPEED, BULL_SPEED
        EN_SPEED = 1
        BULL_SPEED = 8
        self.text.setText('Bullets move 2 times faster')

    def hard(self):
        global EN_SPEED, BULL_SPEED
        EN_SPEED = 2
        BULL_SPEED = 8
        self.text.setText('Enemies move 2 times faster\n than in normal mode')

    def extreme(self):
        global EN_SPEED, BULL_SPEED
        EN_SPEED = 4
        BULL_SPEED = 8
        self.text.setText('Enemies move really fast now!')

    def nightmare(self):
        global EN_SPEED, BULL_SPEED
        EN_SPEED = 8
        BULL_SPEED = 16
        self.text.setText('Enemies and bullets\n move faster than you!')

    def play(self):
        try:
            the_main()
        except:
            self.textfield.setText('Ууупс... Что-то пошло не так.')

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def the_main():
    global enemies

    def draw():
        try:
            x1 = random.randint(X_CHAR + CHAR_SIZE * 7, WIDTH - CHAR_SIZE)
        except:
            pass
        try:
            x2 = random.randint(0, X_CHAR - CHAR_SIZE * 6)
        except:
            pass
        try:
            x = random.choice((x1, x2))
        except:
            try:
                x = x1
            except:
                x = x2

        try:
            y1 = random.randint(Y_CHAR + CHAR_SIZE * 7, HEIGHT - CHAR_SIZE)
        except:
            pass
        try:
            y2 = random.randint(0, Y_CHAR - CHAR_SIZE * 6)
        except:
            pass
        try:
            y = random.choice((y1, y2))
        except:
            try:
                y = y1
            except:
                y = y2
        return c.create_oval(x, y, x + CHAR_SIZE, y + CHAR_SIZE,
                             fill=random.choice(
                                 ('orange', 'yellow', 'purple', 'brown', 'silver', 'darkgreen', 'darkgoldenrod')))

    def movement(self):
        global sum_1, sum_2, pr_1, pr_2
        x1, y1, x2, y2 = c.coords(self)
        if no_shoots[self] >= k:
            if (Y_CHAR + CHAR_SIZE) >= y1 >= Y_CHAR:
                posx, posy = (x1 - 20) if X_CHAR <= x1 else (x2 + 20), y1 + CHAR_SIZE // 2
                bullets[
                    c.create_oval(posx, posy, posx + BULL_SIZE_1, posy + BULL_SIZE_2,
                                  fill='red')] = 0 if x1 >= X_CHAR else 2
                no_shoots[self] = 0
            elif (X_CHAR + CHAR_SIZE) >= x1 >= X_CHAR:
                posx, posy = x1 + CHAR_SIZE // 2, (y1 - 20) if Y_CHAR <= y1 else (y2 + 20)
                bullets[
                    c.create_oval(posx, posy, posx + BULL_SIZE_2, posy + BULL_SIZE_1,
                                  fill='red')] = 1 if y1 <= Y_CHAR else 3
                no_shoots[self] = 0
            else:
                no_shoots[self] += 1
        else:
            no_shoots[self] += 1
        rand_1 = random.choice((0, 1))
        rand_2 = random.choice((1, -1))
        num = enemies.index(self)
        if sum[num] == 80:
            if rand_1:
                c.move(self, rand_2 * EN_SPEED, 0)
            else:
                c.move(self, 0, rand_2 * EN_SPEED)
            sum[num] = 1
            prev[num] = str(rand_1) + ('0' if rand_2 == -1 else '1')
        else:
            pr = prev[num]
            rand_1, rand_2 = int(pr[0]), (-1 if pr[1] == '0' else 1)
            if rand_1:
                c.move(self, rand_2 * EN_SPEED, 0)
            else:
                c.move(self, 0, rand_2 * EN_SPEED)
            sum[num] += 1

    def checker(self):
        global P_S, X_CHAR, Y_CHAR, enemies, no_shoots, bullets, sum, prev
        l, t, r, b = x1, y1, x2, y2 = c.coords(self)
        if c.coords(self)[3] <= 0:
            c.coords(self, x1, HEIGHT - CHAR_SIZE, x2, HEIGHT)
        if c.coords(self)[1] >= HEIGHT:
            c.coords(self, x1, 0, x2, CHAR_SIZE)
        if c.coords(self)[2] <= 0:
            c.coords(self, WIDTH - CHAR_SIZE, y1, WIDTH, y2)
        if c.coords(self)[0] >= WIDTH:
            c.coords(self, 0, y1, CHAR_SIZE, y2)
        X_CHAR, Y_CHAR, _1, _2 = c.coords(character)
        for bull in bullets:
            lb, tb, rb, bb = c.coords(bull)
            if bullets[bull] % 2 == 0:
                s1x, s1y = lb, tb + BULL_SIZE_2 // 2
                s3x, s3y = rb, tb + BULL_SIZE_2 // 2
                s2x, s2y = lb + BULL_SIZE_1 // 2, tb
                s4x, s4y = rb + BULL_SIZE_1 // 2, bb
            else:
                s1x, s1y = lb, tb + BULL_SIZE_1 // 2
                s3x, s3y = rb, tb + BULL_SIZE_1 // 2
                s2x, s2y = lb + BULL_SIZE_2 // 2, tb
                s4x, s4y = rb + BULL_SIZE_2 // 2, bb
            if (l <= s1x <= r and t <= s1y <= b) or (l <= s2x <= r and t <= s2y <= b) or (
                    l <= s3x <= r and t <= s3y <= b) or (l <= s4x <= r and t <= s4y <= b):
                del_bull = bull
                en = draw()
                enemies.append(en)
                no_shoots[en] = 0
                if self in enemies:
                    enemies.pop(enemies.index(self))
                    no_shoots.pop(self)
                    c.delete(self)
                else:
                    c.delete(character)
                    c.create_text(WIDTH / 2, HEIGHT / 2,
                                  text="GAME OVER!",
                                  font="Arial 20",
                                  fill="red")
                    P_S = 0
                    enemies = list()
                    no_shoots = dict()
                    bullets = dict()
                    X_CHAR = WIDTH // 2
                    Y_CHAR = HEIGHT // 2
                    sum = [0] * n
                    prev = ['00'] * n
                    return 0
                break
        try:
            bullets.pop(del_bull)
            c.delete(del_bull)
            P_S += 1
            c.itemconfig(text, text=P_S)
        except:
            pass
        return 1

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

    for _ in range(n):
        en = draw()
        enemies.append(en)
        no_shoots[en] = 0
    text = c.create_text(WIDTH / 2, HEIGHT / 8,
                         text=P_S,
                         font="Arial 20",
                         fill="white")

    def main():
        global P_S, X_CHAR, Y_CHAR, sum, prev
        for i in range(n):
            movement(enemies[i])
        for i in range(n):
            checker(enemies[i])
        bool_ = checker(character)
        if not bool_:
            c.unbind("<KeyPress>")
            return 0
        del_b = list()
        for bull in bullets:
            del_b.extend(movement_bull(bull))
        for bull in del_b:
            bullets.pop(bull)
            c.delete(bull)
        root.after(10, main)

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
            bullets[
                c.create_oval(X_CHAR + CHAR_SIZE // 2, Y_CHAR - 11 - CHAR_SIZE, X_CHAR + CHAR_SIZE // 2 + BULL_SIZE_2,
                              Y_CHAR - 11 - CHAR_SIZE + BULL_SIZE_1, fill='orange')] = 3
        elif event.keysym == "Down":
            bullets[
                c.create_oval(X_CHAR + CHAR_SIZE // 2, Y_CHAR + CHAR_SIZE * 2 + 11,
                              X_CHAR + CHAR_SIZE // 2 + BULL_SIZE_2,
                              Y_CHAR + CHAR_SIZE * 2 + 11 + BULL_SIZE_1, fill='orange')] = 1
        elif event.keysym == "Left":
            bullets[
                c.create_oval(X_CHAR - 11 - CHAR_SIZE, Y_CHAR + CHAR_SIZE // 2, X_CHAR - 11 - CHAR_SIZE + BULL_SIZE_1,
                              Y_CHAR + CHAR_SIZE // 2 + BULL_SIZE_2, fill='orange')] = 0
        elif event.keysym == "Right":
            bullets[c.create_oval(X_CHAR + 2 * CHAR_SIZE + 11, Y_CHAR + CHAR_SIZE // 2,
                                  X_CHAR + 2 * CHAR_SIZE + 11 + BULL_SIZE_1,
                                  Y_CHAR + CHAR_SIZE // 2 + BULL_SIZE_2, fill='orange')] = 2

    c.bind("<KeyPress>", movement_handler)
    main()

    root.mainloop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(""))
    window = Window()
    sys.exit(app.exec())
