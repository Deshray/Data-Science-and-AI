import pygame
import random
import pickle
import os
import numpy as np

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
BALL_SIZE = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
PADDLE_SPEED = 6
FPS = 60
STATE_BUCKETS = 12  # Finer resolution slows down learning, enables tactics

# RL constants
ACTIONS = ["UP", "DOWN", "STAY"]
EPSILON_START = 0.6 #Random action probability at the start
EPSILON_MIN = 0.05 #Minimum random action probability
EPSILON_DECAY = 0.992 #Decay rate for epsilon
ALPHA = 0.1 #Learning rate
GAMMA = 0.98 #Discount factor for future rewards (How much they matter)

# Ball speed control
BALL_SPEED_BASE = 2.0
BALL_SPEED_INCREMENT = 0.2
PADDLE_HIT_MARGIN = 12

class QLearningAgent:
    def __init__(self, name):
        self.name = name
        self.q_table = self.load_q_table()
        self.epsilon = EPSILON_START

    def discretize(self, ball_x, ball_y, ball_dx, ball_dy, paddle_y): # Convert continuous state to discrete buckets by splitting screen into 12x12 grid
        bx = int(ball_x * STATE_BUCKETS / SCREEN_WIDTH)
        by = int(ball_y * STATE_BUCKETS / SCREEN_HEIGHT)
        py = int(paddle_y * STATE_BUCKETS / SCREEN_HEIGHT)
        dx = 1 if ball_dx > 0 else 0
        dy = 1 if ball_dy > 0 else 0
        return (bx, by, dx, dy, py)

    def choose_action(self, state): # Choose
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)
        q_vals = [self.q_table.get((state, a), 0.0) for a in ACTIONS]
        return ACTIONS[np.argmax(q_vals)]

    def learn(self, state, action, reward, next_state): #
        old_q = self.q_table.get((state, action), 0.0)
        future_q = max([self.q_table.get((next_state, a), 0.0) for a in ACTIONS])
        self.q_table[(state, action)] = old_q + ALPHA * (reward + GAMMA * future_q - old_q)

    def save_q_table(self):
        with open(f"{self.name}_q.pkl", "wb") as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self):
        if os.path.exists(f"{self.name}_q.pkl"):
            with open(f"{self.name}_q.pkl", "rb") as f:
                return pickle.load(f)
        return {}

    def decay_epsilon(self):
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RL Pong")
        self.clock = pygame.time.Clock()

        self.ball = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, BALL_SIZE, BALL_SIZE)
        self.paddle_left = pygame.Rect(30, SCREEN_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle_right = pygame.Rect(SCREEN_WIDTH-40, SCREEN_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

        self.ball_dx, self.ball_dy = 0, 0

        self.agent_L = QLearningAgent("left")
        self.agent_R = QLearningAgent("right")

        self.episode = 0
        self.reset()

    def reset(self):
        self.ball.x, self.ball.y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
        self.ball_dx = BALL_SPEED_BASE * random.choice([-1, 1])
        self.ball_dy = BALL_SPEED_BASE * random.uniform(-1, 1)
        self.paddle_left.y = SCREEN_HEIGHT//2
        self.paddle_right.y = SCREEN_HEIGHT//2

    def move_paddle(self, paddle, action):
        if action == "UP":
            paddle.y -= PADDLE_SPEED
        elif action == "DOWN":
            paddle.y += PADDLE_SPEED
        paddle.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddle.y))

    def is_edge_hit(self, ball, paddle):
        return abs(ball.centery - paddle.centery) > (PADDLE_HEIGHT // 2 - PADDLE_HIT_MARGIN)

    def directional_reward(self, ball_y, paddle_y, action):
        if action == "UP" and ball_y < paddle_y:
            return 0.03
        elif action == "DOWN" and ball_y > paddle_y:
            return 0.03
        elif action == "STAY" and abs(ball_y - paddle_y) < 10:
            return 0.01
        return -0.01

    def step(self):
        self.ball.x += self.ball_dx
        self.ball.y += self.ball_dy

        if self.ball.top <= 0 or self.ball.bottom >= SCREEN_HEIGHT:
            self.ball_dy *= -1

        hit_left = self.ball.colliderect(self.paddle_left)
        hit_right = self.ball.colliderect(self.paddle_right)

        left_state = self.agent_L.discretize(self.ball.x, self.ball.y, self.ball_dx, self.ball_dy, self.paddle_left.y)
        right_state = self.agent_R.discretize(self.ball.x, self.ball.y, self.ball_dx, self.ball_dy, self.paddle_right.y)

        left_action = self.agent_L.choose_action(left_state)
        right_action = self.agent_R.choose_action(right_state)

        self.move_paddle(self.paddle_left, left_action)
        self.move_paddle(self.paddle_right, right_action)

        reward_L, reward_R = 0.0, 0.0
        done = False

        if self.ball.left <= 0:
            reward_L = -1.0
            reward_R = 1.0
            done = True
        elif self.ball.right >= SCREEN_WIDTH:
            reward_L = 1.0
            reward_R = -1.0
            done = True
        else:
            if hit_left:
                reward_L += 0.1
                offset = (self.ball.centery - self.paddle_left.centery) / (PADDLE_HEIGHT / 2)
                self.ball_dy = BALL_SPEED_BASE * offset
                self.ball_dx = abs(self.ball_dx) + BALL_SPEED_INCREMENT
                if self.is_edge_hit(self.ball, self.paddle_left):
                    reward_L += 0.3

            if hit_right:
                reward_R += 0.1
                offset = (self.ball.centery - self.paddle_right.centery) / (PADDLE_HEIGHT / 2)
                self.ball_dy = BALL_SPEED_BASE * offset
                self.ball_dx = -abs(self.ball_dx) - BALL_SPEED_INCREMENT
                if self.is_edge_hit(self.ball, self.paddle_right):
                    reward_R += 0.3

            reward_L += self.directional_reward(self.ball.centery, self.paddle_left.centery, left_action)
            reward_R += self.directional_reward(self.ball.centery, self.paddle_right.centery, right_action)

        left_next = self.agent_L.discretize(self.ball.x, self.ball.y, self.ball_dx, self.ball_dy, self.paddle_left.y)
        right_next = self.agent_R.discretize(self.ball.x, self.ball.y, self.ball_dx, self.ball_dy, self.paddle_right.y)

        self.agent_L.learn(left_state, left_action, reward_L, left_next)
        self.agent_R.learn(right_state, right_action, reward_R, right_next)

        return done

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 0, 255), self.paddle_left)
        pygame.draw.rect(self.screen, (0, 128, 255), self.paddle_right)
        pygame.draw.ellipse(self.screen, (0, 255, 0), self.ball)
        pygame.draw.aaline(self.screen, (255, 255, 255), (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            done = self.step()
            self.draw()
            self.clock.tick(FPS)

            if done:
                self.reset()
                self.episode += 1
                self.agent_L.decay_epsilon()
                self.agent_R.decay_epsilon()
                if self.episode % 10 == 0:
                    print(f"Episode {self.episode} complete. Epsilon: {self.agent_L.epsilon:.3f}")
                    self.agent_L.save_q_table()
                    self.agent_R.save_q_table()

        pygame.quit()
        self.agent_L.save_q_table()
        self.agent_R.save_q_table()

if __name__ == "__main__":
    game = PongGame()
    game.run()
