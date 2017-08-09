# classic arcade game Pong
# try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

import os
# from flask import Flask

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

LINE_WIDTH = 2

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]

paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2

paddle1_vel = 0
paddle2_vel = 0

bounce_counter = 0
score1 = 0
score2 = 0

def spawn_ball(direction):
    global ball_pos, ball_vel, bounce_counter # vectors

    bounce_counter = 1
    ball_pos = [WIDTH/2, HEIGHT/2]

    # if direction is RIGHT, the ball's velocity is upper right, else upper left
    if RIGHT:
        ball_vel[0] = random.randrange(120, 240)/70
        ball_vel[1] = -random.randrange(60, 180)/70
    elif not RIGHT:
        ball_vel[0] = -random.randrange(120, 240)/70
        ball_vel[1] = -random.randrange(60, 180)/70


# event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2

    score1 = 0
    score2 = 0

    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, bounce_counter, RIGHT

    # mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White") # mid line
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0] * (1.1 ** bounce_counter)
    ball_pos[1] = ball_pos[1] + ball_vel[1] * (1.1 ** bounce_counter)

    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] + ball_vel[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, LINE_WIDTH, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel - HALF_PAD_HEIGHT) >= 0 and (paddle1_pos + paddle1_vel+ HALF_PAD_HEIGHT) <= HEIGHT:
        paddle1_pos = paddle1_pos + paddle1_vel

    if (paddle2_pos + paddle2_vel - HALF_PAD_HEIGHT) >= 0 and (paddle2_pos + paddle2_vel+ HALF_PAD_HEIGHT) <= HEIGHT:
        paddle2_pos = paddle2_pos + paddle2_vel

    # paddles
    canvas.draw_polygon([[0, paddle1_pos-HALF_PAD_HEIGHT],[PAD_WIDTH, paddle1_pos-HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos+HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT]], LINE_WIDTH, "White", "White")
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT],[WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]], LINE_WIDTH, "White", "White")

    # paddle and ball collide
    if ball_pos[0]- BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] < (paddle1_pos - HALF_PAD_HEIGHT) or ball_pos[1] > (paddle1_pos + HALF_PAD_HEIGHT):
                score2 = score2 + 1
                RIGHT = True
                spawn_ball(RIGHT)
        else:
            bounce_counter = bounce_counter + 1
            ball_vel[0] = - ball_vel[0]

    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] < (paddle2_pos - HALF_PAD_HEIGHT) or ball_pos[1] > (paddle2_pos + HALF_PAD_HEIGHT):
                score1 = score1 + 1
                RIGHT = False
                spawn_ball(RIGHT)
        else:
            bounce_counter = bounce_counter + 1
            ball_vel[0] = - ball_vel[0]

    # scores
    canvas.draw_text(str(score1), (WIDTH*1/4, HEIGHT *1/4), 30, 'White')
    canvas.draw_text(str(score2), (WIDTH*3/4, HEIGHT *1/4), 30, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel

    speed = 5

    if key == simplegui.KEY_MAP['s']:
        paddle1_vel =  + speed
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel =  + speed

    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = - speed

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = - speed

def keyup(key):
    global paddle1_vel, paddle2_vel

    paddle1_vel = 0
    paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game, 80)


# start frame
new_game()
frame.start()
