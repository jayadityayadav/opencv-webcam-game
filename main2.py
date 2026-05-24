# ============================================================
# NEXUS VOID
# ULTRA ADVANCED HAND CONTROLLED CYBERPUNK SHOOTER
# ============================================================

import cv2
import numpy as np
import mediapipe as mp
import random
import math
import time

# ============================================================
# OPTIMIZATION
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

cap.set(3, CAM_W)
cap.set(4, CAM_H)

# ============================================================
# MEDIAPIPE
# ============================================================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65
)

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

trail_points = []

# ============================================================
# GAME VARIABLES
# ============================================================

score = 0
health = 100
combo = 0
level = 1

boss_mode = False

laser_mode = 0
shield = 0
slow_motion = 0

screen_flash = 0
screen_shake = 0

frame_count = 0

last_shot = 0
shoot_delay = 0.12

charge_start = None
charge_power = 0

ultimate_ready = False
ultimate_energy = 0

prev_time = time.time()
last_time = time.time()

# ============================================================
# OBJECTS
# ============================================================

bullets = []
enemies = []
particles = []
shockwaves = []
stars = []

# ============================================================
# STARS
# ============================================================

for i in range(150):

    stars.append([
        random.randint(0, GAME_W),
        random.randint(0, GAME_H),
        random.randint(1,3)
    ])

# ============================================================
# BULLET
# ============================================================

class Bullet:

    def __init__(self, x, y, power=1):

        self.x = x
        self.y = y

        self.power = power

        self.speed = 1800

        self.radius = 6 + power * 2

    def update(self, dt):

        self.y -= self.speed * dt

    def draw(self, frame, glow):

        color = CYAN

        if self.power >= 3:
            color = ORANGE

        cv2.circle(
            glow,
            (int(self.x), int(self.y)),
            self.radius + 12,
            color,
            -1
        )

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            self.radius,
            WHITE,
            -1
        )

# ============================================================
# ENEMY
# ============================================================

class Enemy:

    def __init__(self, enemy_type="normal", boss=False):

        self.type = enemy_type

        self.boss = boss

        self.x = random.randint(80, GAME_W - 80)
        self.y = -100

        self.angle = 0

        if boss:

            self.radius = 120
            self.hp = 150
            self.speed = 140

        else:

            if enemy_type == "fast":

                self.radius = 20
                self.hp = 1
                self.speed = 500

            elif enemy_type == "tank":

                self.radius = 55
                self.hp = 8
                self.speed = 120

            elif enemy_type == "zigzag":

                self.radius = 35
                self.hp = 2
                self.speed = 250

            else:

                self.radius = 30
                self.hp = 1
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

            self.y += self.speed * dt * 0.35

        else:

            self.y += self.speed * dt

    def draw(self, frame, glow):

        cv2.circle(
            glow,
            (int(self.x), int(self.y)),
            self.radius + 18,
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
            self.radius + 4,
            WHITE,
            2
        )

        if self.boss:

            cv2.rectangle(
                frame,
                (int(self.x-100), int(self.y-170)),
                (int(self.x+100), int(self.y-140)),
                WHITE,
                2
            )

            hp_width = int((self.hp / 150) * 200)

            cv2.rectangle(
                frame,
                (int(self.x-100), int(self.y-170)),
                (int(self.x-100 + hp_width), int(self.y-140)),
                RED,
                -1
            )

# ============================================================
# PARTICLES
# ============================================================

class Particle:

    def __init__(self, x, y, color):

        self.x = x
        self.y = y

        self.vx = random.uniform(-500,500)
        self.vy = random.uniform(-500,500)

        self.life = random.randint(15,40)

        self.size = random.randint(2,5)

        self.color = color

    def update(self, dt):

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.vx *= 0.95
        self.vy *= 0.95

        self.life -= 1

    def draw(self, frame):

        alpha = max(0, self.life / 40)

        color = (
            int(self.color[0] * alpha),
            int(self.color[1] * alpha),
            int(self.color[2] * alpha)
        )

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            self.size,
            color,
            -1
        )

# ============================================================
# SHOCKWAVE
# ============================================================

class Shockwave:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.radius = 10
        self.life = 20

    def update(self):

        self.radius += 15
        self.life -= 1

    def draw(self, frame):

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            int(self.radius),
            CYAN,
            3
        )

# ============================================================
# BACKGROUND
# ============================================================

