# ============================================================
# ULTRA ADVANCED AI CYBER SHOOTER ENGINE
# PROFESSIONAL OPTIMIZED VERSION
# ============================================================

import cv2
import numpy as np
import mediapipe as mp
import random
import math
import time

# ============================================================
# OPENCV OPTIMIZATION
# ============================================================

cv2.setUseOptimized(True)
cv2.ocl.setUseOpenCL(True)

# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

CAM_W = 320
CAM_H = 240

GAME_W = 1280
GAME_H = 720

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)

# ============================================================
# MEDIAPIPE
# ============================================================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65
)

mp_draw = mp.solutions.drawing_utils

# ============================================================
# COLORS
# ============================================================

CYAN = (255,255,0)
PURPLE = (255,0,255)
RED = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
YELLOW = (0,255,255)
BLUE = (255,0,0)
ORANGE = (0,165,255)

# ============================================================
# PLAYER
# ============================================================

player_x = GAME_W // 2
player_y = GAME_H - 120

smooth_x = player_x
smooth_y = player_y

# ============================================================
# GAME VARIABLES
# ============================================================

score = 0
health = 100
combo = 0
level = 1

shield = 0
laser_mode = 0
slow_motion = 0

boss_mode = False

last_shot = 0
shoot_delay = 0.12

frame_count = 0

prev_time = time.time()
last_time = time.time()

screen_flash = 0
screen_shake = 0

# ============================================================
# OBJECTS
# ============================================================

bullets = []
enemies = []
particles = []
stars = []

# ============================================================
# STARFIELD
# ============================================================

for i in range(120):

    stars.append([
        random.randint(0, GAME_W),
        random.randint(0, GAME_H),
        random.randint(1,3)
    ])

# ============================================================
# BULLET
# ============================================================

class Bullet:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.speed = 1500

    def update(self, dt):

        self.y -= self.speed * dt

    def draw(self, frame, glow):

        cv2.line(
            frame,
            (int(self.x), int(self.y)),
            (int(self.x), int(self.y - 20)),
            WHITE,
            3
        )

        cv2.line(
            glow,
            (int(self.x), int(self.y)),
            (int(self.x), int(self.y - 20)),
            CYAN,
            8
        )

# ============================================================
# ENEMY
# ============================================================

class Enemy:

    def __init__(self, enemy_type="normal", boss=False):

        self.type = enemy_type

        self.boss = boss

        self.x = random.randint(80, GAME_W - 80)

        self.y = -50

        self.angle = 0

        if boss:

            self.radius = 120
            self.hp = 100
            self.speed = 120

        else:

            self.radius = random.randint(20,45)
            self.hp = 1

            if enemy_type == "fast":
                self.speed = 420

            elif enemy_type == "zigzag":
                self.speed = 260

            else:
                self.speed = 220

        self.color = (
            random.randint(100,255),
            0,
            random.randint(100,255)
        )

    def update(self, dt):

        self.angle += 0.05

        if self.type == "zigzag":

            self.x += math.sin(self.angle * 5) * 8

        if slow_motion > 0:

            self.y += self.speed * dt * 0.3

        else:

            self.y += self.speed * dt

    def draw(self, frame, glow):

        cv2.circle(
            glow,
            (int(self.x), int(self.y)),
            self.radius + 20,
            PURPLE,
            -1
        )

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            self.radius,
            self.color,
            -1
        )

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            self.radius + 5,
            WHITE,
            2
        )

        if self.boss:

            cv2.rectangle(
                frame,
                (int(self.x-80), int(self.y-160)),
                (int(self.x+80), int(self.y-135)),
                WHITE,
                2
            )

            hp_width = int((self.hp / 100) * 160)

            cv2.rectangle(
                frame,
                (int(self.x-80), int(self.y-160)),
                (int(self.x-80 + hp_width), int(self.y-135)),
                RED,
                -1
            )

# ============================================================
# PARTICLES
# ============================================================

