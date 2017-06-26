import os, itertools, threading, glob
import pygame.gfxdraw as gfxdraw
from pygame import *
from math import *
from random import *

vec = math.Vector2

# Colors
WHITE = (255,255,255)
GREY = (120,120,120)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (200,200,0)
PINK = (255,100,100)

enemy_colors = [RED, BLUE, GREEN, YELLOW, PINK]
enemy_speeds = [2,2,2,3,5]

init()

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,40'
width, height = 800, 640
screen = display.set_mode((width,height))
screen_rect = screen.get_rect()
FPS = 60
myClock = time.Clock()
running = True
tool = 'selection'
selected_tower = None

map1points = [(0, 64), (288,150), (576, 64), (576, 192), (64, 192), (64, 330), (576, 330), (576, 448), (64, 448), (64, 576), (640, 576)]
map2points = [(0, 0),(620, 620)]
map3points = [(0, 0),(100, 0),(100, 100),(200, 100),(200, 200),(300, 200),(300, 300),(400, 300),(400, 400),(500, 400),(500, 500),(600, 500),(600, 600),(640, 600)]
map4points = [(0, 0), (0, 640), (640, 640), (640, 0), (100, 0), (100, 540), (540, 540), (540, 100), (200, 100), (200, 440), (440, 440), (440, 200), (300, 200), (300, 340), (640, 340)]
map5points = [(300, 640), (300, 450), (80, 540), (210, 310), (70, 60), (320, 200), (570, 60), (440, 310), (540, 540), (340, 450), (330, 640)]
map6points = [(0, 0), (10, 0), (20, 0), (30, 0), (40, 0), (50, 0), (60, 0), (70, 0), (80, 0), (90, 0), (100, 0), (110, 0), (110, 0), (120, 0), (130, 0), (150, 0), (150, 0), (160, 0), (170, 0), (190, 0), (190, 0), (210, 0), (230, 0), (240, 0), (250, 0), (260, 0), (270, 0), (290, 0), (290, 0), (310, 10), (320, 10), (330, 10), (350, 10), (370, 0), (380, 0), (410, 0), (420, 0), (440, 0), (440, 0), (450, 0), (460, 0), (460, 0), (480, 0), (490, 0), (520, 0), (530, 0), (550, 0), (560, 0), (570, 0), (600, 10), (610, 10), (610, 10), (610, 20), (620, 40), (600, 60), (590, 80), (520, 120), (440, 160), (380, 120), (400, 10), (530, 40), (530, 80), (470, 100), (410, 80), (310, 50), (250, 50), (210, 40), (170, 50), (130, 60), (100, 90), (80, 110), (80, 140), (80, 180), (80, 230), (80, 280), (100, 320), (110, 340), (190, 400), (260, 430), (350, 430), (590, 240), (590, 220), (550, 150), (430, 130), (300, 110), (240, 170), (220, 250), (150, 350), (40, 420), (0, 490), (0, 550), (20, 590), (30, 600), (80, 610), (120, 610), (180, 610), (240, 610), (320, 620), (380, 600), (430, 570), (450, 500), (430, 450), (370, 490), (340, 530), (290, 550), (220, 570), (120, 570), (80, 530), (70, 450), (90, 440), (130, 400), (180, 370), (190, 320), (170, 290), (140, 280), (100, 250), (70, 220), (60, 170), (70, 140), (110, 100), (190, 100), (310, 120), (390, 150), (450, 190), (470, 230), (500, 300), (530, 380), (540, 430), (570, 490), (640, 640)]
map7points = [(0, 0),(0, 310), (640, 310), (640, 0), (330, 0), (330, 640), (640, 640), (640, 330), (0, 330), (0, 640), (310, 640), (310, 0), (0, 0)]
map8points = [(0, 10), (20, 190), (180, 110), (140, 70), (140, 230), (320, 340), (410, 250), (330, 120), (430, 70), (580, 90), (490, 210), (560, 30), (740, 50), (790, 210), (620, 240), (300, 50), (70, 270), (70, 470), (500, 420), (800, 500)]
all_maps_points = [map1points,map2points,map3points,map4points, map5points, map6points, map7points, map8points]
current_map_index = 0
current_map = all_maps_points[current_map_index]
map_mask = Surface((640,640))

