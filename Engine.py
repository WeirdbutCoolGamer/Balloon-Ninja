import pygame, sys
from Balloon import Balloon
from Button import Button
from Kitten import Kitten
from random import random
 
class Engine():
 
    def __init__(self):
        pass
 
    def release_batch(self, screen, settings, balloons, kittens):
        for x in range(0, settings.batch_size):
            self.spawn_balloon(screen, settings, balloons, kittens)
 
    def check_balloons(self, balloons, kittens, sword, scoreboard, screen, settings, time_passed):
        # Find any balloons that have been popped,
        #  or have disappeared off the top of the screen
        for balloon in balloons:
            balloon.update(time_passed)
 
            if balloon.rect.colliderect(sword.rect):
                self.pop_balloon(scoreboard, settings, balloon, balloons)
                continue
 
            if balloon.y_position < -balloon.image_h/2 + settings.scoreboard_height:
                self.miss_balloon(scoreboard, balloon, balloons)
                self.spawn_balloon(screen, settings, balloons, kittens)
                continue
 
            balloon.blitme()
 
        if scoreboard.balloons_popped > 0 or scoreboard.balloons_missed > 0:
            scoreboard.popped_ratio = float(scoreboard.balloons_popped)/(scoreboard.balloons_popped + scoreboard.balloons_missed)
            if scoreboard.popped_ratio < settings.min_popped_ratio:
                # Set game_active to false, empty the list of balloons, and increment games_played
                settings.game_active = False
                settings.games_played += 1
 
    def check_kittens(self, kittens, sword, scoreboard, screen, settings, time_passed):
        # Find any kittens that have been killed, or have survived to top of screen
        for kitten in kittens:
            kitten.update(time_passed)
 
            if kitten.rect.colliderect(sword.rect):
                self.kill_kitten(scoreboard, settings, kitten, kittens)
                continue
 
            if kitten.y_position < -kitten.image_h/2 + settings.scoreboard_height:
                self.spare_kitten(scoreboard, settings, kitten, kittens)
                continue
 
            kitten.blitme()
 
    def update_sword(self, sword, mouse_x, mouse_y, settings):
        # Update the sword's position, and draw the sword on the screen
        sword.x_position = mouse_x
        if sword.grabbed:
            sword.y_position = mouse_y
        else:
            sword.y_position = sword.image_h/2 + settings.scoreboard_height
        sword.update_rect()
        sword.blitme()
 
    def miss_balloon(self, scoreboard, balloon, balloons):
        scoreboard.balloons_missed += 1
        balloons.remove(balloon)
 
    def spare_kitten(self, scoreboard, settings, kitten, kittens):
        scoreboard.kittens_spared += 1
        scoreboard.score += settings.kitten_score_factor * settings.points_per_balloon
        kittens.remove(kitten)
 
    def pop_balloon(self, scoreboard, settings, balloon, balloons):
        scoreboard.balloons_popped += 1
        scoreboard.score += settings.points_per_balloon
        balloons.remove(balloon)
 
    def kill_kitten(self, scoreboard, settings, kitten, kittens):
        scoreboard.kittens_killed += 1
        scoreboard.score -= settings.kitten_score_factor * settings.points_per_balloon
        kittens.remove(kitten)
 
    def spawn_balloon(self, screen, settings, balloons, kittens):
        balloons.append(Balloon(screen, settings))
        # Periodically release a kitten:
        if random() < settings.kitten_ratio:
            self.spawn_kitten(screen, settings, kittens)
 
    def spawn_kitten(self, screen, settings, kittens):
        kittens.append(Kitten(screen, settings))
 
    def check_events(self, settings, scoreboard, sword, play_button, mouse_x, mouse_y, balloons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sword.rect.collidepoint(mouse_x, mouse_y):
                    sword.grabbed = True
                if play_button.rect.collidepoint(mouse_x, mouse_y):
                    # Play button has been pressed.  Empty list of balloons,
                    #  initialize scoreboard and game parameters, and make game active.
                    del balloons[:]
                    scoreboard.initialize_stats()
                    settings.initialize_game_parameters()
                    settings.game_active = True
            if event.type == pygame.MOUSEBUTTONUP:
                sword.grabbed = False