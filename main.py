import pygame, sys , random
def draw_floor():
    screen.blit(floor,(floor_x_pos,700))
    screen.blit(floor,(floor_x_pos+576,700))
pygame.mixer.pre_init(frequency = 44100, size = 16, channels =1, buffer = 1000)
pygame.init()
screen = pygame.display.set_mode((576,800))
clock = pygame.time.Clock()
game_font = pygame.font.Font("freesansbold.ttf",40)
def create_pipe():
    pipe_heights = random.choice([400,600,500])
    bottom_pipe = pipe_surface.get_rect(midtop = (576,pipe_heights))
    top_pipe = pipe_surface.get_rect(midtop = (576,pipe_heights-600))
    return bottom_pipe,top_pipe
def move_pipes(pipes):
    for pipe in pipes:
        pipe. centerx -= 5
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe  ,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 725:
        death_sound.play()
        return False
    return True
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird =bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect
def score_display(game_state):
    if game_state == "main_game":
        score_surface =game_font.render("Score:"+str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == "game_over":
        score_surface =game_font.render("Score:"+str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        #high_surface =game_font.render("High Score:"+str(int(high_score)),True,(255,255,255))
        #high_rect = high_surface.get_rect(center = (288,600))
        #screen.blit(high_surface,high_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

gravity =0.25
bird_movement = 0
score = 0
high_score = 0
game_active = True
bg_surface = pygame.image.load("Assits/background-day.png").convert()
bg_surface=pygame.transform.scale2x(bg_surface)

floor = pygame.image.load("Assits/base.png").convert()
floor=pygame.transform.scale2x(floor)
floor_x_pos = 0
bird_downflap =pygame.image.load("Assits/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("Assits/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("Assits/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index =0
#bird_surface = pygame.transform.scale2x(bird_surface)
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center =(100,400))

pipe_surface = pygame.image.load("Assits/pipe-green.png").convert()
#pipe_surface = pygame.transform.scale2x(pipe_surface)
game_over_surface = pygame.image.load("Assits/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center =(288,400))

flap_sound = pygame.mixer.Sound("music/sfx_wing.wav")
death_sound = pygame.mixer.Sound("music/sfx_hit.wav")
score_sound = pygame.mixer.Sound("music/sfx_point.wav")
score_sound_countdown = 100
#bg_sound = pygame.mixer.Sound("music/bgm.mp3")
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)
pipe_list = []
SPAWNPIPE =pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12 
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                score = 0
                game_active=True
                pipe_list.clear()
                bird_rect.center = (100,400)
                bird_movement=0
                
        if event.type == SPAWNPIPE:
            pipe_list.extend (create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()

    screen.blit(bg_surface,(0,0))
    if game_active:
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement 
        screen.blit(rotated_bird,bird_rect)
        #game_active = check_collision(pipe_list)
        game_active = check_collision(pipe_list)
        #PIpes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01 
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown=100
    else:
        screen.blit(game_over_surface,game_over_rect)
        highscore = update_score(score,high_score)
        score_display("game_over")


    
    #floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos=0
    #bg_sound.play(-1)
    pygame.display.update()
    clock.tick(120)