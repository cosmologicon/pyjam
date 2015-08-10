import pygame, random

freq = 22050

pygame.mixer.pre_init(freq, -16, 1, 1)

static = "".join([chr(random.randint(1, 255)) for _ in range(freq)] * 60)
def playstatic(t):
	nsamp = int(freq * 2 * t)
	sound = pygame.mixer.Sound(static[:nsamp])
	sound.set_volume(0.05)
	sound.play()
	return sound