def draw_background(frame, dt):

    offset = int(time.time() * 100) % 40

    for x in range(0, GAME_W, 40):

        cv2.line(
            frame,
            (x,0),
            (x,GAME_H),
            (15,8,30),
            1
        )

    for y in range(-40, GAME_H, 40):

        y += offset

        cv2.line(
            frame,
            (0,y),
            (GAME_W,y),
            (15,8,30),
            1
        )

    for star in stars:

        star[1] += star[2] * 140 * dt

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

    frame_count += 1

    # ========================================================
    # SURFACES
    # ========================================================

    frame = np.zeros((GAME_H, GAME_W, 3), dtype=np.uint8)

    glow = np.zeros_like(frame)

    ui = np.zeros_like(frame)

    # ========================================================
    # FPS
    # ========================================================

    fps = int(1 / max(dt, 0.001))

    # ========================================================
    # LEVEL
    # ========================================================

    level = score // 100 + 1

    # ========================================================
    # BACKGROUND
    # ========================================================

    draw_background(frame, dt)

    # ========================================================
    # HAND TRACKING
    # ========================================================

    shoot = False

    if frame_count % 2 == 0:

        rgb = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                index_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]

                ix = int(index_tip.x * GAME_W)
                iy = int(index_tip.y * GAME_H)

                tx = int(thumb_tip.x * GAME_W)
                ty = int(thumb_tip.y * GAME_H)

                smooth_x = int(smooth_x * 0.8 + ix * 0.2)
                smooth_y = int(smooth_y * 0.8 + iy * 0.2)

                player_x = smooth_x
                player_y = smooth_y

                distance = math.hypot(ix - tx, iy - ty)

                # ====================================================
                # CHARGE SYSTEM
                # ====================================================

                if distance < 45:

                    if charge_start is None:

                        charge_start = time.time()

                    charge_power = min(
                        5,
                        int((time.time() - charge_start) * 5)
                    )

                    shoot = True

                else:

                    charge_start = None
                    charge_power = 1

    # ========================================================
    # SHOOT
    # ========================================================

    if shoot and current_time - last_shot > shoot_delay:

        bullets.append(
            Bullet(
                player_x,
                player_y,
                max(1, charge_power)
            )
        )

        if laser_mode > 0:

            bullets.append(
                Bullet(player_x - 25, player_y, charge_power)
            )

            bullets.append(
                Bullet(player_x + 25, player_y, charge_power)
            )

        last_shot = current_time

    # ========================================================
    # ENEMY SPAWN
    # ========================================================

    if random.randint(1, max(4, 22-level)) == 1:

        enemy_type = random.choice([
            "normal",
            "fast",
            "tank",
            "zigzag"
        ])

        enemies.append(
            Enemy(enemy_type)
        )

    # ========================================================
    # BOSS
    # ========================================================

    if score > 0 and score % 700 == 0 and not boss_mode:

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
            screen_shake = 10

            shockwaves.append(
                Shockwave(player_x, player_y)
            )

            enemies.remove(enemy)

            continue

        for bullet in bullets[:]:

            dist = math.hypot(
                enemy.x-bullet.x,
                enemy.y-bullet.y
            )

            if dist < enemy.radius:

                enemy.hp -= bullet.power

                screen_flash = 0.12
                screen_shake = 5

                ultimate_energy += 1

                shockwaves.append(
                    Shockwave(enemy.x, enemy.y)
                )

                for i in range(18):

                    particles.append(
                        Particle(enemy.x, enemy.y, CYAN)
                    )

                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy.hp <= 0:

                    if enemy.boss:

                        score += 700
                        boss_mode = False

                    else:

                        score += 10

                    combo += 1

                    for i in range(40):

                        particles.append(
                            Particle(enemy.x, enemy.y, ORANGE)
                        )

                    enemies.remove(enemy)

                break

    # ========================================================
    # SHOCKWAVES
    # ========================================================

    for shockwave in shockwaves[:]:

        shockwave.update()

        shockwave.draw(frame)

        if shockwave.life <= 0:

            shockwaves.remove(shockwave)

    # ========================================================
    # PARTICLES
    # ========================================================

    for particle in particles[:]:

        particle.update(dt)

        particle.draw(frame)

        if particle.life <= 0:

            particles.remove(particle)

    # ========================================================
    # PLAYER TRAIL
    # ========================================================

    trail_points.append((player_x, player_y))

    if len(trail_points) > 15:

        trail_points.pop(0)

    for i in range(1, len(trail_points)):

        alpha = i / len(trail_points)

        thickness = int(10 * alpha)

        cv2.line(
            glow,
            trail_points[i-1],
            trail_points[i],
            CYAN,
            thickness
        )

    # ========================================================
    # PLAYER
    # ========================================================

    cv2.circle(
        glow,
        (player_x, player_y),
        70,
        CYAN,
        -1
    )

    cv2.circle(
        frame,
        (player_x, player_y),
        30,
        CYAN,
        -1
    )

    cv2.circle(
        frame,
        (player_x, player_y),
        50,
        WHITE,
        2
    )

    # ========================================================
    # GLOW PASS
    # ========================================================

    glow = cv2.GaussianBlur(glow, (0,0), 12)

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

        screen_flash *= 0.88

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
    # ULTIMATE BAR
    # ========================================================

    ultimate_energy = min(100, ultimate_energy)

    cv2.rectangle(
        ui,
        (20,60),
        (320,85),
        WHITE,
        2
    )

    cv2.rectangle(
        ui,
        (20,60),
        (20 + int(ultimate_energy * 3),85),
        CYAN,
        -1
    )

    # ========================================================
    # HUD
    # ========================================================

    cv2.putText(
        ui,
        f"SCORE : {score}",
        (20,130),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        WHITE,
        2
    )

    cv2.putText(
        ui,
        f"LEVEL : {level}",
        (20,180),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        CYAN,
        2
    )

    cv2.putText(
        ui,
        f"FPS : {fps}",
        (20,230),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        GREEN,
        2
    )

    cv2.putText(
        ui,
        f"COMBO : {combo}",
        (20,280),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        YELLOW,
        2
    )

    cv2.putText(
        ui,
        f"CHARGE : {charge_power}",
        (20,330),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        ORANGE,
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

        cv2.imshow("NEXUS VOID", frame)

        cv2.waitKey(4000)

        break

    # ========================================================
    # SHOW
    # ========================================================

    cv2.imshow("NEXUS VOID", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ============================================================
# EXIT
# ============================================================

print("FINAL SCORE:", score)

cap.release()

cv2.destroyAllWindows()
