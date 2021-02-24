import random

from window import Window
from boid import Boid, Obstacle


width = 500
height = 500

objects = []
for _ in range(50):
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    objects.append(Boid(x, y, (255, 255, 255), 5))

objects.append(Obstacle(250, 250))

window = Window(width, height, objects)
window.run()