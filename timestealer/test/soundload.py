import pygame, numpy

# Ogg doesn't work below 32k. WAV works for any frequency.

FREQ0 = 20000
# Music from https://opengameart.org/content/zombies-march
musicname = "ZombiesAreComing.wav"

pygame.init()
pygame.display.set_mode((600, 400))
pygame.mixer.quit()
pygame.mixer.init(frequency=FREQ0, size=-16, channels=1, buffer=1)
sound1 = pygame.mixer.Sound(musicname)
arr = pygame.sndarray.array(sound1)
print(arr.shape)
sound1.play()
while not any(event.type in [pygame.QUIT, pygame.KEYDOWN] for event in pygame.event.get()):
	pass