map_surf = Surface((640,640))
map_surf.fill(WHITE)
map_rect = map_surf.get_rect()

side_bar_rect = Rect(640,0,160,640)
start_round_button = Surface((side_bar_rect.width-20, 50))
start_round_button.fill(BLUE)
start_round_rect = start_round_button.get_rect()
start_round_rect.bottomright = side_bar_rect.right - 10, side_bar_rect.bottom - 10

header_font = font.SysFont('Showcard Gothic', 20)
type_render_text = 'Type: Close'
type_render = header_font.render(type_render_text, True, WHITE)

def get_image(sheet, pos):
	img = Surface((pos[2],pos[3]), SRCALPHA)
	img.fill((255,255,255,0))
	img.blit(sheet, img.get_rect(), pos)
	return img

def get_cos(file_path):
	f = open(file_path).read().strip()
	co_list = f.split('\n')
	for i in co_list:
		if i[0] == '\t':
			i = i[1:]
	for pos in range(len(co_list)):
		co_list[pos] = co_list[pos].split(' ')
		for s in range(4):
			co_list[pos][s] = int(co_list[pos][s]) * 32

	return co_list

def load_images():
	global master_sheet, tower_sheet, tower_cos
	master_sheet = image.load('images/master_sheet.png')
	tower_sheet = image.load('images/tower_sheet.png')
	tower_cos = get_cos('images/tower_co.txt')
	time.wait(2000)

loading_ani_pics = []
folder = 'images/loading images 2'
for i in range(len(glob.glob(folder+'/*.png'))):
	tmp = image.load(folder + '/frame{0:0>3}.png'.format(i))
	loading_ani_pics.append(transform.scale(tmp, (width, height)))
def loading_animation():
	for i in itertools.cycle(loading_ani_pics):
		if done_loading_images:
			break
		i.set_colorkey(i.get_at((0,0)))
		screen.fill(i.get_at((0,0)))
		tmpRect = i.get_rect()
		tmpRect.center = width/2, height/2
		screen.blit(i, tmpRect)
		display.flip()
		time.wait(5)

# Give a target function and this function will thread it with an animation
def do_loading(target, args=[]):
	global done_loading_images
	done_loading_images = False
	l = threading.Thread(target=target, args=args)
	l.start()
	a = threading.Thread(target=loading_animation, args=[])
	a.start()

	while done_loading_images == False:
		if not l.isAlive():
			done_loading_images = True

do_loading(load_images)

