# Survival Turtle Game

A small arcade game made in Python for a school performance task. You control a turtle, catch orange circles to score points, and try not to get hit by the red enemies. The longer you last, the harder it gets.

It started as a simple "catch the circles" game and slowly grew into a survival game.

## About this project

This was a performance task in school, meant to practice Python programming. It uses the things we learned in class: variables, functions, if statements, loops, lists, dictionaries, keyboard events, random numbers, and saving a score to a file. The graphics all come from Python's built-in `turtle` module, so there is nothing extra to install.

## How to play

Press SPACE on the title screen and the game starts. You have 3 lives. Here is what you will see on the screen:

- **Orange circle:** catch it to get 1 point. It runs away when you get close, so try to trap it against a wall.
- **Red square:** bounces around the arena. If you touch one, you lose a life.
- **Red triangle:** this one chases you. It is slower than you, but it never stops, so keep moving.
- **Gold star:** shows up at random and disappears after a few seconds. Grab it for 5 points and one life back.

After you get hit, your turtle blinks for about a second, and you can't be hit again during that time.

Every 5 points you go up a level. Everything gets a bit faster and one more enemy joins, up to 8 enemies. There is no ending, so the goal is just to beat your best score. The game saves it for you.

## Controls

- Arrow keys or W, A, S, D to move (you can hold the key down)
- SPACE to start, or to play again after game over
- P to pause and resume
- R to restart

## How to run it

1. Install Python from python.org if you don't have it yet. On Windows, tick the box that says **Add python.exe to PATH** on the first screen of the installer. If you skip this, the `python` command won't work later.
2. Download this project, or clone it:

   ```bash
   git clone https://github.com/BuqueAndrewLopez/survival-turtle-game.git
   cd survival-turtle-game
   ```

3. Open a terminal in the project folder and run:

   ```bash
   python main.py
   ```

   On Windows, `py main.py` also works. If you use VS Code, you can open `main.py` and press the Run button at the top right instead.

4. The game opens in its own window. Press SPACE to start.

You don't need to install anything with pip. On some Linux computers, `turtle` needs Tkinter, which you can get with `sudo apt install python3-tk`.

## Files

- `main.py` is the whole game.
- `highscore.txt` is created automatically the first time you set a best score. It is ignored by git, so it will not be uploaded.

## How the code works

The game runs in a loop that repeats about 50 times a second. Each time around, it moves the player, the circle, the star and the enemies a little bit, checks if anything touched, and redraws the screen once.

A variable called `state` keeps track of whether you are on the title screen, playing, paused, or on the game over screen, and things only move while you are playing.

For the controls, pressing a key turns a True/False flag on and releasing it turns the flag off. The game checks those flags every frame. This makes the movement smooth, because normal key repeat has a small delay before it kicks in.

The squares bounce by flipping their direction when they hit a wall. The triangles use turtle's `towards()` and `forward()` to chase you, and the circle does the same thing in the opposite direction to run away. Two things count as touching when the distance between them is less than 20 pixels.

## Playing with the settings

If you want to change how the game feels, these are the easiest places to start in `main.py`:

- `PLAYER_SPEED` changes how fast you move.
- `target_speed()`, `square_speed()` and `hunter_speed()` change how fast the circle, squares and triangles go.
- `wanted = min(level + 1, 8)` in `add_enemies()` changes how many enemies you face.
- `invincible = 60` in `check_hits()` changes how long you are protected after a hit.
- `random.random() < 0.003` in `update_star()` changes how often the gold star shows up.

## Room for improvement

This is a school project, so I wrote the code to be simple and easy to read instead of perfectly organized. If I kept working on it, these are the things I would improve first.

**Use classes.** Right now the player, the circle, the squares, the triangles and the star are all separate turtle objects, and things like `dx` and `dy` are attached to them by hand. Functions like `move_enemies()` and `move_target()` have to reach into a lot of variables outside of them. A cleaner way is to give each kind of thing its own class, so it keeps its own data and knows how to move itself. Something like this:

```python
class Enemy(turtle.Turtle):
    def move(self, player):
        pass

class Square(Enemy):
    def move(self, player):
        pass

class Hunter(Enemy):
    def move(self, player):
        self.setheading(self.towards(player))
        self.forward(3)
```

The squares and triangles would share the same `Enemy` class and only differ in how they move. To add a new kind of enemy, you would add one new class instead of changing several functions.

**Put the game itself in a class.** The score, lives, level and state are global variables right now, so many functions need the `global` keyword. In a `Game` class they would become `self.score`, `self.lives` and so on, and the functions would become methods of that class. That gets rid of most of the globals and makes bugs easier to track down.

**Split the code into files.** Everything is in `main.py` at the moment. A better structure would be:

```
main.py        starts the game
game.py        the Game class and the game loop
entities.py    Player, Target, Square, Hunter and Star classes
settings.py    speeds, colors, sizes and other numbers
```

**Replace the eight key functions.** The `press_up`, `release_up`, `press_down` and the rest are repetitive. One function that takes the direction as an argument would do the same job with a lot less code.

**Name the numbers.** Numbers like `20`, `60` and `140` are spread through the code. Giving them names (for example `HIT_DISTANCE`) or moving them to a settings file would make the game easier to tweak.

**New features I would like to add:** sound effects, power-ups like a shield or slow motion, a difficulty menu, obstacles in the arena, and a top 5 high score list instead of just one best score.

## License

This project uses the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for the full text. You are free to use it, change it and improve it, as long as your version stays under the same license.

## Author

Made by Andrew Buque, Philippines.