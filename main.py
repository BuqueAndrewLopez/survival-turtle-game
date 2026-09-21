import turtle
import random
import math
import os

LEFT = -280
RIGHT = 280
BOTTOM = -280
TOP = 230
PLAYER_SPEED = 6

score_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")

screen = turtle.Screen()
screen.title("Survival Turtle Game")
screen.bgcolor("lightblue")
screen.setup(width=600, height=600)
screen.tracer(0)

star_points = []
for i in range(10):
    if i % 2 == 0:
        radius = 13
    else:
        radius = 5.5
    angle = math.radians(90 + i * 36)
    star_points.append((radius * math.cos(angle), radius * math.sin(angle)))
screen.register_shape("star", tuple(star_points))


def make_turtle(shape, color):
    t = turtle.Turtle()
    t.shape(shape)
    t.color(color)
    t.penup()
    t.hideturtle()
    return t


def make_writer():
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    return t


border = make_writer()
border.pensize(3)
border.color("navy")
border.goto(LEFT - 15, BOTTOM - 15)
border.pendown()
border.goto(RIGHT + 15, BOTTOM - 15)
border.goto(RIGHT + 15, TOP + 15)
border.goto(LEFT - 15, TOP + 15)
border.goto(LEFT - 15, BOTTOM - 15)

hud = make_writer()
writer = make_writer()

player = make_turtle("turtle", "green")
target = make_turtle("circle", "orange")
star_item = make_turtle("star", "gold")

enemies = []
for i in range(8):
    if i % 3 == 2:
        enemy = make_turtle("triangle", "red")
    else:
        enemy = make_turtle("square", "red")
    enemy.dx = 1
    enemy.dy = 1
    enemies.append(enemy)

icons = [
    make_turtle("circle", "orange"),
    make_turtle("square", "red"),
    make_turtle("triangle", "red"),
    make_turtle("star", "gold"),
]
icons[2].setheading(90)

state = "title"
score = 0
lives = 3
level = 1
invincible = 0
star_timer = 0
enemy_count = 0
keys = {"up": False, "down": False, "left": False, "right": False}


def load_best():
    try:
        with open(score_file) as f:
            return int(f.read())
    except (OSError, ValueError):
        return 0


def save_best():
    try:
        with open(score_file, "w") as f:
            f.write(str(best))
    except OSError:
        pass


best = load_best()


def target_speed():
    return min(3 + level * 0.35, 5.2)


def square_speed():
    return min(1.8 + level * 0.25, 4)


def hunter_speed():
    return min(1.8 + level * 0.2, 3.6)


def random_spot(distance=150):
    while True:
        x = random.randint(LEFT + 10, RIGHT - 10)
        y = random.randint(BOTTOM + 10, TOP - 10)
        if player.distance(x, y) >= distance:
            return x, y


def write_text(text, x, y, size, style, color, align):
    writer.color(color)
    writer.goto(x, y)
    writer.write(text, align=align, font=("Arial", size, style))


def show_message(title, lines, color):
    writer.clear()
    write_text(title, 0, 40, 32, "bold", color, "center")
    y = 0
    for line in lines:
        write_text(line, 0, y, 14, "normal", color, "center")
        y -= 26


def clear_message():
    if state == "playing":
        writer.clear()


def draw_hud():
    hud.clear()
    hud.color("black")
    hud.goto(-290, 255)
    hud.write("Score: " + str(score) + "   Level: " + str(level) + "   Lives: " + str(lives),
              font=("Arial", 15, "bold"))
    hud.goto(290, 255)
    hud.write("Best: " + str(max(best, score)), align="right", font=("Arial", 15, "bold"))


def hide_all():
    player.hideturtle()
    target.hideturtle()
    star_item.hideturtle()
    for e in enemies:
        e.hideturtle()


def show_all():
    player.showturtle()
    target.showturtle()
    if star_timer > 0:
        star_item.showturtle()
    for i in range(enemy_count):
        enemies[i].showturtle()


def show_title():
    writer.clear()
    write_text("Survival Turtle Game", 0, 145, 34, "bold", "darkgreen", "center")
    lines = [
        "Catch orange circles for +1 point (they run away!)",
        "Dodge red squares - each hit costs a life",
        "Red triangles hunt you, so keep moving!",
        "Grab the gold star for +5 points and a life",
    ]
    y = 85
    for i in range(4):
        icons[i].goto(-255, y + 8)
        icons[i].showturtle()
        write_text(lines[i], -225, y, 13, "normal", "black", "left")
        y -= 38
    write_text("Every 5 points is a new level: faster, and one more enemy joins",
               0, -72, 12, "normal", "navy", "center")
    write_text("Move:  Arrow keys or WASD", 0, -110, 14, "bold", "black", "center")
    write_text("P = pause        R = restart", 0, -135, 13, "normal", "black", "center")
    write_text("Press SPACE to start", 0, -190, 22, "bold", "darkgreen", "center")


def add_enemies():
    global enemy_count
    wanted = min(level + 1, 8)
    while enemy_count < wanted:
        e = enemies[enemy_count]
        e.goto(random_spot())
        e.dx = random.choice([-1, 1])
        e.dy = random.choice([-1, 1])
        e.showturtle()
        enemy_count += 1


def add_points(amount):
    global score, level
    score += amount
    if score // 5 + 1 > level:
        level = score // 5 + 1
        add_enemies()
        show_message("Level " + str(level) + "!", [], "darkgreen")
        screen.ontimer(clear_message, 1000)
    draw_hud()


