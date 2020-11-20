#Initializes Modules
import pygame as pg
import random 
import os
import sys
#Initialized Pygame And Display
pg.init()
display = pg.display.set_mode((500, 500))
pg.display.set_caption("Flappy Bird")
pg.display.update()
#Initializes Variables
running = True
dead = False
playAgain = False
birdPos = [225, 250]
pipePos = [[500, random.randrange(-200, 0, 20)]]
pipeGap = 0
groundPos = [0, 500]
backgroundPos = [0, 500]
ySpeed = 0
movement = 2.5
points = 0
grav = .25
white = (255, 255, 255)
black = (0, 0, 0)
clock = pg.time.Clock()
#Initializes Assets
birdPic = pg.transform.scale(pg.image.load("Assets/bird.png"), (50, 40))
upPipePic = pg.transform.scale(pg.image.load("Assets/upPipe.png"), (50, 300))
downPipePic = pg.transform.scale(pg.image.load("Assets/downPipe.png"), (50, 300))
ground = pg.transform.scale(pg.image.load("Assets/ground.png"), (500, 50))
background = pg.transform.scale(pg.image.load("Assets/background.png"), (500, 450))
inFont = pg.font.Font("Assets/TextFont/8-bit Arcade In.ttf", 80)
outFont = pg.font.Font("Assets/TextFont/8-bit Arcade Out.ttf", 80)
#Initializes Sprite Class
class Bird (pg.sprite.Sprite):
	def __init__(self, picture):
		super().__init__()
		self.rotation = 0
		self.picture = picture
		self.image = picture
		self.rect = self.image.get_rect()
		self.mask = pg.mask.from_surface(self.image)
	def update(self):
		if ySpeed < 0:
			self.rotation = 20
		elif ySpeed < 10:
			self.rotation = 20 + ySpeed * -5
		self.image = pg.transform.rotate(self.picture, self.rotation)
		
class Pipe (pg.sprite.Sprite):
	def __init__(self, picture):
		super().__init__()
		self.picture = picture
		self.image = picture
		self.rect = self.image.get_rect()
		self.mask = pg.mask.from_surface(self.image)

def drawPipe (i, pipePos):
	pipe = Pipe(pipePic)
	pipe.rect.x = pipePos[i][0]
	pipe.rect.y = pipePos[i][1]
	pipe_group.add(pipe)
#Makes Pipe Pictures One Picture
pipePic = pg.Surface((50, 7000))
pipePic.blit(upPipePic, (0, 400))
pipePic.blit(downPipePic, (0, 0))
#Groups Bird Sprite
bird_group = pg.sprite.Group()
bird = Bird(birdPic)
bird_group.add(bird)
#Groups Pipe Sprites
pipe_group = pg.sprite.Group()
pipe = Pipe(pipePic)
pipe_group.add(pipe)
#Main Game Loop
while running:
	#Initializes Frame Rate
	clock.tick(60)
	#Gets Keystrokes
	for event in pg.event.get():
		#Quits Game If You Press The Quit Button
		if event.type == pg.QUIT:
			running = False
		#Detects Keystroke
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_UP:
				if not dead:
					ySpeed = 0
					ySpeed -= 3.5
			#Detects Enter Key And Restarts If Dead 
			if event.key == pg.K_RETURN:
				if dead:
					 os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
	#Creates Gravity
	if birdPos[1] <= 400 and grav < 4:
		birdPos[1] += ySpeed
		ySpeed += grav 
	#Detects Groud Collision
	if birdPos[1] >= 405:
		birdPos[1] = 405
		movement = 0
		dead = True
	#Changes Bird Y Position
	birdPos[1] += ySpeed
	#Moves Pipes
	for i in range(len(pipePos)):
		pipePos[i][0] -= movement
	#Keeps Track Of Distance Between Pipes
	pipeGap += movement
	#Spawns A New Pipe If Distance Between Them Is Great Enough
	if pipeGap == 200:
		pipePos.append([500, random.randrange(-200, 0, 10)])
		#Resets Distance Counter
		pipeGap = 0
	#Deletes Pipe If It Is Off Screen
	if pipePos[0][0] == -50:
		del pipePos[0]
	#Detects When Pipe Goes Past Bird
	for i in range(len(pipePos)):
		if pipePos[i][0] == 200 and not dead:
			points += 1
	#Moves Bird Sprite Based Off Of Its Proper Position
	bird.rect.x = birdPos[0]
	bird.rect.y = birdPos[1]
	#THIS NEEDS OPTIMIZED
	pipe_group.empty()
	for i in range(len(pipePos)):
		drawPipe(i, pipePos)
	#Detects Collision Between The Pipes And Bird
	collision = pg.sprite.spritecollide(bird, pipe_group, False, pg.sprite.collide_mask)
	if collision:
		movement = 0
		dead = True
	#Scrolls Background
	for i in range(2):
		backgroundPos[i] -= movement/5
		if backgroundPos[i] == -500:
			backgroundPos[i] = 500
		display.blit(background, (backgroundPos[i], 0))
	#Draws Pipes
	pipe_group.draw(display)
	#Scrolls Ground
	for i in range(2):
		groundPos[i] -= movement
		if groundPos[i] == -500:
			groundPos[i] = 500
		display.blit(ground, (groundPos[i], 450))
	#Displays Bird
	bird_group.draw(display)
	#Scoreboard
	outScore = outFont.render(str(points), True, black)
	outScoreRect = outScore.get_rect()
	outScoreRect.center = (250, 50)
	display.blit(outScore, outScoreRect)
	inScore = inFont.render(str(points), True, white)
	inScoreRect = inScore.get_rect()
	inScoreRect.center = (250, 50)
	display.blit(inScore, inScoreRect)
	#Updates All Groups And Display
	pg.display.update()
	bird_group.update()
	pipe_group.update()