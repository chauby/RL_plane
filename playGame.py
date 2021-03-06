#-*-coding:UTF-8 -*-
# import the pygame module
import pygame
import random
import time
import os.path
from datetime import datetime

# import pygame.locals for easier access to key coordinates
from pygame.locals import *

# import font
from pygame.font import *

#定义游戏的屏幕大小
width = 800
hight = 600
main_dir = os.path.split(os.path.abspath(__file__))[0]

#定义Player类
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		image = pygame.image.load('source/GodPlane.png').convert()
		self.image = pygame.transform.scale(image, (64, 64))
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center = (width/2, 500))#set the plaer's init position

	def update(self, pressed_keys):
		if pressed_keys[K_UP]:
			self.rect.move_ip(0, -2)
		if pressed_keys[K_DOWN]:
			self.rect.move_ip(0, 2)
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-2, 0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(2, 0)

		#限制plaer的移动范围，不能超出屏幕
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > width:
			self.rect.right = width
		if self.rect.top < 0:
			self.rect.top = 0
		elif self.rect.bottom > hight:
			self.rect.bottom = hight 

#定义子弹类
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x_position, y_position):
		super(Bullet, self).__init__()
		image = pygame.image.load('source/bullet.png').convert()
		self.image = pygame.transform.scale(image, (16, 16))
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center = (x_position, y_position))
		self.speed = 2

	def update(self):
		self.rect.move_ip(0, -self.speed)
		if self.rect.top < 0:
			self.kill()

#定义血点奖励类
class RewardBlood(pygame.sprite.Sprite):
	def __init__(self):
		super(RewardBlood, self).__init__()
		image = pygame.image.load('source/sphere.png').convert()
		self.image = pygame.transform.scale(image, (32, 32))
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center = (random.randint(0, width), 0))
		self.speed = random.randint(1, 2)

	def update(self):
		self.rect.move_ip(0, self.speed)
		if self.rect.bottom > hight:
			self.kill()

#定义敌人类
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		index = random.randint(0, 3)
		if index == 0:
			image = pygame.image.load('source/JpPlane.png').convert()
		elif index == 1:
			image = pygame.image.load('source/GreenPlane.png').convert()
		elif index == 2:
			image = pygame.image.load('source/JitPlane.png').convert()
		else:
			image = pygame.image.load('source/LXPlane.png').convert()

		self.image = pygame.transform.scale(image, (32, 32))
		self.init_position = [10, 100, 200, 300, 400, 500, 600, 700, 790]
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center = (self.init_position[random.randint(0, 8)], 0))
		# self.speed = random.randint(1, 2)
		self.speed = 1

	def update(self):
		self.rect.move_ip(0, self.speed)
		if self.rect.bottom > hight:
			self.kill()

#定义云朵类
class Cloud(pygame.sprite.Sprite):
	"""docstring for Cloud"""
	def __init__(self):
		super(Cloud, self).__init__()
		self.image = pygame.image.load('source/cloud.png').convert()
		self.image.set_colorkey((0, 0, 0), RLEACCEL)
		self.rect = self.image.get_rect(center = (random.randint(0, width), 0))
		self.speed = random.randint(1,3)

	def update(self):
		self.rect.move_ip(0, self.speed)
		if self.rect.bottom > hight + 50:
			self.kill()

#定义声音类
class dummysound:
	def play(self):pass

def load_sound(file):
	if not pygame.mixer: return dummysound()
	file = os.path.join(main_dir, 'source', file)
	try:
		sound = pygame.mixer.Sound(file)
		return sound
	except pygame.error:
		print "warning, unnable to load, %s" % file
	return dummysound()

def show_text(surface_handle, pos, text, color, font_bold = False, font_size = 13, font_italic = False):   
    ''''' 
    Function:文字处理函数 
    Input：surface_handle：surface句柄 
           pos：文字显示位置 
           color:文字颜色 
           font_bold:是否加粗 
           font_size:字体大小 
           font_italic:是否斜体 
    Output: NONE 
    author: socrates 
    blog:http://blog.csdn.net/dyx1024 
    date:2012-04-15 
    '''         
    #获取系统字体，并设置文字大小  
    cur_font = pygame.font.SysFont("宋体", font_size)  
      
    #设置是否加粗属性  
    cur_font.set_bold(font_bold)  
      
    #设置是否斜体属性  
    cur_font.set_italic(font_italic)  
      
    #设置文字内容  
    text_fmt = cur_font.render(text, 1, color)  
      
    #绘制文字  
    surface_handle.blit(text_fmt, pos)   

