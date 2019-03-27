from tkinter import Tk, Canvas, NW
from PIL import Image, ImageTk
from skimage import io
from scipy.misc import imresize
import random


def check(enemie):
    global GAME_END
    x = enemie
    arr = c.coords(x)
    sep1, sep2 = c.coords(separators[enemies_ind_size[x][0]]), c.coords(separators[enemies_ind_size[x][0] + 1])
    # print(arr, sep1, sep2)
    if sep1[2] > arr[0] or arr[1] > HEIGHT:
        c.create_text(WIDTH // 2, HEIGHT // 3,
                      text="GAME OVER!",
                      font="Arial 20",
                      fill="red")
        GAME_END = True


def update():
    global AIM, cnt
    c.delete(AIM)
    c.delete(cnt)
    cnt = c.create_text(WIDTH // 2, HEIGHT // 8,
                        text=counter,
                        font=("Purisa", 20),
                        fill="white")
    AIM = c.create_image(WIDTH // 2 - aim.size[0] // 2, HEIGHT // 2 - aim.size[1] // 2, anchor=NW, image=aim1)


def new_demon():
    ind = random.choice(free_zones)
    free_zones.pop(free_zones.index(ind))
    corx = (c.coords(separators[ind])[2] + c.coords(separators[ind + 1])[0]) // 2
    cory = HEIGHT // 2
    half_size = ENEMIE_START_SIZE // 2
    new_enem = c.create_image(corx - half_size, cory - half_size, anchor=NW, image=cacodemons[0])
    enemies.add(new_enem)
    enemies_ind_size[new_enem] = [ind, ENEMIE_START_SIZE]


def check_explosions():
    global explosions
    for i in range(len(explosions)):
        explosions[i][1] += 1
    expl_left = []
    for x in explosions:
        if x[1] > 5:
            c.delete(x[0])
        else:
            expl_left.append(x)
    explosions = expl_left


def main():
    global enemies, free_zones
    if not ON_PAUSE:
        check_explosions()
        if len(enemies) < 2:
            new_demon()
        new_enemies = set()
        del_enemies = set()
        for x in enemies:
            check(x)
            if GAME_END:
                enemies -= del_enemies
                enemies |= new_enemies
                update()
                return 0
            del_enemies.add(x)
            arr = c.coords(x)
            cacodem = cacodemons[enemies_ind_size[x][1] + ENEMIE_ADD * 2 - 2]
            # print(cacodem)
            c.delete(x)
            new_size = c.create_image(arr[0] - ENEMIE_ADD, arr[1] - ENEMIE_ADD, anchor=NW, image=cacodem)
            new_enemies.add(new_size)
            enemies_ind_size[new_size] = [enemies_ind_size[x][0], enemies_ind_size[x][1] + ENEMIE_ADD * 2]
            if new_size != x:
                del enemies_ind_size[x]
        enemies = new_enemies
        update()
    root.after(max(30 - counter, 8), main)


def movement_handler(event):
    global counter, ON_PAUSE
    char = event.keysym
    if ON_PAUSE:
        if char == "Escape":
            ON_PAUSE = False
        return 0
    if char == 'Right':
        if c.coords(separators[-1])[0] <= WIDTH // 10 * 7:
            return 0
        for i in range(len(separators)):
            c.move(separators[i], -LEN_MOVE, 0)
        for x in enemies:
            c.move(x, -LEN_MOVE, 0)
        for x in explosions:
            c.move(x, -LEN_MOVE, 0)
    elif char == "Left":
        if c.coords(separators[0])[0] >= WIDTH // 10 * 3:
            return 0
        for i in range(len(separators)):
            c.move(separators[i], LEN_MOVE, 0)
        for x in enemies:
            c.move(x, LEN_MOVE, 0)
        for x in explosions:
            c.move(x, LEN_MOVE, 0)
    elif char == 'space' and not GAME_END:
        for x in enemies:
            coors = c.coords(x)
            if coors[0] < WIDTH // 2 < coors[0] + enemies_ind_size[x][1]:
                explosions.append([c.create_image((coors[0] * 2 + enemies_ind_size[x][1]) // 2 - SIZE_EXPLOSION // 2,
                                                  HEIGHT // 2 - SIZE_EXPLOSION // 2,
                                                  anchor=NW, image=explosion_img), 0])
                free_zones.append(enemies_ind_size[x][0])
                del enemies_ind_size[x]
                c.delete(x)
                enemies.remove(x)
                counter += 1
                break
    elif char == "Escape":
        ON_PAUSE = True


def init():
    global separators, free_zones
    separators = [c.create_rectangle(WIDTH // 4 * i - W_SEP // 2, 0, WIDTH // 4 * i + W_SEP // 2, HEIGHT, fill='black')
                  for i in range(1, 4, 2)]
    sep_end = [c.create_rectangle(WIDTH // 4 * i - W_SEP // 2, 0, WIDTH // 4 * i + W_SEP // 2, HEIGHT, fill='red') for i
               in range(-1, 6, 6)]
    separators.insert(0, sep_end[0])
    separators.append(sep_end[-1])
    free_zones = [i for i in range(len(separators) - 1)]


WIDTH = 1800
HEIGHT = 900
W_SEP = 10
LEN_MOVE = 20
ENEMIE_START_SIZE = 2
ENEMIE_ADD = 1
GAME_END = False
ON_PAUSE = False
counter = 0
root = Tk()
root.title('Game')
c = Canvas(root, width=WIDTH, height=HEIGHT, bg='gray')
separators = []
enemies = set()
free_zones = []
enemies_ind_size = dict()
explosions = []

path = '/home/artemsh23/PycharmProjects/titled/'
img = io.imread(path + 'cacodemon/cacodem3.png')
img2 = io.imread(path + 'cacodemon/cacodem2.png')
cacodemons = []
SIZE_EXPLOSION = 500
for i in range(2, 940, 2):
    print(i)
    cacodemons.append(
        ImageTk.PhotoImage(Image.open(path + 'cacodemon/images/img' + str(i) + '.png')))
    cacodemons.append(0)
explosion_img = ImageTk.PhotoImage(
    Image.fromarray(imresize(io.imread(path + 'cacodemon/explosion.png'),
                             (SIZE_EXPLOSION, SIZE_EXPLOSION))))

colors = ['blue', 'green', 'purple', 'darkgreen', 'yellow', 'orange']
init()

cnt = c.create_text(WIDTH // 2, HEIGHT // 8,
                    text=counter,
                    font=("Purisa", 20),
                    fill="white")

aim = Image.open(path + "cacodemon/aim.png")
aim1 = ImageTk.PhotoImage(aim)
AIM = c.create_image(WIDTH // 2 - aim.size[0] // 2, HEIGHT // 2 - aim.size[1] // 2, anchor=NW, image=aim1)

c.grid()
c.focus_set()

if __name__ == "__main__":
    c.bind("<KeyPress>", movement_handler)
    main()
    root.mainloop()
