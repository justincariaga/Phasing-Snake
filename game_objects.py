import pygame
import random

class Snake:
	def __init__(self, window_width, window_height, space):
		self.sprite_width = 50
		self.sprite_height = 50
		self.color = (255, 0, 0, 128)

		self.sprites = [pygame.Surface((self.sprite_width, self.sprite_height), 
			pygame.SRCALPHA, 32).convert_alpha() for i in range(3)]

		self.rects = [sprite.get_rect() for sprite in self.sprites]
		for i in range(len(self.rects)):
			self.sprites[i].fill(self.color)
			space.remove((window_width // 2 - self.sprite_width // 2, window_height // 2 + self.sprite_height * i - self.sprite_height // 2))
			self.rects[i].center = (window_width // 2, window_height // 2 + self.sprite_height * i)

		self.dx = 0
		self.dy = -1
		self.speed = 50

	def update(self, window_width, window_height, space):
		space.append(self.rects[-1].topleft)
		for i in range(-1, -len(self.sprites), -1):
			self.rects[i].center = self.rects[i - 1].center
	
		self.rects[0].left += self.dx * self.speed
		self.rects[0].top += self.dy * self.speed
		if self.rects[0].left >= window_width:
			self.rects[0].left = 0
		if self.rects[0].right <= 0:
			self.rects[0].right = window_width
		if self.rects[0].top >= window_height:
			self.rects[0].top = 0
		if self.rects[0].bottom <= 0:
			self.rects[0].bottom = window_height
		space.remove(self.rects[0].topleft)


class Food:
	def __init__(self, space):
		self.sprite_width = 50
		self.sprite_height = 50
		self.color = (0, 255, 0, 128)
		self.surface = pygame.Surface((self.sprite_width, self.sprite_height), 
			pygame.SRCALPHA, 32).convert_alpha()
		self.rect = self.surface.get_rect()
		self.surface.fill(self.color)
		self.appear(space)


	def appear(self, space):
		self.rect.topleft = random.choice(space)



