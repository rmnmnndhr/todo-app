import pygame
import json
from settings import *


# render text --
def text(message, screen, color, size, x, y, center = None):
	font = pygame.font.SysFont("Lucida Console", size)
	text = font.render(message, True, color)
	if center:
		screen.blit(text,( x - text.get_width() // 2, y - text.get_height() // 2))
	else:
		screen.blit(text, (x, y))

	return text.get_width(), text.get_height()


def load():
    try:
        with open('data.json') as f:
            return json.load(f)
    except:
        data = []
        with open('data.json', 'w') as f:
            json.dump(data, f)

        with open('data.json') as f:
            return json.load(f)


def save(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)
