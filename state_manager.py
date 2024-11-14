import pygame as py
from constants_config import *

class Game(object):
    #Single instance of this class is responsible for managing individual game states
    #Also implements system-wide behaviour i.e., login screen 
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

            #Manages event handling if idle screen is active
            if self.idle_screen:
                if event.type == py.QUIT:
                    self.done = True
                elif event.type == py.MOUSEBUTTONDOWN:
                    mouse_position = py.mouse.get_pos()
                    #Check if user has 
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
        #self.done controls swithcing screens
        self.state.done = False
        self.state_name = next_state
        self.state = self.states[self.state_name]
        self.state.startup(self.states[current_state].persist)

    def update(self, dt):
        self.idle_timer += (dt / 1000)
        #print(f"Idle Timer: {self.idle_timer:.2f} seconds")

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
        resume_rect_background = py.Rect(self.box_x_position, self.box_y_position, self.info_box_width, self.info_box_height)
        resume_rect_color = MEDIUM_GREEN 
        py.draw.rect(surface, resume_rect_color, resume_rect_background, border_radius=20)

        resume_button_text = self.font.render("Resume", True, WARM_SOFT_WHITE)
        resume_text_rect = resume_button_text.get_rect(center=resume_rect_background.center)
        surface.blit(resume_button_text, resume_text_rect)

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
        idle_notification_rect = py.Rect(self.box_x_position, self.box_y_position, self.info_box_width, self.info_box_height)
        idle_notification_color = MEDIUM_GREEN
        py.draw.rect(surface, idle_notification_color, idle_notification_rect, border_radius=10)

        idle_notification_text = self.font.render("Idle timeout in 5 seconds...", True, WARM_SOFT_WHITE)
        notification_text_rect = idle_notification_text.get_rect(center=idle_notification_rect.center)
        surface.blit(idle_notification_text, notification_text_rect)

class IncorrectPasswordNotification:
    def __init__(self, box_x_position=300, box_y_position=100, info_box_width=400, info_box_height=50):
        self.info_box_width = info_box_width
        self.info_box_height = info_box_height
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.font = py.font.SysFont('georgia', 24)

    def render(self, surface):
        incorrect_password_notification = py.Rect(self.box_x_position, self.box_y_position, self.info_box_width, self.info_box_height)
        incorrect_notification_color = PURE_WHITE
        py.draw.rect(surface, incorrect_notification_color, incorrect_password_notification, border_radius=10)

        incorrect_password_notification_text = self.font.render("Incorrect password. Try again.", True, PURE_BLACK)
        incorrect_notification_text_rect = incorrect_password_notification_text.get_rect(center=incorrect_password_notification.center)
        surface.blit(incorrect_password_notification_text, incorrect_notification_text_rect)

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
        password_background_rect = py.Rect(self.box_x_position - 50, self.box_y_position - 75, self.box_width + 100, self.box_height + 100)
        password_rect_color = MEDIUM_GREEN
        py.draw.rect(surface, password_rect_color, password_background_rect, border_radius=20)

        password_prompt_text = self.font.render("Enter password:", True, WARM_SOFT_WHITE)
        password_prompt_rect = password_prompt_text.get_rect(topleft=(password_background_rect.x + 30, password_background_rect.y + 10))
        surface.blit(password_prompt_text, password_prompt_rect)

        password_input_rect = py.Rect(self.box_x_position, self.box_y_position, self.box_width, self.box_height)
        password_input_color = WARM_SOFT_WHITE
        py.draw.rect(surface, password_input_color, password_input_rect, border_radius=10)

        password_input_text = self.font.render(self.user_input_text, True, PURE_BLACK)
        password_input_text_rect = password_input_text.get_rect(midleft=(password_input_rect.x + 10, password_input_rect.centery))
        surface.blit(password_input_text, password_input_text_rect)

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

