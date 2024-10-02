# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 1280))
clock = pygame.time.Clock()
running = True
dt = 0

# inital location + size
rectX = 100
rectY = 100
rectSizeX = 500
rectSizeY = 200

# text boxes
base_font = pygame.font.Font(None, 32)
activeColor = pygame.Color((20, 40, 125))
inactiveColor = pygame.Color((20, 40, 75))

class TextBox:

    def __init__(self, x, y, w, h, direction, text=""):
        # Rect must be capitalized here
        self.rect = pygame.Rect(x, y, w, h)
        self.color = inactiveColor
        self.text = text
        self.textSurface = base_font.render(text, True, (255, 255, 255))
        self.active = False
        self.direction = direction
    
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = activeColor
            else:
                self.active = False
                self.color = inactiveColor
        if event.type == pygame.KEYDOWN:
            if self.active == True:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN: #enter
                    if self.text.isdigit():
                        sizeInt = int(self.text)
                        if sizeInt > 1081:
                            sizeInt = 1080
                            self.text = "1080"
                        self.direction = sizeInt
                        print(self.direction)
                    else:
                        print("Invalid integer!")

                else:
                    self.text += event.unicode
                self.textSurface = base_font.render(self.text, True, (255, 255, 255))

    def update(self):
        width = max(140, self.textSurface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.textSurface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

textbox1 = TextBox(50, 50, 140, 32, rectSizeX)
textbox2 = TextBox(240, 50, 140, 32, rectSizeY)
textboxes = [textbox1, textbox2]

active = False

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in textboxes:
            box.handleEvent(event)
            box.update()

    screen.fill((0,0,0))

    for box in textboxes:
        box.draw(screen)
    pygame.draw.rect(screen, (255, 255, 255), [rectX, rectY, textbox1.direction, textbox2.direction], 2)
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    clock.tick(60)

pygame.quit()