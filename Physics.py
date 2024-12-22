import pygame
import sys
import math

pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Physics Ball Simulation")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
YELLOW = (255, 255, 0)

# Box boundaries (top-left, width, height)
# We'll draw a white rectangle on a black background.
box_x, box_y, box_width, box_height = 50, 50, 700, 500

# Ball properties
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_vx = 0   # velocity in x direction
ball_vy = 0   # velocity in y direction
ball_ay = 0.5 # gravity acceleration

dragging = False
drag_start_pos = (0, 0)

# Font for displaying distance
font = pygame.font.SysFont(None, 30)

# Center of the screen (for the yellow line)
center_x, center_y = WIDTH // 2, HEIGHT // 2

def draw_scene():
    # Fill background with black
    screen.fill(BLACK)
    
    # Draw the white rectangular box boundary
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 2)
    
    # Draw the red ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    
    # Draw a yellow line from center of screen to the ball
    pygame.draw.line(screen, YELLOW, (center_x, center_y), (ball_x, ball_y), 2)
    
    # Calculate distance from center to ball
    dist_to_center = math.hypot(ball_x - center_x, ball_y - center_y)
    
    # Show the distance as text in the corner
    distance_text = font.render(f"Distance: {dist_to_center:.2f}", True, YELLOW)
    screen.blit(distance_text, (20, 20))
    
    pygame.display.flip()

# Main loop
running = True
while running:
    dt = clock.tick(60)  # time between frames in milliseconds
    dt_sec = dt / 1000.0 # convert dt to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                # Check if we clicked inside the ball
                mouse_x, mouse_y = event.pos
                dist = math.hypot(mouse_x - ball_x, mouse_y - ball_y)
                if dist <= ball_radius:
                    dragging = True
                    drag_start_pos = (mouse_x, mouse_y)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:
                # Throw the ball based on drag distance
                mouse_x, mouse_y = event.pos
                dx = mouse_x - drag_start_pos[0]
                dy = mouse_y - drag_start_pos[1]
                
                # Adjust multiplier for throw strength
                throw_strength = 0.1
                ball_vx = dx * throw_strength
                ball_vy = dy * throw_strength
                
                dragging = False

    # If not dragging, apply physics updates
    if not dragging:
        # Gravity
        ball_vy += ball_ay
        
        # Update ball position
        ball_x += ball_vx
        ball_y += ball_vy
    
    # Collision with box boundaries
    # Left boundary
    if ball_x - ball_radius < box_x:
        ball_x = box_x + ball_radius
        ball_vx = -ball_vx * 0.8  # bounce, reduce speed
    # Right boundary
    if ball_x + ball_radius > box_x + box_width:
        ball_x = box_x + box_width - ball_radius
        ball_vx = -ball_vx * 0.8
    # Top boundary
    if ball_y - ball_radius < box_y:
        ball_y = box_y + ball_radius
        ball_vy = -ball_vy * 0.8
    # Bottom boundary
    if ball_y + ball_radius > box_y + box_height:
        ball_y = box_y + box_height - ball_radius
        ball_vy = -ball_vy * 0.8

    # Draw everything
    draw_scene()

pygame.quit()
sys.exit()
