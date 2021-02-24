import pygame


class Window:
    def __init__(self, width, height, objects):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.clock = pygame.time.Clock()
        self.objects = objects
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def update(self):
        for obj in self.objects:
            obj.update(self)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for obj in self.objects:
            obj.draw(self)
        pygame.display.flip()