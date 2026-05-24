# ============================================================
# ULTRA ADVANCED AI CYBER SHOOTER
# ============================================================

import cv2
import numpy as np
import mediapipe as mp
import random
import math
import time

# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

WIDTH = 1280
HEIGHT = 720

cap.set(3, WIDTH)
cap.set(4, HEIGHT)

# ============================================================
# MEDIAPIPE
# ============================================================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
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

player_x = WIDTH // 2
player_y = HEIGHT - 100

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
slow_motion = 0
laser_mode = 0
screen_shake = 0

boss_mode = False

last_shot = 0
shoot_delay = 0.15

prev_time = time.time()

# ============================================================
# OBJECTS
# ============================================================

bullets = []
enemy_bullets = []
enemies = []
particles = []
powerups = []
damage_numbers = []
stars = []

# ============================================================
# STARFIELD
# ============================================================

for i in range(200):

    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1,3)
    ])

# ============================================================
# BULLET
# ============================================================

class Bullet:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.speed = 25

    def update(self):

        self.y -= self.speed

    def draw(self, frame):

        overlay = frame.copy()

        cv2.line(
            overlay,
            (int(self.x), int(self.y)),
            (int(self.x), int(self.y - 35)),
            CYAN,
            10
        )

        overlay = cv2.GaussianBlur(overlay, (0,0), 10)

        frame[:] = cv2.addWeighted(
            overlay,
            0.5,
            frame,
            0.5,
            0
        )

        cv2.line(
            frame,
            (int(self.x), int(self.y)),
            (int(self.x), int(self.y - 35)),
            WHITE,
            4
        )

# ============================================================
# ENEMY BULLET
# ============================================================

class EnemyBullet:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.speed = 10

    def update(self):

        self.y += self.speed

    def draw(self, frame):

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            10,
            ORANGE,
            -1
        )

# ============================================================
# ENEMY
# ============================================================

class Enemy:

    def __init__(self, boss=False):

        self.boss = boss

        self.x = random.randint(80, WIDTH - 80)
        self.y = -50

        if boss:

            self.radius = 120
            self.hp = 60
            self.speed = 2

        else:

            self.radius = random.randint(25,45)
            self.hp = 1
            self.speed = random.uniform(3,8) + level * 0.5

        self.color = (
            random.randint(100,255),
            0,
            random.randint(100,255)
        )

    def update(self):

        if slow_motion > 0:

            self.y += self.speed * 0.3

        else:

            self.y += self.speed

        if self.boss:

            if random.randint(1,12) == 1:

                enemy_bullets.append(
                    EnemyBullet(self.x, self.y)
                )

    def draw(self, frame):

        overlay = frame.copy()

        cv2.circle(
            overlay,
            (int(self.x), int(self.y)),
            self.radius + 25,
            PURPLE,
            -1
        )

        overlay = cv2.GaussianBlur(overlay, (0,0), 20)

        frame[:] = cv2.addWeighted(
            overlay,
            0.25,
            frame,
            0.75,
            0
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
            self.radius + 10,
            WHITE,
            2
        )

        if self.boss:

            cv2.rectangle(
                frame,
                (int(self.x-80), int(self.y-150)),
                (int(self.x+80), int(self.y-130)),
                WHITE,
                2
            )

            hp_width = int((self.hp / 60) * 160)

            cv2.rectangle(
                frame,
                (int(self.x-80), int(self.y-150)),
                (int(self.x-80 + hp_width), int(self.y-130)),
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

        self.vx = random.uniform(-10,10)
        self.vy = random.uniform(-10,10)

        self.life = random.randint(20,50)

        self.color = color

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.life -= 1

    def draw(self, frame):

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            3,
            self.color,
            -1
        )

# ============================================================
# POWERUP
# ============================================================

class PowerUp:

    def __init__(self):

        self.x = random.randint(50, WIDTH - 50)
        self.y = -50

        self.radius = 25
        self.speed = 5

        self.type = random.choice([
            "shield",
            "heal",
            "slow",
            "laser"
        ])

    def update(self):

        self.y += self.speed

    def draw(self, frame):

        color = GREEN

        if self.type == "shield":
            color = BLUE

        elif self.type == "slow":
            color = PURPLE

        elif self.type == "laser":
            color = CYAN

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            self.radius,
            color,
            -1
        )

