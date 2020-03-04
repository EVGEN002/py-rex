import pygame, sys, random, os

pygame.init()

current_path = os.path.dirname(__file__)
assets = os.path.join(current_path, 'assets')

FPS = 60
icon = pygame.image.load(os.path.join(assets, 'icon.png'))
pygame.display.set_icon(icon)
display_size = display_width, display_height = 800, 600
display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Py-Rex')
platform = 500 

#pygame.mixer.music.load(r'C:\Users\Evgeny\Desktop\STORAGE\CODE\game_dev\py-rex\assets\bg.mp3')
pygame.mixer.music.set_volume(0.3)

jump_sound = pygame.mixer.Sound(os.path.join(assets, 'jump.mp3'))
#hit_sound = pygame.mixer.Sound(r'C:\Users\Evgeny\Desktop\STORAGE\CODE\game_dev\py-rex\assets\hit.mp3')

barrier_img = [pygame.image.load(os.path.join(assets, 'cactus0.png')).convert_alpha(), 
pygame.image.load(os.path.join(assets, 'cactus1.png')).convert_alpha(), 
pygame.image.load(os.path.join(assets, 'cactus2.png')).convert_alpha()]
user_img = [pygame.image.load(os.path.join(assets, 'dino0.png')).convert_alpha(), pygame.image.load(os.path.join(assets, 'dino1.png')).convert_alpha()]
user_img_jump = pygame.image.load(os.path.join(assets, 'dino3.png')).convert_alpha()
cloud_img = pygame.image.load(os.path.join(assets, 'cloud.png')).convert_alpha()

user_width = user_img[0].get_rect().width
user_height = user_img[0].get_rect().height
cactus_options = [barrier_img[0].get_rect().width, platform - barrier_img[0].get_rect().height, barrier_img[1].get_rect().width, 
platform - barrier_img[1].get_rect().height, barrier_img[2].get_rect().width, platform - barrier_img[2].get_rect().height]
user_x = display_width // 5
user_y = platform - user_height

clock = pygame.time.Clock()
make_jump = False
jump_height = 20
jump_count = jump_height
img_count = 0
bg_x = 0
scores = 0
max_scores = 0
max_above = 0

class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed
    
    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))

def run_game():
    global make_jump, bg_x

    #pygame.mixer_music.play(-1)

    game = True
    barrier_arr = []
    create_barrier_arr(barrier_arr)
    background = pygame.image.load(os.path.join(assets, 'bg.jpg')).convert_alpha()
    cloud = open_cloud()
    while game:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    jump_sound.play()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause() 
        if make_jump:
            jump()
        count_scores(barrier_arr)
        if check_collision(barrier_arr):
            game = False
        rel_bg_x = bg_x % background.get_rect().width
        display.blit(background, (rel_bg_x - background.get_rect().width, 0))
        if rel_bg_x < display_width:
            display.blit(background, (rel_bg_x, 0))
        print_text('scores: ' + str(scores), 600, 10)
        bg_x -= 4
        draw_user()
        draw_array(barrier_arr)
        move_cloud(cloud)
        pygame.display.update()
        clock.tick(FPS)
    return game_over()

def jump():
    global user_y, jump_count, make_jump
    if jump_count >= -jump_height:
        user_y -= jump_count / 2
        jump_count -= 1
    else:
        jump_count = jump_height
        make_jump = False   

def draw_user():
    global img_count
    if make_jump == False: 
        if img_count == 8:
            img_count = 0
        display.blit(user_img[img_count // 4], (user_x, user_y))
        img_count += 1
    else:
        display.blit(user_img_jump, (user_x, user_y))

def create_barrier_arr(array):
    choice = random.randrange(0, 3)
    img = barrier_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + jump_height, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = barrier_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = barrier_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))

def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)
    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 280
    else:
        radius = maximum
    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)
    return radius

def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = barrier_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_self(radius, height, width, img)

def open_cloud():
    cloud = Object(display_width, 80, cloud_img.get_rect().width, cloud_img, 2)
    return cloud

def move_cloud(cloud):
    check = cloud.move()
    if not check:
        cloud.return_self(display_width, random.randrange(10, 200), cloud.width, cloud_img)

def print_text(message, x, y, font_color = (115, 115, 115), font_type = r'C:\Users\Evgeny\Desktop\STORAGE\CODE\game_dev\py-rex\assets\PressStart2P-Regular.ttf', font_size = 14):
    font_type = pygame.font.Font(font_type, font_size)
    text  = font_type.render(message, True, font_color)
    display.blit(text, (x, y))

def pause():
    paused = True
    pygame.mixer_music.pause()
    while paused:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
        print_text('Paused. Press \'Enter\' to continue', 160, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()
        clock.tick(15)
    pygame.mixer_music.unpause()
def check_collision(lets):
    for let in lets:
        if let.y == 449:
            if not make_jump:
                if let.x <= user_x + user_width - 35 <= let.x + let.width:
                    return True
            elif jump_count >= 0:
                if user_y + user_height - 5  >= let.y:
                    if let.x <= user_x + user_width - 35 <= let.x + let.width:
                        return True
            else:
                if user_y + user_height - 10  >= let.y:
                    if let.x <= user_x <= let.x + let.width:
                        return True
        else:
            if not make_jump:
                if let.x <= user_x + user_width - 5 <= let.x + let.width:
                    return True
            elif jump_count == 10:
                if user_y + user_height - 5 >= let.y:
                    if let.x <= user_x + user_width - 5 <= let.x + let.width:
                        return True
            elif jump_count >= -1:
                if user_y + user_height - 5 >= let.y:
                    if let.x <= user_x + user_width - 35 <= let.x + let.width:
                        return True
                else:
                    if user_y + user_height - 10  >= let.y:
                        if let.x <= user_x + 5 <= let.x + let.width:
                            return True
    return False

def count_scores(lets):
    global scores, max_above
    above_barrier = 0

    if -jump_height + 10 <= jump_count < jump_height - 5:
        for let in lets:
            if user_y + user_height - 5 <= let.y:
                if let.x <= user_x <= let.x + let.width:                
                    above_barrier += 1
                elif let.x <= user_x + user_width <= let.x + let.width:
                    above_barrier += 1
        max_above = max(max_above, above_barrier)
    else:
        if jump_count == -jump_height:
            scores += max_above
            max_above = 0
def game_over():
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores
    stopped = True
    while stopped:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
        print_text('GAME OVER', 340, 300)
        print_text('Max scores: ' + str(max_scores), 320, 340)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False
        pygame.display.update()
        clock.tick(15)

while run_game():
    scores = 0
    make_jump = False
    jump_count = jump_height
    user_y = platform - user_height
pygame.quit()
quit()