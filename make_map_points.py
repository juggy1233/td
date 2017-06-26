import os
from pygame import *

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,190,0)
BLUE = (0,0,255)

init()

MAPX = 800
MAPY = 500

os.environ['SDL_VIDEO_CENTERED'] = '1'
size = width,height = MAPX+2+200,MAPY+2
screen = display.set_mode(size)
map_rect = Rect(0,0,MAPX+2,MAPY+2)

display_font = font.SysFont('Showcard Gothic', 18)

def make_point_font(points):
	letter_width, letter_height = display_font.size(str(points[0]))
	surf = Surface((200, len(points)*letter_height), SRCALPHA)
	surf.fill((255,255,255,0))
	for n,p in enumerate(points):
		tmp = display_font.render(str(p), True, BLACK)
		tmp_rect = tmp.get_rect()
		tmp_rect.y = n * letter_height
	return surf

points = []
running = True

while running:
	click = False
	for evt in event.get():
		if evt.type == QUIT:
			running = False

		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False

		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				click = True

			if evt.button == 3:
				if points:
					del points[-1]

	mx, my = mouse.get_pos()
	mx, my = mx - mx%10, my - my%10

	screen.fill(WHITE)
	screen.fill(RED, (width-200,0,200,MAPX+2))

	if map_rect.collidepoint((mx,my)):
		if click:
			points.append((mx,my))

		mouse_text = display_font.render('X: ' + str(mx) + '   Y: ' + str(my), True, BLACK)
		screen.blit(mouse_text, (MAPX+10,10))
		draw.circle(screen, BLUE, (mx,my), 2)

	for n,p in enumerate(points):
		draw.circle(screen, GREEN, p, 6)
		screen.blit(display_font.render(str(p), True, BLACK), (MAPX,50+n*20))

	for pos in range(len(points[:-1])):
		draw.line(screen, BLACK, points[pos], points[pos+1], 2)

	display.flip()

quit()

with open('points.txt', 'w') as f:
	f.write('[')
	for p in points:
		f.write('(%i, %i)' % (p[0], p[1]))
		if p != points[-1]:
			f.write(', ')
	f.write(']')