# ============================================================
# DAMAGE TEXT
# ============================================================

class DamageText:

    def __init__(self, x, y, text):

        self.x = x
        self.y = y

        self.text = text
        self.life = 30

    def update(self):

        self.y -= 2
        self.life -= 1

    def draw(self, frame):

        cv2.putText(
            frame,
            self.text,
            (int(self.x), int(self.y)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            YELLOW,
            3
        )

# ============================================================
# CYBER GRID
# ============================================================

def draw_grid(frame):

    offset = int(time.time() * 60) % 40

    for x in range(0, WIDTH, 40):

        cv2.line(
            frame,
            (x,0),
            (x,HEIGHT),
            (20,10,40),
            1
        )

    for y in range(-40, HEIGHT, 40):

        y += offset

        cv2.line(
            frame,
            (0,y),
            (WIDTH,y),
            (20,10,40),
            1
        )

# ============================================================
# STARFIELD
# ============================================================

def draw_stars(frame):

    for star in stars:

        star[1] += star[2]

        if star[1] > HEIGHT:

            star[0] = random.randint(0, WIDTH)
            star[1] = 0

        cv2.circle(
            frame,
            (star[0], star[1]),
            star[2],
            WHITE,
            -1
        )

# ============================================================
# MAIN LOOP
# ============================================================

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame,1)

    frame = cv2.resize(frame,(WIDTH,HEIGHT))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ========================================================
    # FPS
    # ========================================================

    fps = int(1 / (time.time() - prev_time))
    prev_time = time.time()

    # ========================================================
    # LEVEL SYSTEM
    # ========================================================

    level = score // 100 + 1

    # ========================================================
    # EFFECTS
    # ========================================================

    draw_grid(frame)
    draw_stars(frame)

    # ========================================================
    # HAND TRACKING
    # ========================================================

    results = hands.process(rgb)

    shoot = False

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            ix = int(index_tip.x * WIDTH)
            iy = int(index_tip.y * HEIGHT)

            tx = int(thumb_tip.x * WIDTH)
            ty = int(thumb_tip.y * HEIGHT)

            smooth_x = int(smooth_x * 0.7 + ix * 0.3)
            smooth_y = int(smooth_y * 0.7 + iy * 0.3)

            player_x = smooth_x
            player_y = smooth_y

            distance = math.sqrt(
                (ix - tx)**2 +
                (iy - ty)**2
            )

            if distance < 40:

                shoot = True

    # ========================================================
    # SHOOT
    # ========================================================

    current_time = time.time()

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

        enemies.append(
            Enemy()
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
    # POWERUPS
    # ========================================================

    if random.randint(1,250) == 1:

        powerups.append(
            PowerUp()
        )

    # ========================================================
    # BULLETS
    # ========================================================

    for bullet in bullets[:]:

        bullet.update()
        bullet.draw(frame)

        if bullet.y < 0:

            bullets.remove(bullet)

    # ========================================================
    # ENEMY BULLETS
    # ========================================================

    for eb in enemy_bullets[:]:

        eb.update()
        eb.draw(frame)

        dist = math.sqrt(
            (eb.x-player_x)**2 +
            (eb.y-player_y)**2
        )

        if dist < 30:

            if shield <= 0:

                health -= 5

            enemy_bullets.remove(eb)

    # ========================================================
    # ENEMIES
    # ========================================================

    for enemy in enemies[:]:

        enemy.update()
        enemy.draw(frame)

        dist_player = math.sqrt(
            (enemy.x-player_x)**2 +
            (enemy.y-player_y)**2
        )

        if dist_player < enemy.radius + 25:

            if shield <= 0:

                health -= 15

            screen_shake = 15

            enemies.remove(enemy)

            continue

        for bullet in bullets[:]:

            dist = math.sqrt(
                (enemy.x-bullet.x)**2 +
                (enemy.y-bullet.y)**2
            )

            if dist < enemy.radius:

                enemy.hp -= 1

                screen_shake = 5

                for i in range(30):

                    particles.append(
                        Particle(enemy.x, enemy.y, CYAN)
                    )

                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy.hp <= 0:

                    if enemy.boss:

                        score += 300
                        boss_mode = False

                    else:

                        score += 10 * max(1, combo // 5)

                    combo += 1

                    damage_numbers.append(
                        DamageText(enemy.x, enemy.y, "+10")
                    )

                    if enemy in enemies:
                        enemies.remove(enemy)

                break

    # ========================================================
    # POWERUPS
    # ========================================================

    for p in powerups[:]:

        p.update()
        p.draw(frame)

        dist = math.sqrt(
            (p.x-player_x)**2 +
            (p.y-player_y)**2
        )

        if dist < p.radius + 25:

            if p.type == "heal":
                health = min(100, health + 30)

            elif p.type == "shield":
                shield = 300

            elif p.type == "slow":
                slow_motion = 300

            elif p.type == "laser":
                laser_mode = 300

            powerups.remove(p)

    # ========================================================
    # PARTICLES
    # ========================================================

    for particle in particles[:]:

        particle.update()
        particle.draw(frame)

        if particle.life <= 0:

            particles.remove(particle)

    # ========================================================
    # DAMAGE TEXT
    # ========================================================

    for dmg in damage_numbers[:]:

        dmg.update()
        dmg.draw(frame)

        if dmg.life <= 0:

            damage_numbers.remove(dmg)

    # ========================================================
    # TIMERS
    # ========================================================

    if shield > 0:

        shield -= 1

        cv2.circle(
            frame,
            (player_x, player_y),
            60,
            BLUE,
            3
        )

    if slow_motion > 0:
        slow_motion -= 1

    if laser_mode > 0:
        laser_mode -= 1

    # ========================================================
    # PLAYER GLOW
    # ========================================================

    overlay = frame.copy()

    cv2.circle(
        overlay,
        (player_x, player_y),
        70,
        CYAN,
        -1
    )

    overlay = cv2.GaussianBlur(overlay, (0,0), 25)

    frame = cv2.addWeighted(
        overlay,
        0.25,
        frame,
        0.75,
        0
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
        3
    )

    # ========================================================
    # SCREEN SHAKE
    # ========================================================

    if screen_shake > 0:

        dx = random.randint(-screen_shake, screen_shake)
        dy = random.randint(-screen_shake, screen_shake)

        M = np.float32([[1,0,dx],[0,1,dy]])

        frame = cv2.warpAffine(frame, M, (WIDTH, HEIGHT))

        screen_shake -= 1

    # ========================================================
    # HEALTH BAR
    # ========================================================

    cv2.rectangle(frame, (20,20), (320,45), WHITE, 2)

    cv2.rectangle(
        frame,
        (20,20),
        (20 + int(health * 3),45),
        GREEN,
        -1
    )

    # ========================================================
    # HUD
    # ========================================================

    cv2.putText(
        frame,
        f"SCORE : {score}",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        WHITE,
        2
    )

    cv2.putText(
        frame,
        f"COMBO : {combo}",
        (20,120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        YELLOW,
        2
    )

    cv2.putText(
        frame,
        f"LEVEL : {level}",
        (20,160),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        CYAN,
        2
    )

    cv2.putText(
        frame,
        f"FPS : {fps}",
        (20,200),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        GREEN,
        2
    )

    # ========================================================
    # POWER STATUS
    # ========================================================

    if laser_mode > 0:

        cv2.putText(
            frame,
            "LASER MODE",
            (900,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            CYAN,
            3
        )

    if slow_motion > 0:

        cv2.putText(
            frame,
            "SLOW MOTION",
            (850,100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            PURPLE,
            3
        )

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

        cv2.putText(
            frame,
            f"FINAL SCORE : {score}",
            (420,430),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            WHITE,
            3
        )

        cv2.imshow("ULTRA AI CYBER SHOOTER", frame)

        cv2.waitKey(4000)

        break

    # ========================================================
    # SHOW
    # ========================================================

    cv2.imshow("ULTRA AI CYBER SHOOTER", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ============================================================
# EXIT
# ============================================================

print("FINAL SCORE:", score)

cap.release()
cv2.destroyAllWindows()
