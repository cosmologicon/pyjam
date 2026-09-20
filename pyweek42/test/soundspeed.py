import pygame, numpy

FREQ0 = 22050
# Sound effect from https://opengameart.org/content/steampunk-fantasy-voices
fname = "Hero_Taunt_001.wav"


pygame.init()
pygame.display.set_mode((600, 400))


FREQ1 = int(FREQ0 / 2.5)
pygame.mixer.quit()
pygame.mixer.init(frequency=FREQ1, size=-16, channels=1, buffer=1)
sound1 = pygame.mixer.Sound(fname)
arr = pygame.sndarray.array(sound1)
print(arr)
print(arr.flags)
pygame.mixer.quit()

pygame.mixer.init(frequency=FREQ0, size=-16, channels=1, buffer=1)
sound = pygame.sndarray.make_sound(arr)


sound.play()

while not any(event.type in [pygame.KEYDOWN, pygame.QUIT] for event in pygame.event.get()):
	pass


