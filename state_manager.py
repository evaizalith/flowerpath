import pygame as py
from constants_config import *

class Game(object):
    # Single instance of this class is responsible for managing the individual game state

    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = py.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

        self.idle_screen = False
        self.idle_timer = 0
        self.idle_notification_shown = False

        self.password_box_shown = False
        self.incorrect_password_notification_box_shown = False

        self.resume_button = ResumeButton(box_x_position=300, box_y_position=550)
        self.idle_notification = IdleNotification(box_x_position=300, box_y_position=550)
        self.incorrect_password_notification_box = IncorrectPasswordNotification(box_x_position=300, box_y_position=400)
        self.password_input_text = PasswordInput(box_x_position=300, box_y_position=300, box_width=400, box_height=50)

    def event_loop(self):
        for event in py.event.get():
            #if statement handles idle screen and password handling
            if self.idle_screen:
                if event.type == py.QUIT:
                    self.done = True
                elif event.type == py.MOUSEBUTTONDOWN:
                    mouse_position = py.mouse.get_pos()
                    if self.password_input_text.check_click(mouse_position):
                        self.password_box_shown = True
                    else:
                        self.password_box_shown = False
                    if self.resume_button.check_resume_button_click(mouse_position):
                        if self.password_input_text.verify_password():
                            self.idle_screen = False
                            self.idle_notification_shown = False
                            self.idle_timer = 0
                            self.password_input_text.clear()
                            self.incorrect_password_notification_box_shown = False
                        else:
                            self.incorrect_password_notification_box_shown = True
                elif event.type == py.KEYDOWN and self.password_box_shown:
                    self.password_input_text.handle_event(event)
            else:
                if event.type in (py.MOUSEMOTION, py.MOUSEBUTTONDOWN, py.KEYDOWN):
                    self.idle_timer = 0
                    self.idle_notification_shown = False

                self.state.get_event(event)

    def flip_state(self):
        # Actually switches to the next game state and passes persistent data to the new state
        current_state = self.state_name
        next_state = self.state.next_state
        # Marks the screen as NOT done before transitioning, so a return to that screen will not cause immediate exit
        self.state.done = False
        self.state_name = next_state
        self.state = self.states[self.state_name]
        self.state.startup(self.states[current_state].persist)

    def update(self, dt):
        # Increment the idle timer by the elapsed time (dt)
        self.idle_timer += (dt / 1000)
        print(f"Idle Timer: {self.idle_timer:.2f} seconds")

        if self.idle_timer > TIME_TO_IDLE_WARNING:
            self.idle_notification_shown = True

        if self.idle_timer > TIME_TO_TIMEOUT:
            self.idle_screen = True
            self.idle_notification_shown = False

        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

        if self.idle_notification_shown:
            self.idle_notification.render(self.screen)

        if self.idle_screen:
            idle_screen_color = LIGHT_BLUE
            idle_screen_rect = self.screen.get_rect()
            py.draw.rect(self.screen, idle_screen_color, idle_screen_rect)

            self.resume_button.render(self.screen)
            self.password_input_text.render(self.screen)

        if self.incorrect_password_notification_box_shown:
            self.incorrect_password_notification_box.render(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            py.display.update()

class ResumeButton:
    def __init__(self, box_x_position=152, box_y_position=1000, info_box_width=400, info_box_height=67):
        self.info_box_width = info_box_width
        self.info_box_height = info_box_height
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.font = py.font.SysFont('georgia', 36)

    def render(self, surface):
        button_rect = py.Rect(self.box_x_position, self.box_y_position, self.info_box_width, self.info_box_height)
        button_color = MEDIUM_GREEN 
        py.draw.rect(surface, button_color, button_rect, border_radius=20)

        button_text = self.font.render("Resume", True, WARM_SOFT_WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        surface.blit(button_text, button_text_rect)

    def check_resume_button_click(self, mouse_position):
        x, y = mouse_position
        return (self.box_x_position <= x <= self.box_x_position + self.info_box_width) and (self.box_y_position <= y <= self.   box_y_position + self.info_box_height)

class IdleNotification:
    def __init__(self, box_x_position=300, box_y_position=100, info_box_width=400, info_box_height=50):
        self.info_box_width = info_box_width
        self.info_box_height = info_box_height
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.font = py.font.SysFont('georgia', 24)

    def render(self, surface):
        notification_rect = py.Rect(self.box_x_position, self.box_y_position, self.info_box_width, self.info_box_height)
        notification_color = MEDIUM_GREEN
        py.draw.rect(surface, notification_color, notification_rect, border_radius=10)

        notification_text = self.font.render("Idle timeout in 5 seconds...", True, WARM_SOFT_WHITE)
        notification_text_rect = notification_text.get_rect(center=notification_rect.center)
        surface.blit(notification_text, notification_text_rect)

class IncorrectPasswordNotification:
    def __init__(self, box_x_position=300, box_y_position=100, info_box_width=400, info_box_height=50):
        self.info_box_width = info_box_width
        self.info_box_height = info_box_height
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.font = py.font.SysFont('georgia', 24)

    def render(self, surface):
        notification_rect = py.Rect(self.box_x_position, self.box_y_position, self.info_box_width, self.info_box_height)
        notification_color = PURE_WHITE
        py.draw.rect(surface, notification_color, notification_rect, border_radius=10)

        notification_text = self.font.render("Incorrect password. Try again.", True, PURE_BLACK)
        notification_text_rect = notification_text.get_rect(center=notification_rect.center)
        surface.blit(notification_text, notification_text_rect)

class PasswordInput:
    def __init__(self, box_x_position, box_y_position, box_width, box_height, correct_password="1234"):
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.box_width = box_width
        self.box_height = box_height
        self.correct_password = correct_password
        self.user_input_text = "" 
        self.font = py.font.SysFont('georgia', 36)

    def render(self, surface):
        background_rect = py.Rect(self.box_x_position - 50, self.box_y_position - 75, self.box_width + 100, self.box_height + 100)
        background_rect_color = MEDIUM_GREEN
        py.draw.rect(surface, background_rect_color, background_rect, border_radius=20)

        background_rect_text = self.font.render("Enter password:", True, WARM_SOFT_WHITE)
        background_rect_rect = background_rect_text.get_rect(topleft=(background_rect.x + 30, background_rect.y + 10))
        surface.blit(background_rect_text, background_rect_rect)

        input_rect = py.Rect(self.box_x_position, self.box_y_position, self.box_width, self.box_height)
        input_color = WARM_SOFT_WHITE
        py.draw.rect(surface, input_color, input_rect, border_radius=10)

        input_text = self.font.render(self.user_input_text, True, PURE_BLACK)
        input_text_rect = input_text.get_rect(midleft=(input_rect.x + 10, input_rect.centery))
        surface.blit(input_text, input_text_rect)

    def check_click(self, mouse_position):
        x, y = mouse_position
        return (self.box_x_position <= x <= self.box_x_position + self.box_width) and (self.box_y_position <= y <= self.box_y_position + self.box_height)

    def handle_event(self, event):
        if event.key == py.K_BACKSPACE:
            self.user_input_text = self.user_input_text[:-1]
        elif event.key == py.K_RETURN:
            pass
        else:
            self.user_input_text += event.unicode

    def verify_password(self):
        if self.user_input_text == self.correct_password:
            return True
        else:
            return False
            
    def clear(self):
        self.user_input_text = ""