def game_over():
    global state, best
    state = "over"
    hide_all()
    result = "Score: " + str(score)
    if score > best:
        best = score
        save_best()
        result = result + "  -  NEW BEST!"
    draw_hud()
    show_message("Game Over", [result, "Press SPACE to play again"], "darkred")


def reset_background():
    screen.bgcolor("lightblue")


def move_player():
    dx = 0
    dy = 0
    if keys["left"]:
        dx -= 1
    if keys["right"]:
        dx += 1
    if keys["up"]:
        dy += 1
    if keys["down"]:
        dy -= 1
    if dx == 0 and dy == 0:
        return
    length = math.sqrt(dx * dx + dy * dy)
    x = player.xcor() + dx / length * PLAYER_SPEED
    y = player.ycor() + dy / length * PLAYER_SPEED
    player.setheading(math.degrees(math.atan2(dy, dx)))
    player.goto(max(LEFT, min(RIGHT, x)), max(BOTTOM, min(TOP, y)))


def blink_player():
    global invincible
    if invincible > 0:
        invincible -= 1
        if invincible % 10 < 5:
            player.hideturtle()
        else:
            player.showturtle()
        if invincible == 0:
            player.showturtle()


def move_target():
    if player.distance(target) < 140:
        target.setheading(target.towards(player) + 180)
    elif random.randint(1, 60) == 1:
        target.setheading(random.randint(0, 360))
    target.forward(target_speed())
    x = target.xcor()
    y = target.ycor()
    if x > RIGHT or x < LEFT:
        target.setheading(180 - target.heading())
    if y > TOP or y < BOTTOM:
        target.setheading(-target.heading())
    target.goto(max(LEFT, min(RIGHT, x)), max(BOTTOM, min(TOP, y)))
    if player.distance(target) < 20:
        target.goto(random_spot())
        target.setheading(random.randint(0, 360))
        add_points(1)


def update_star():
    global star_timer, lives
    if star_timer == 0:
        if random.random() < 0.003:
            star_item.goto(random_spot(100))
            star_item.showturtle()
            star_timer = 200
        return
    star_timer -= 1
    if star_timer == 0:
        star_item.hideturtle()
    elif player.distance(star_item) < 20:
        star_timer = 0
        star_item.hideturtle()
        if lives < 3:
            lives += 1
        add_points(5)
    elif star_timer < 60:
        if star_timer % 12 < 6:
            star_item.hideturtle()
        else:
            star_item.showturtle()


def move_enemies():
    for i in range(enemy_count):
        e = enemies[i]
        if i % 3 == 2:
            e.setheading(e.towards(player))
            e.forward(hunter_speed())
        else:
            e.setx(e.xcor() + e.dx * square_speed())
            e.sety(e.ycor() + e.dy * square_speed())
            if e.xcor() > RIGHT or e.xcor() < LEFT:
                e.dx = -e.dx
            if e.ycor() > TOP or e.ycor() < BOTTOM:
                e.dy = -e.dy


def check_hits():
    global lives, invincible
    if invincible > 0:
        return
    for i in range(enemy_count):
        if player.distance(enemies[i]) < 20:
            lives -= 1
            invincible = 60
            screen.bgcolor("#ffc9c9")
            screen.ontimer(reset_background, 120)
            draw_hud()
            if lives <= 0:
                game_over()
            return


def start_game():
    global state, score, lives, level, invincible, star_timer, enemy_count
    score = 0
    lives = 3
    level = 1
    invincible = 0
    star_timer = 0
    enemy_count = 0
    for k in keys:
        keys[k] = False
    hide_all()
    for icon in icons:
        icon.hideturtle()
    writer.clear()
    player.goto(0, -25)
    player.setheading(0)
    player.showturtle()
    target.goto(random_spot())
    target.setheading(random.randint(0, 360))
    target.showturtle()
    add_enemies()
    draw_hud()
    state = "playing"


def space_pressed():
    if state == "title" or state == "over":
        start_game()


def pause_pressed():
    global state
    if state == "playing":
        state = "paused"
        for k in keys:
            keys[k] = False
        hide_all()
        show_message("Paused", ["Press P to resume"], "navy")
    elif state == "paused":
        state = "playing"
        writer.clear()
        show_all()


def press_up():
    keys["up"] = True


def release_up():
    keys["up"] = False


def press_down():
    keys["down"] = True


def release_down():
    keys["down"] = False


def press_left():
    keys["left"] = True


def release_left():
    keys["left"] = False


def press_right():
    keys["right"] = True


def release_right():
    keys["right"] = False


for key in ["Up", "w", "W"]:
    screen.onkeypress(press_up, key)
    screen.onkeyrelease(release_up, key)
for key in ["Down", "s", "S"]:
    screen.onkeypress(press_down, key)
    screen.onkeyrelease(release_down, key)
for key in ["Left", "a", "A"]:
    screen.onkeypress(press_left, key)
    screen.onkeyrelease(release_left, key)
for key in ["Right", "d", "D"]:
    screen.onkeypress(press_right, key)
    screen.onkeyrelease(release_right, key)
for key in ["r", "R"]:
    screen.onkeypress(start_game, key)
for key in ["p", "P"]:
    screen.onkeypress(pause_pressed, key)
screen.onkeypress(space_pressed, "space")


def game_loop():
    if state == "playing":
        move_player()
        blink_player()
        move_target()
        update_star()
        move_enemies()
        check_hits()
    screen.update()
    screen.ontimer(game_loop, 20)


screen.listen()
draw_hud()
show_title()
game_loop()
screen.mainloop()