class Bullet:
	def __init__(self, angle, pos, speed=30, size=10, lives=0):
		bullets.append(self)
		self.pos, self.angle, self.speed, self.lives = pos, angle, speed, lives
		self.image = Surface((size, size), SRCALPHA)
		self.rect = self.image.get_rect()
		draw.circle(self.image, GREEN, self.rect.center, self.rect.width//2)
		self.rect.center = pos
		self.pos = vec(pos[0], pos[1])
		self.vx = self.speed * cos(self.angle)
		self.vy = self.speed * sin(self.angle)

	def kill(self):
		bullets.remove(self)

	def move(self):
		global dead_enemies
		self.pos.x += self.vx
		self.pos.y += self.vy
		self.rect.center = self.pos

		if not map_rect.colliderect(self.rect):
			self.kill()
		else:
			for e in enemies:
				if e.rect.colliderect(self.rect):
					e.health -= 1
					if e.health <= 0:
						e.kill()
						dead_enemies += 1
					self.lives -= 1
					if self.lives <= 0:
						self.kill()
					break

class FreezePellet:
	def __init__(self, angle, pos, size=10):
		bullets.append(self)
		self.pos, self.angle, self.speed = pos, angle, randint(5,30) / 10
		self.image = Surface((size, size), SRCALPHA)
		self.rect = self.image.get_rect()
		draw.circle(self.image, choice([BLUE, (100,100,255), (150,150,255), (50,50,255)]), self.rect.center, self.rect.width//2)
		self.rect.center = pos
		self.pos = vec(pos[0], pos[1])
		self.vx = self.speed * cos(self.angle)
		self.vy = self.speed * sin(self.angle)
		self.fric = 0.025

	def kill(self):
		bullets.remove(self)

	def move(self):
		global dead_enemies
		self.vx -= self.vx * self.fric
		self.vy -= self.vy * self.fric
		self.pos.x += self.vx
		self.pos.y += self.vy
		self.rect.center = self.pos

		if not map_rect.colliderect(self.rect) or hypot(self.vx,self.vy) < 0.1:
			self.kill()
		else:
			for e in enemies:
				if e.rect.colliderect(self.rect):
					e.frozen_counter = 0
					self.kill()
					break

class Tower:
	def __init__(self, pos, rad, target='first'):
		self.sheet_index_number = 0
		self.tower_types = ['first', 'strong', 'close']
		self.type_index = self.tower_types.index(target)
		self.rad, self.pos, self.target = rad, pos, self.tower_types[self.type_index]
		self.old_upgrade_num = 1
		self.upgrade_num = 0
		self.images = self.get_images_list(self.upgrade_num)
		self.original_image = self.images[0]
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.rect.center = pos

		self.shoot_delay = 0
		self.shoot_delay_max = 20		# After how long tower can shoot
		self.bullet_speed = 15
		self.bullet_size = 10
		self.randomness = 5
		self.bullets_per_frame = 1
		self.weapon = Bullet

		self.angle_to_enemy = None

		self.shooting = False
		self.shooting_counter = 0
		self.shooting_counter_max = 3	# Shooting animation delay
		self.shooting_frame = 0

		self.fire_images = [get_image(tower_sheet, tower_cos[9]), get_image(tower_sheet, tower_cos[10]), get_image(tower_sheet, tower_cos[11])]
		self.fire_counter = 0
		self.fire_counter_max = 2
		self.fire_frame = 0

	def kill(self): towers.remove(self)

	def get_images_list(self, upgrade_num):
		l = []
		for i in range(3):
			tmp = get_image(tower_sheet, tower_cos[self.sheet_index_number + upgrade_num*3+i])
			l.append(transform.scale(tmp, (tmp.get_width()*2, tmp.get_height()*2)))
		l.append(l[1])
		return l

	def find_close_enemy(self):
		dists = []
		for pos in range(len(enemies)):
			e = enemies[pos]
			d = hypot(e.rect.centerx - self.rect.centerx, e.rect.centery - self.rect.centery)
			dists.append((d))
		if dists:
			small_dist = dists.index(min(dists))
			if dists[small_dist] <= self.rad:
				return enemies[small_dist]
		return None

	def find_first_enemy(self):
		dist_traveled = []
		en = []
		for e in enemies:
			if hypot(self.rect.centerx - e.rect.centerx, self.rect.centery - e.rect.centery) <= self.rad:
				dist_traveled.append(e.distance_traveled)
				en.append(e)
		if dist_traveled:
			return enemies[enemies.index(en[dist_traveled.index(max(dist_traveled))])]
		return None

	def find_strong_enemy(self):
		lives = []
		en = []
		for e in enemies:
			if hypot(e.rect.centerx - self.rect.centerx, e.rect.centery - self.rect.centery) <= self.rad:
				lives.append(e.health)
				en.append(e)

		if lives:
			return enemies[enemies.index(en[lives.index(max(lives))])]

	def update(self):
		if self.type_index == len(self.tower_types):
			self.type_index = 0
		elif self.type_index < 0:
			self.type_index = len(self.tower_types)-1

		if self.target != self.tower_types[self.type_index]:
			self.target = self.tower_types[self.type_index]

		if self.old_upgrade_num != self.upgrade_num:
			self.images = self.get_images_list(self.upgrade_num)
			self.old_upgrade_num = self.upgrade_num
			self.original_image = self.images[0]

		if self.target == 'first':
			target_enemy = self.find_first_enemy()
		if self.target == 'close':
			target_enemy = self.find_close_enemy()
		if self.target == 'strong':
			target_enemy = self.find_strong_enemy()


		self.animate()
		if target_enemy != None:
			self.angle_to_enemy = atan2(target_enemy.rect.centery - self.rect.centery, target_enemy.rect.centerx - self.rect.centerx)
			self.shoot_delay += 1
			if self.shoot_delay >= self.shoot_delay_max:
				self.shoot_delay = 0
				self.shooting = True
				for i in range(self.bullets_per_frame):
					if self.upgrade_num == 0:
						shot = self.weapon(self.angle_to_enemy+radians(randint(-self.randomness, self.randomness)), (self.rect.centerx + 2*16*cos(self.angle_to_enemy), self.rect.centery + 2*16*sin(self.angle_to_enemy)), size=self.bullet_size)
					elif self.upgrade_num == 1:
						shot = self.weapon(self.angle_to_enemy+radians(randint(-self.randomness, self.randomness)), (self.rect.centerx + 2*16*cos(self.angle_to_enemy+radians(10)), self.rect.centery + 2*16*sin(self.angle_to_enemy+radians(10))), size=self.bullet_size)
						shot = self.weapon(self.angle_to_enemy+radians(randint(-self.randomness, self.randomness)), (self.rect.centerx + 2*16*cos(self.angle_to_enemy-radians(10)), self.rect.centery + 2*16*sin(self.angle_to_enemy-radians(10))), size=self.bullet_size)
					elif self.upgrade_num == 2:
						shot = self.weapon(self.angle_to_enemy+radians(randint(-self.randomness, self.randomness)), (self.rect.centerx + 2*14*cos(self.angle_to_enemy+radians(40)), self.rect.centery + 2*14*sin(self.angle_to_enemy+radians(40))), size=self.bullet_size)
						shot = self.weapon(self.angle_to_enemy+radians(randint(-self.randomness, self.randomness)), (self.rect.centerx + 2*14*cos(self.angle_to_enemy-radians(40)), self.rect.centery + 2*14*sin(self.angle_to_enemy-radians(40))), size=self.bullet_size)
						shot = self.weapon(self.angle_to_enemy+radians(randint(-self.randomness, self.randomness)), (self.rect.centerx + 2*16*cos(self.angle_to_enemy), self.rect.centery + 2*16*sin(self.angle_to_enemy)), size=self.bullet_size)

		if self.angle_to_enemy == None:
			self.image = transform.rotate(self.original_image, 0)
		else:
			self.image = transform.rotate(self.original_image, 270 - degrees(self.angle_to_enemy))
		self.rect = self.image.get_rect()
		self.rect.center = self.pos

		draw.circle(map_mask, BLUE, self.pos, tower_place_size)
		gfxdraw.filled_circle(map_surf, self.pos[0], self.pos[1], tower_place_size, BLUE+(150,))

class Freeze(Tower):
	def __init__(self, pos, rad, target='first'):
		super().__init__(pos, rad, target)
		self.sheet_index_number = 18
		self.shoot_delay_max = 5	# Time between shooting
		self.bullet_size = 5
		self.randomness = 40
		self.bullets_per_frame = 5

		self.weapon = FreezePellet
		self.fire_images = [get_image(tower_sheet, tower_cos[27]), get_image(tower_sheet, tower_cos[28]), get_image(tower_sheet, tower_cos[29])]

	def animate(self):
		if self.shooting:
			self.shooting_counter += 1
			if self.shooting_counter >= self.shooting_counter_max:
				self.shooting_counter = 0
				self.shooting_frame += 1
				if self.shooting_frame > len(self.images)-1:
					self.shooting_frame = 0
					self.shooting = False
			self.fire_counter += 1
			if self.fire_counter >= self.fire_counter_max:
				self.fire_counter = 0
				self.fire_frame += 1
				if self.fire_frame >= len(self.fire_images):
					self.fire_frame = 0

			if self.upgrade_num != 0:
				tmp = transform.scale(self.fire_images[self.fire_frame], (48,48))
			else:
				tmp = transform.scale(self.fire_images[self.fire_frame], (64,64))
			tmp =  transform.rotate(tmp, 270 - degrees(self.angle_to_enemy))
			tmpRect = tmp.get_rect()
			if self.upgrade_num == 0:
				tmpRect.center = self.rect.centerx + 2*16*cos(self.angle_to_enemy), self.rect.centery + 2*16*sin(self.angle_to_enemy)
				map_surf.blit(tmp, tmpRect)
			elif self.upgrade_num == 1:
				tmpRect.center = self.rect.centerx + 2*16*cos(self.angle_to_enemy+radians(10)), self.rect.centery + 2*16*sin(self.angle_to_enemy+radians(10))
				map_surf.blit(tmp, tmpRect)

				tmpRect.center = self.rect.centerx + 2*16*cos(self.angle_to_enemy-radians(10)), self.rect.centery + 2*16*sin(self.angle_to_enemy-radians(10))
				map_surf.blit(tmp, tmpRect)
			elif self.upgrade_num == 2:
				tmpRect.center = self.rect.centerx + 2*16*cos(self.angle_to_enemy), self.rect.centery + 2*16*sin(self.angle_to_enemy)
				map_surf.blit(tmp, tmpRect)

				tmpRect.center = self.rect.centerx + 2*14*cos(self.angle_to_enemy+radians(40)), self.rect.centery + 2*14*sin(self.angle_to_enemy+radians(40))
				map_surf.blit(tmp, tmpRect)

				tmpRect.center = self.rect.centerx + 2*14*cos(self.angle_to_enemy-radians(40)), self.rect.centery + 2*14*sin(self.angle_to_enemy-radians(40))
				map_surf.blit(tmp, tmpRect)
		self.original_image = self.images[self.shooting_frame]

class Gunner(Tower):
	def __init__(self, pos, rad, target='first'):
		super().__init__(pos, rad, target)

	def animate(self):
		if self.shooting:
			self.shooting_counter += 1
			if self.shooting_counter >= self.shooting_counter_max:
				self.shooting_counter = 0
				self.shooting_frame += 1
				if self.shooting_frame > len(self.images)-1:
					self.shooting_frame = 0
					self.shooting = False

			self.fire_counter += 1
			if self.fire_counter >= self.fire_counter_max:
				self.fire_counter = 0
				self.fire_frame += 1
				if self.fire_frame >= len(self.fire_images):
					self.fire_frame = 0

			if self.upgrade_num != 0:
				tmp = transform.scale(self.fire_images[self.fire_frame], (48,48))
			else:
				tmp = transform.scale(self.fire_images[self.fire_frame], (64,64))
			tmp =  transform.rotate(tmp, 270 - degrees(self.angle_to_enemy))
			tmpRect = tmp.get_rect()
			if self.upgrade_num == 0:
				tmpRect.center = self.rect.centerx + 2*16*cos(self.angle_to_enemy), self.rect.centery + 2*16*sin(self.angle_to_enemy)
				map_surf.blit(tmp, tmpRect)
			elif self.upgrade_num == 1:
				tmpRect.center = self.rect.centerx + 2*16*cos(self.angle_to_enemy+radians(10)), self.rect.centery + 2*16*sin(self.angle_to_enemy+radians(10))
				map_surf.blit(tmp, tmpRect)

				tmpRect.center = self.rect.centerx + 2*16*cos(self.angle_to_enemy-radians(10)), self.rect.centery + 2*16*sin(self.angle_to_enemy-radians(10))
				map_surf.blit(tmp, tmpRect)
			elif self.upgrade_num == 2:
				tmpRect.center = self.rect.centerx + 2*16*cos(self.angle_to_enemy), self.rect.centery + 2*16*sin(self.angle_to_enemy)
				map_surf.blit(tmp, tmpRect)

				tmpRect.center = self.rect.centerx + 2*14*cos(self.angle_to_enemy+radians(40)), self.rect.centery + 2*14*sin(self.angle_to_enemy+radians(40))
				map_surf.blit(tmp, tmpRect)

				tmpRect.center = self.rect.centerx + 2*14*cos(self.angle_to_enemy-radians(40)), self.rect.centery + 2*14*sin(self.angle_to_enemy-radians(40))
				map_surf.blit(tmp, tmpRect)
		self.original_image = self.images[self.shooting_frame]

class Enemy:
	def __init__(self, health=10):
		self.total_health = health
		self.health = health
		self.speed = enemy_speeds[self.health-1]
		self.image = Surface((20, 20), SRCALPHA)
		self.image.fill((255,255,255,0))
		self.rect = self.image.get_rect()
		draw.circle(self.image, enemy_colors[self.health-1], (self.rect.width//2, self.rect.height//2), self.rect.width//2)
		self.rect.center = current_map[0]
		self.seg = 1
		self.vel = vec(0, 0)
		self.pos = vec(current_map[0][0], current_map[0][1])
		self.distance_traveled = 0
		self.frozen_counter_max = 240
		self.frozen_counter = self.frozen_counter_max + 1

	def kill(self):
		enemies.remove(self)

	def move(self):
		global dead_enemies
		self.frozen_counter += 1
		if self.frozen_counter < self.frozen_counter_max:
			self.speed = enemy_speeds[self.health-1] * 3/5
		else:
			self.speed = enemy_speeds[self.health-1]
		self.distance_traveled += self.speed
		while True:
			try:
				x2 = current_map[self.seg][0]
				break
			except IndexError:
				self.seg -= 1
		x2 = current_map[self.seg][0]
		y2 = current_map[self.seg][1]
		dist=hypot(self.rect.centerx-x2,self.rect.centery-y2)
		if dist<=self.speed:
			if self.seg<len(current_map)-1:
				self.seg+=1
			elif current_map[self.seg] == current_map[-1]:
				dead_enemies += 1
				self.kill()
		xdiff = self.rect.centerx - current_map[self.seg][0]
		ydiff = self.rect.centery - current_map[self.seg][1]
		angle = radians(180) + atan2(ydiff, xdiff)
		vx = self.speed * (cos(angle))
		vy = self.speed * (sin(angle))
		self.vel.x = vx
		self.vel.y = vy

		self.pos.x += self.vel.x
		self.pos.y += self.vel.y
		self.rect.center = self.pos

		draw.circle(self.image, enemy_colors[self.health-1], (self.rect.width//2, self.rect.height//2), self.rect.width//2)
		draw.rect(map_surf, GREY, (self.rect.x-self.rect.width//2, self.rect.y - 20, self.rect.width*2, 10))
		draw.rect(map_surf, GREEN, (self.rect.x-self.rect.width//2, self.rect.y - 20, self.rect.width*2/self.total_health*self.health, 10))

towers = []
bullets = []
enemies = []
dead_enemies = 0

side_bar_slot1 = Rect(side_bar_rect.x + 20, 20, 50, 50)
side_bar_slot2 = Rect(side_bar_rect.x + 90, 20, 50, 50)
side_bar_slot3 = Rect(side_bar_rect.x + 20, 90, 50, 50)
side_bar_slot4 = Rect(side_bar_rect.x + 90, 90, 50, 50)

spawning_in = False
round_going = False
spawn_delay = 0
spawn_delay_max = 10
max_enemies = 10

tower_place_size = 30

for i in [-100,0,100]:
	t1 = Freeze((map_rect.width//2+i, map_rect.height//2 - 75), 200)
	towers.append(t1)

key.set_repeat(500,20)
while running:
	click = False
	let_go = False
	for evt in event.get():
		if evt.type == QUIT:
			running = False

		elif evt.type == KEYDOWN:
			if evt.key == 127:		# DELETE KEY
				if selected_tower != None:
					selected_tower.kill()
					map_mask.fill(WHITE)
					selected_tower = None

			if evt.key == K_ESCAPE:
				if tool == 'selection':
					running = False
				else:
					tool = 'selection'
					selected_tower = None

			if evt.key == K_1: tool = 'close'
			if evt.key == K_2: tool = 'strong'
			if evt.key == K_3: tool = 'first'

			if evt.key == K_t:
				if FPS == 60:
					FPS = 120
				elif FPS == 120:
					FPS = 60

			if evt.key == K_RETURN:
				if selected_tower != None and selected_tower.upgrade_num < 2:
					selected_tower.upgrade_num += 1
					selected_tower.rad += 20
		elif evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1: click = True
			if evt.button == 4:
				current_map_index += 1
				if current_map_index == len(all_maps_points):
					current_map_index = 0

			if evt.button == 5:
				current_map_index -= 1
				if current_map_index < 0:
					current_map_index = len(all_maps_points)-1

		elif evt.type == MOUSEBUTTONUP:
			if evt.button == 1: let_go = True

	mx,my = mouse.get_pos()
	mb = mouse.get_pressed()

	screen.fill(WHITE)
	map_surf.fill(WHITE)

	if all_maps_points[current_map_index] != current_map:
		current_map = all_maps_points[current_map_index]

	draw.rect(screen, RED, side_bar_rect)
	draw.rect(screen, YELLOW, (side_bar_rect.x + 2, side_bar_rect.y + 2, side_bar_rect.width - 4, side_bar_rect.height - 4), 5)
	draw.rect(screen, WHITE, map_rect)
	gfxdraw.box(screen, start_round_rect, BLUE)
	draw.rect(screen, GREY, side_bar_slot1)
	draw.rect(screen, GREY, side_bar_slot2)
	draw.rect(screen, GREY, side_bar_slot3)
	draw.rect(screen, GREY, side_bar_slot4)

	for i in range(len(current_map)-1):
		draw.line(map_surf, BLACK, current_map[i], current_map[i+1], 3)

	if start_round_rect.collidepoint((mx,my)) and click and not round_going and not spawning_in:
		dead_enemies = 0
		round_going = True
		spawning_in = True

	if spawning_in:
		spawn_delay += 1
		if spawn_delay >= spawn_delay_max:
			spawn_delay = 0
			e = Enemy(health=5)
			enemies.append(e)
			if len(enemies) + dead_enemies >= max_enemies:
				spawning_in = False

	if dead_enemies >= max_enemies:
		round_going = False

	for b in bullets:
		b.move()
		map_surf.blit(b.image, b.rect)
	for e in enemies:
		e.move()
		map_surf.blit(e.image, e.rect)

	if selected_tower != None:
		gfxdraw.filled_circle(map_surf, selected_tower.rect.centerx, selected_tower.rect.centery, selected_tower.rad, BLACK+(100,))	
		type_string = "Type: " + selected_tower.target.lower().capitalize()
		if type_render_text != type_string:
			type_render = header_font.render(type_string, True, WHITE)
		type_render_text = type_string

		type_render_rect = type_render.get_rect()
		type_render_rect.midbottom = side_bar_rect.centerx, height-100
		screen.blit(type_render, type_render_rect)
		if type_render_rect.collidepoint((mx,my)):
			if click: selected_tower.type_index += 1

	for t in towers:
		t.update()
		map_surf.blit(t.image, t.rect)

	if map_rect.collidepoint((mx,my)):
		if tool == 'selection':
			if let_go:
				found_tower = False
				for t in towers:
					# if t.rect.collidepoint((mx,my)) and t != selected_tower:
					if hypot(mx - t.rect.centerx, my - t.rect.centery) <= tower_place_size and t != selected_tower:
						selected_tower = t
						found_tower = True
						break
				if not found_tower:
					selected_tower = None


		else:
			color_on_mask = map_mask.get_at((mx,my))
			if color_on_mask != BLUE:
				gfxdraw.filled_circle(map_surf, mx, my, tower_place_size, GREEN+(100,))
			else:
				gfxdraw.filled_circle(map_surf, mx, my, tower_place_size, RED+(100,))
			if let_go:
				if color_on_mask != BLUE:
					t = Gunner((mx,my), 150, target=tool)
					towers.append(t)
				tool = 'selection'
	screen.blit(map_surf, map_rect)
	display.flip()
	myClock.tick(FPS)
	dt = myClock.get_fps()
	display.set_caption('FPS: ' + str(dt))

quit()