def playGame():
	# initialize pygame
	pygame.init()

	# create the screen object
	# here we pass it a size of 800x600
	screen = pygame.display.set_mode((width, hight))

	#创建游戏背景
	background = pygame.Surface(screen.get_size())
	background.fill((135, 206, 250))

	# Create a custom event for adding a new enemy.
	ADDENEMY = pygame.USEREVENT + 1
	pygame.time.set_timer(ADDENEMY, 500)
	ADDCLOUD = pygame.USEREVENT + 2
	pygame.time.set_timer(ADDCLOUD, 1000)
	ADDREWARD = pygame.USEREVENT + 3
	pygame.time.set_timer(ADDREWARD, 1000)
	ADDBULLET = pygame.USEREVENT + 4
	pygame.time.set_timer(ADDBULLET, 200)

	#创建plaer
	player = Player()

	#创建敌人集合
	enemies = pygame.sprite.Group()

	#创建云彩集合
	clouds = pygame.sprite.Group()

	#创建奖励集合
	rewardBloods = pygame.sprite.Group()

	#创建子弹集合
	bullets = pygame.sprite.Group()

	all_sprites = pygame.sprite.Group()
	all_sprites.add(player)

	#加入声音
	boom_sound = load_sound('boom.wav')
	shoot_sound = load_sound('shoot.wav')
	if pygame.mixer:
		music = os.path.join(main_dir, 'source', 'hundouluo.mp3')
		pygame.mixer.music.load(music)
		pygame.mixer.music.play(-1)

	start_time = datetime.now()
	current_time = start_time
	player_get_bloods = 0
	player_hit_enemies = 0

	#main loop
	running = True
	game_over = False
	while running:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
				elif event.key == K_SPACE:
					if (len(bullets) <= 3) and (game_over == False):
						new_bullet = Bullet(player.rect[0] + 32, player.rect[1])
						bullets.add(new_bullet)
						all_sprites.add(new_bullet)
						shoot_sound.play()

			elif event.type == QUIT:
				running = False
			elif event.type == ADDENEMY:
				new_enemy = Enemy()
				enemies.add(new_enemy)
				all_sprites.add(new_enemy)
			elif event.type == ADDCLOUD:
				new_cloud = Cloud()
				clouds.add(new_cloud)
				all_sprites.add(new_cloud)
			elif event.type == ADDREWARD:
				new_reward = RewardBlood()
				rewardBloods.add(new_reward)
				all_sprites.add(new_reward)
	                elif event.type == ADDBULLET:
	                        if (len(bullets) <= 3) and (game_over == False):
	                                new_bullet = Bullet(player.rect[0] + 32, player.rect[1])
	                                bullets.add(new_bullet)
	                                all_sprites.add(new_bullet)
	                                shoot_sound.play()

		screen.blit(background, (0, 0))
		clouds.update()
		enemies.update()
		rewardBloods.update()
		if game_over == False:
			pressed_keys = pygame.key.get_pressed()
			player.update(pressed_keys)
		bullets.update()

		for entity in all_sprites:
			screen.blit(entity.image, entity.rect)

		#遇到敌人
		if pygame.sprite.spritecollideany(player, enemies):
			player.kill()
			game_over = True
			boom_sound.play()

		#击中敌人
		if pygame.sprite.groupcollide(bullets, enemies, True, True):
			player_hit_enemies += 1

		#获得血液
		if pygame.sprite.spritecollide(player, rewardBloods, True):
			player_get_bloods += 1

		if game_over == True:
			show_text(screen, (width/2 - 230, hight/2 - 100), "GAME OVER", (255, 0, 0), False, font_size = 100)
		else:
			current_time = datetime.now()

		#score_text = u"Score: %s" % ((current_time - start_time).seconds + player_get_bloods + player_hit_enemies)
		score_text = u"Score: %s" % (player_get_bloods + player_hit_enemies)
		show_text(screen, (20, 20), score_text, (0, 0, 255), False, font_size = 28)

		#将两次flip之间的修改更新到整个屏幕
		pygame.display.flip()

if __name__ == "__main__":
	playGame()