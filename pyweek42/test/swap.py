import pygame

FREQ0 = 22050
# Sound effect from https://opengameart.org/content/steampunk-fantasy-voices
sfxname = "Hero_Taunt_001.wav"
# Music from https://opengameart.org/content/zombies-march
musicname = "ZombiesAreComing.wav"


pygame.mixer.pre_init(frequency=FREQ0, size=-16, channels=1, buffer=1)
pygame.init()
pygame.display.set_mode((600, 400))
sound0 = pygame.mixer.Sound(sfxname)
sound1 = pygame.mixer.Sound(musicname)

channel = pygame.mixer.Channel(1)
channel.play(sound0)
print(channel.get_queue())
channel.queue(sound0)
print(channel.get_queue())
channel.queue(sound1)
print(channel.get_queue())


t0 = pygame.time.get_ticks()
playing = True
while playing:
	dfactor = 0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			playing = False
	pygame.display.flip()