class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.vx = random.uniform(-300,300)
        self.vy = random.uniform(-300,300)

        self.life = random.randint(15,30)

        self.size = random.randint(2,4)

    def update(self, dt):

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.vx *= 0.96
        self.vy *= 0.96

        self.life -= 1

    def draw(self, frame):

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            self.size,
            CYAN,
            -1
        )

# ============================================================
# STARS
# ============================================================

def draw_stars(frame, dt):

    for star in stars:

        star[1] += star[2] * 120 * dt

        if star[1] > GAME_H:

            star[0] = random.randint(0, GAME_W)
            star[1] = 0

        cv2.circle(
            frame,
            (int(star[0]), int(star[1])),
            star[2],
            WHITE,
            -1
        )

# ============================================================
# CYBER GRID
# ============================================================

def draw_grid(frame):

    offset = int(time.time() * 80) % 40

    for x in range(0, GAME_W, 40):

        cv2.line(
            frame,
            (x,0),
            (x,GAME_H),
            (20,10,40),
            1
        )

    for y in range(-40, GAME_H, 40):

        y += offset

        cv2.line(
            frame,
            (0,y),
            (GAME_W,y),
            (20,10,40),
            1
        )

# ============================================================
# MAIN LOOP
# ============================================================

while True:

    current_time = time.time()

    dt = current_time - last_time

    last_time = current_time

    success, cam = cap.read()

    if not success:
        break

    cam = cv2.flip(cam,1)

    # ========================================================
    # SURFACES
    # ========================================================

    frame = np.zeros((GAME_H, GAME_W, 3), dtype=np.uint8)

    glow = np.zeros_like(frame)

    ui = np.zeros_like(frame)

    frame_count += 1

    # ========================================================
    # FPS
    # ========================================================

    fps = int(1 / max(dt, 0.0001))

    # ========================================================
    # LEVEL
    # ========================================================

    level = score // 100 + 1

    # ========================================================
    # BACKGROUND
    # ========================================================

    draw_grid(frame)

    draw_stars(frame, dt)

    # ========================================================
    # HAND TRACKING
    # ========================================================

    shoot = False

    if frame_count % 2 == 0:

        rgb = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    cam,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                index_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]

                ix = int(index_tip.x * GAME_W)
                iy = int(index_tip.y * GAME_H)

                tx = int(thumb_tip.x * GAME_W)
                ty = int(thumb_tip.y * GAME_H)

                smooth_x = int(smooth_x * 0.75 + ix * 0.25)
                smooth_y = int(smooth_y * 0.75 + iy * 0.25)

                player_x = smooth_x
                player_y = smooth_y

                distance = math.hypot(ix - tx, iy - ty)

                if distance < 40:

                    shoot = True

    # ========================================================
    # SHOOT
    # ========================================================

    if shoot and current_time - last_shot > shoot_delay:

        bullets.append(
            Bullet(player_x, player_y)
        )

        if laser_mode > 0:

            bullets.append(
                Bullet(player_x - 25, player_y)
            )

            bullets.append(
                Bullet(player_x + 25, player_y)
            )

        last_shot = current_time

    # ========================================================
    # ENEMY SPAWN
    # ========================================================

    if random.randint(1, max(4, 20-level)) == 1:

        enemy_type = random.choice([
            "normal",
            "fast",
            "zigzag"
        ])

        enemies.append(
            Enemy(enemy_type)
        )

    # ========================================================
    # BOSS
    # ========================================================

    if score > 0 and score % 500 == 0 and not boss_mode:

        enemies.append(
            Enemy(boss=True)
        )

        boss_mode = True

    # ========================================================
    # BULLETS
    # ========================================================

    for bullet in bullets[:]:

        bullet.update(dt)

        bullet.draw(frame, glow)

        if bullet.y < 0:

            bullets.remove(bullet)

    # ========================================================
    # ENEMIES
    # ========================================================

    for enemy in enemies[:]:

        enemy.update(dt)

        enemy.draw(frame, glow)

        dist_player = math.hypot(
            enemy.x-player_x,
            enemy.y-player_y
        )

        if dist_player < enemy.radius + 30:

            health -= 10

            screen_flash = 0.5
            screen_shake = 8

            enemies.remove(enemy)

            continue

        for bullet in bullets[:]:

            dist = math.hypot(
                enemy.x-bullet.x,
                enemy.y-bullet.y
            )

            if dist < enemy.radius:

                enemy.hp -= 1

                screen_flash = 0.15
                screen_shake = 4

                for i in range(12):

                    particles.append(
                        Particle(enemy.x, enemy.y)
                    )

                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy.hp <= 0:

                    if enemy.boss:

                        score += 500
                        boss_mode = False

                    else:

                        score += 10

                    combo += 1

                    enemies.remove(enemy)

                break

    # ========================================================
    # PARTICLES
    # ========================================================

    for particle in particles[:]:

        particle.update(dt)

        particle.draw(frame)

        if particle.life <= 0:

            particles.remove(particle)

    # ========================================================
    # PLAYER
    # ========================================================

    cv2.circle(
        glow,
        (player_x, player_y),
        60,
        CYAN,
        -1
    )

    cv2.circle(
        frame,
        (player_x, player_y),
        28,
        CYAN,
        -1
    )

    cv2.circle(
        frame,
        (player_x, player_y),
        45,
        WHITE,
        2
    )

    # ========================================================
    # GLOW PASS
    # ========================================================

    glow = cv2.GaussianBlur(glow, (0,0), 10)

    frame = cv2.addWeighted(
        frame,
        1,
        glow,
        0.45,
        0
    )

    # ========================================================
    # SCREEN SHAKE
    # ========================================================

    if screen_shake > 0:

        dx = random.randint(-screen_shake, screen_shake)
        dy = random.randint(-screen_shake, screen_shake)

        frame = np.roll(frame, dx, axis=1)
        frame = np.roll(frame, dy, axis=0)

        screen_shake -= 1

    # ========================================================
    # SCREEN FLASH
    # ========================================================

    if screen_flash > 0:

        white = np.full(frame.shape, 255, dtype=np.uint8)

        frame = cv2.addWeighted(
            frame,
            1-screen_flash,
            white,
            screen_flash,
            0
        )

        screen_flash *= 0.85

    # ========================================================
    # HEALTH BAR
    # ========================================================

    cv2.rectangle(
        ui,
        (20,20),
        (320,45),
        WHITE,
        2
    )

    cv2.rectangle(
        ui,
        (20,20),
        (20 + int(health * 3),45),
        GREEN,
        -1
    )

    # ========================================================
    # HUD
    # ========================================================

    cv2.putText(
        ui,
        f"SCORE : {score}",
        (20,90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        WHITE,
        2
    )

    cv2.putText(
        ui,
        f"LEVEL : {level}",
        (20,140),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        CYAN,
        2
    )

    cv2.putText(
        ui,
        f"FPS : {fps}",
        (20,190),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        GREEN,
        2
    )

    cv2.putText(
        ui,
        f"COMBO : {combo}",
        (20,240),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        YELLOW,
        2
    )

    # ========================================================
    # CAMERA WINDOW
    # ========================================================

    cam = cv2.resize(cam, (320,240))

    frame[20:260, GAME_W-340:GAME_W-20] = cam

    cv2.rectangle(
        frame,
        (GAME_W-340,20),
        (GAME_W-20,260),
        CYAN,
        2
    )

    # ========================================================
    # FINAL COMPOSITE
    # ========================================================

    frame = cv2.addWeighted(frame, 1, ui, 1, 0)

    # ========================================================
    # GAME OVER
    # ========================================================

    if health <= 0:

        cv2.putText(
            frame,
            "GAME OVER",
            (350,350),
            cv2.FONT_HERSHEY_SIMPLEX,
            3,
            RED,
            6
        )

        cv2.imshow(
            "ULTRA ADVANCED AI CYBER SHOOTER",
            frame
        )

        cv2.waitKey(4000)

        break

    # ========================================================
    # SHOW
    # ========================================================

    cv2.imshow(
        "ULTRA ADVANCED AI CYBER SHOOTER",
        frame
    )

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ============================================================
# EXIT
# ============================================================

print("FINAL SCORE:", score)

cap.release()

cv2.destroyAllWindows()
