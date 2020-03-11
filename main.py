

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



class Game:
	def __init__(self):
		self.playing = True
		self.is_dead = False
		self.FPS = 15
		self.clock = pygame.time.Clock()
		self.window_width = 50 * 25
		self.window_height = 50 * 15
		self.window = pygame.display.set_mode((self.window_width, self.window_height))


		self.space = [(i * 50, j * 50) for i in range(self.window_width // 50) for j in range(self.window_height // 50)]
		self.snake = game_objects.Snake(self.window_width, self.window_height, self.space)
		self.food = game_objects.Food(self.space)

	def run(self):
		while self.playing:
			self.pressed = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
					self.playing = False
			self.window.fill((30, 39, 46))
			if self.is_dead:
				pass
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
		for i in range(len(self.snake.rects)):
			for j in range(i + 1, len(self.snake.rects)):
				if self.snake.rects[i].colliderect(self.snake.rects[j]):
					self.is_dead = True
					self.playing = False

	def check_food_collision(self):
		if self.snake.rects[0].colliderect(self.food.rect):
			self.snake.sprites.append(pygame.Surface((self.snake.sprite_width, self.snake.sprite_height)))
			self.snake.rects.append(self.snake.sprites[-1].get_rect())
			self.snake.rects[-1].topleft = self.snake.rects[-2].topleft
			self.snake.sprites[-1].fill(self.snake.color)
			self.food.appear(self.space)

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
