import pygame
import sys
import time
import random

WIDTH = 600
HEIGHT = 600
WALL_WIDTH = WIDTH / 20
BALL_RADIUS = 10
BLACK_COLOR = (0,0,0,0)
WHITE_COLOR = (255,255,255,0)
GREEN_COLOR = (0,255,0,0)


pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('bounce')


class Wall:
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def draw_wall(self):
		pygame.draw.rect(screen,BLACK_COLOR,(self.x,self.y,self.width,self.height))




class Ball:
	def __init__(self,x,y,radius):
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		self.radius = radius
		self.g = 3
		self.direction = ''

	def draw_ball(self):
		pygame.draw.circle(screen,WHITE_COLOR,(self.x,self.y),self.radius)

	def drop(self):
		self.dy += self.g
		self.y += self.dy
		if self.y + self.radius >= bottom_wall.y:
			self.y = bottom_wall.y - self.radius 
		if self.y - self.radius <= top_wall.height:
			self.y = top_wall.height + self.radius

	def bounce(self):
		self.dy = -self.dy
		self.dy *= 0.8

	def wall_bounce(self,wall):
		if abs(self.dx) > 3:
			if wall == left_wall:
				self.x = wall.width + self.radius
			elif wall == right_wall:
				self.x = wall.x - self.radius
			self.dx = -self.dx

	def jump(self):
		#to only allow jumps IF ball is touching ground
		#if self.y >= bottom_wall.y - self.radius:
		#	self.dy = -50
		self.dy = -50
	def move(self,direction):
		if direction =='left':
			self.dx = -12
		elif direction == 'right':
			self.dx = 12
		else:
			if self.dx > 0:
				self.dx -=0.5
			elif self.dx < 0:
				self.dx +=0.5
			else:
				self.dx = 0
		self.x +=self.dx





class CollisionManager:
	def between_ball_and_ground(self,ball,wall):
		if ball.y + ball.radius >= wall.y:
			return True
		return False
	def between_ball_and_ceiling(self,ball,wall):
		if ball.y - ball.radius <= wall.height:
			return True
		return False
	def between_ball_and_left_wall(self,ball,wall):
		if ball.x - ball.radius <= wall.width:
			return True
		return False
	def between_ball_and_right_wall(self,ball,wall):
		if ball.x + ball.radius >= wall.x:
			return True
		return False






left_wall = Wall(0,0,WALL_WIDTH,HEIGHT)
right_wall = Wall(WIDTH-WALL_WIDTH,0,WALL_WIDTH,HEIGHT)
top_wall = Wall(WALL_WIDTH,0,WIDTH-(2*WALL_WIDTH),WALL_WIDTH)
bottom_wall = Wall(WALL_WIDTH,HEIGHT-WALL_WIDTH,WIDTH-(2*WALL_WIDTH),WALL_WIDTH)

def display_walls():
	left_wall.draw_wall()
	right_wall.draw_wall()
	top_wall.draw_wall()
	bottom_wall.draw_wall()


ball = Ball(random.randint(WALL_WIDTH,WIDTH-WALL_WIDTH),random.randint(WALL_WIDTH,HEIGHT-WALL_WIDTH),BALL_RADIUS)
collision = CollisionManager()
balls = [ball]
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
			if event.key == pygame.K_SPACE:
				for b in balls:
					b.jump()
			if event.key == pygame.K_LEFT:
				ball.direction = 'left'
			if event.key == pygame.K_RIGHT:
				ball.direction = 'right'
			if event.key == pygame.K_b:
				nextBall = Ball(random.randint(WALL_WIDTH,WIDTH-WALL_WIDTH),random.randint(WALL_WIDTH,HEIGHT-WALL_WIDTH),BALL_RADIUS)
				balls.append(nextBall)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				ball.direction = ''
	
	screen.fill(GREEN_COLOR)
	display_walls()
	
	for b in balls:
		b.move(ball.direction)
		b.drop()
		if collision.between_ball_and_ground(b,bottom_wall):
			b.bounce()
		if collision.between_ball_and_ceiling(b,top_wall):
			b.bounce()
		if collision.between_ball_and_left_wall(b,left_wall):
			b.wall_bounce(left_wall)
		if collision.between_ball_and_right_wall(b,right_wall):
			b.wall_bounce(right_wall)
		b.draw_ball()
	time.sleep(0.03)
	pygame.display.update()
