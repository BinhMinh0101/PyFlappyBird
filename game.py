from asyncio.windows_utils import pipe
import pygame as pg
import sys
import random


def draw_floor():  # set kich thuoc background + floor
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos+432, 650))


def creat_pipe():  # set kich thuoc khối cột
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(400, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(400, random_pipe_pos-750))
    return bottom_pipe, top_pipe


def move_pipe(pipes):  # dùng để di chuyển cột
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):  # vẽ cột
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pg.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):  # kiểm tra kích thước của cột bị lấn ra màn hình game kh
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        hit_sound.play()
        return False
    return True


def rotate_bird(bird1):
    new_bird = pg.transform.rotozoom(bird1, -bird_movement*3, 1)
    return new_bird


def bird_animation():  # trả về hình ảnh chim + kích thước
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):  # điểm số bắt đầu của game
    if game_state == 'main game':
        score_surface = game_font.render(
            str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):  # cập nhật điểm số cao nhất
    if score > high_score:
        high_score = score
    return high_score


pg.mixer.pre_init(frequency=44100, size=-16, channels=2,
                  buffer=512)  # sét âm thanh cho game
pg.init()  # hàm khởi động game
screen = pg.display.set_mode((432, 768))  # sét kích thước màn hình
clock = pg.time.Clock()  # Set FPS cho game
game_font = pg.font.Font('04B_19.ttf', 40)  # Font chu
gravity = 0.25  # trọng lực bật của bird
bird_movement = 0  # chuyển động của bird
game_active = True  # điều kiện đúng của game
score = 0  # khởi tạo biến lưu điểm
high_score = 0  # điểm cao nhất
# Chen background
bg = pg.image.load('assests/background-night.png').convert()
bg = pg.transform.scale2x(bg)  # X2 background
# chen footer
floor = pg.image.load('assests/floor.png').convert()  # background footer
floor = pg.transform.scale2x(floor)
floor_x_pos = 0
# bird 3 thạng thái bên dưới
bird_down = pg.transform.scale2x(pg.image.load(
    'assests/yellowbird-downflap.png').convert_alpha())  # trạng thái cánh chim cụp xuống
bird_mid = pg.transform.scale2x(pg.image.load(
    'assests/yellowbird-midflap.png').convert_alpha())  # trạng thái cánh chim nằm thẳng
bird_up = pg.transform.scale2x(pg.image.load(
    'assests/yellowbird-upflap.png').convert_alpha())  # trạng thái cánh chim bay lên
# 0 1 2 danh sách trạng thái của chim để dùng vào vòng lặp
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
''' bird = pg.transform.scale2x(bird) '''
bird_rect = bird.get_rect(center=(
    30, 100))  # tạo ô vuông xung quanh bao bọc con chim, nếu đụng vào cột thì game over
birdflap = pg.USEREVENT + 1  # userevent nhận định đối tượng
pg.time.set_timer(birdflap, 200)  # tao timer cho bird
# convert là giải nén hình ảnh thấp xuống để mượt hơn
pipe_surface = pg.image.load('assests/pipe-green.png').convert()
pipe_surface = pg.transform.scale2x(pipe_surface)
pipe_list = []
# tao timer
spawpipe = pg.USEREVENT
pg.time.set_timer(spawpipe, 1400)  # sau 1.4s tao ong moi
# danh sách kích thước ống để random vào trò chơi
pipe_height = [300, 400, 500]
# Tao man hinh ket thuc
game_over_surface = pg.transform.scale2x(
    pg.image.load('assests/message.png').convert_alpha())
# kích thước màn hình khi kết thúc game căn giữa
game_over_rect = game_over_surface.get_rect(center=(216, 384))
# Chen am thanh
flap_sound = pg.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pg.mixer.Sound('sound/sfx_hit.wav')
score_sound = pg.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100  # đếm ngược âm thanh game khi va chạm ( 0.1s)
# while loop cua tro choi, mục đích duy trì màn hình game
while True:
    pg.time.delay(13)
    for event in pg.event.get():  # lay su kien pygame dien ra
        if event.type == pg.QUIT:  # điều kiện, nếu nhấn dấu X sẽ out game
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:  # điều kiện điều khiển bird, nhấn cách để điều khiển
            if event.key == pg.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -7
                flap_sound.play()  # chạy âm thanh game
            if event.key == pg.K_SPACE and game_active == False:  # điều kiện sử lý va chạm
                game_active = True
                pipe_list.clear()  # clear đi để chèn background thua vào
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawpipe:  # nếu bird đang bay, thì ống mới liên tiếp được chạy
            pipe_list.extend(creat_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))  # them background vao game
    if game_active:
        # bird
        bird_movement += gravity  # tao trong luc cho bird
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # pape
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:  # lưu lại điểm số cao nhất khi game over
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game over')

    # floor
    floor_x_pos -= 1
    draw_floor()  # footer hiển thị chạy bên dưới
    if floor_x_pos <= -432:  # nếu footer bé hơn màn hình game thì được phép chèn vô, ko thì ko đc
        floor_x_pos = 0

    # cập nhật dữ liệu của game, như điểm số cao nhất, màn hình về nguyên trạng
    pg.display.update()
    clock.tick(120)  # fps
