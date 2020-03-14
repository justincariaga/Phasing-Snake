

import pygame
import sys 
import random
import time
import math
import json
import os

import game_objects
import resources

from pygame.locals import *


pygame.init()
pygame.mixer.init()

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)

class Game:
	def __init__(self):
		self.playing = True
		self.is_dead = True
		self.FPS = 15
		self.clock = pygame.time.Clock()
		self.window_width = 50 * 25
		self.window_height = 50 * 15
		self.window = pygame.display.set_mode((self.window_width, self.window_height))
		# self.cover_art = pygame.image.load("cover_art.jpg")
		self.cover_art = pygame.image.load(find_data_file("cover_art.jpg"))

		pygame.display.set_caption("Phasing Snake")


		self.space = [(i * 50, j * 50) for i in range(self.window_width // 50) for j in range(self.window_height // 50)]
		self.snake = game_objects.Snake(self.window_width, self.window_height, self.space)
		self.food = game_objects.Food(self.space)

		# labels
		self.font_color = (255, 255, 255)
		self.font_obj = pygame.font.SysFont("Terminal", 50, bold=True)
		self.score = 0
		self.texts = {
			"title": self.font_obj.render("Phasing Snake", True, self.font_color),
			"enter": self.font_obj.render("Press Enter To Play!", True, self.font_color),
			"score": self.font_obj.render("Score: {}".format(self.score), True, self.font_color),
		}
		self.text_rects = {
			"title": self.texts["title"].get_rect(),
			"enter": self.texts["enter"].get_rect(),
			"score": self.texts["score"].get_rect(),
		}
		self.text_rects["title"].center = (self.window_width // 2, self.window_height // 2 - 200)
		self.text_rects["enter"].center = (self.window_width // 2, self.window_height // 2 + 100)
		self.text_rects["score"].center = (self.window_width // 2, self.window_height // 2 + 200)

	def run(self):
		while self.playing:
			self.pressed = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
					self.playing = False
				if event.type == pygame.KEYDOWN and self.is_dead and event.key == pygame.K_RETURN:
					self.is_dead = False
					self.score = 0
					self.text_rects["score"].bottomleft = (0, self.window_height)
			self.window.fill((30, 39, 46))
			self.texts["score"] =  self.font_obj.render("Score: {}".format(self.score), True, self.font_color)
			self.window.blit(self.texts["score"], self.text_rects["score"])
			if self.is_dead:
				self.window.blit(self.cover_art, (0, 0))
				self.window.blit(self.texts["score"], self.text_rects["score"])


			else:
				self.handle_input()
				self.check_snake_collision()
				self.check_food_collision()

				for sprite in range(len(self.snake.sprites)):
					self.window.blit(self.snake.sprites[sprite], self.snake.rects[sprite])
				self.window.blit(self.food.surface, self.food.rect)
			pygame.display.update()
			self.clock.tick(self.FPS)


	def check_snake_collision(self):
		for j in range(1, len(self.snake.rects)):
			if self.snake.rects[0].colliderect(self.snake.rects[j]):
				self.is_dead = True
				self.text_rects["score"].center = (self.window_width // 2, self.window_height // 2 + 200)
				self.space = [(i * 50, j * 50) for i in range(self.window_width // 50) for j in range(self.window_height // 50)]
				self.snake.reset(self.window_width, self.window_height, self.space)
				break


	def check_food_collision(self):
		if self.snake.rects[0].colliderect(self.food.rect):
			self.snake.sprites.append(pygame.Surface((self.snake.sprite_width, self.snake.sprite_height)))
			self.snake.rects.append(self.snake.sprites[-1].get_rect())
			self.snake.rects[-1].topleft = self.snake.rects[-2].topleft
			self.snake.sprites[-1].fill(self.snake.color)
			self.food.appear(self.space)
			self.score += 1

	def handle_input(self):
		if self.pressed[K_LEFT] and self.snake.dx != 1:
			self.snake.dx = -1
			self.snake.dy = 0
		if self.pressed[K_RIGHT] and self.snake.dx != -1:
			self.snake.dx = 1
			self.snake.dy = 0
		if self.pressed[K_UP] and self.snake.dy != 1:
			self.snake.dy = -1
			self.snake.dx = 0
		if self.pressed[K_DOWN] and self.snake.dy != -1:
			self.snake.dy = 1
			self.snake.dx = 0
		self.snake.update(self.window_width, self.window_height, self.space)

if __name__ == "__main__":
	game = Game()
	game.run()
