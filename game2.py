import cv2
import numpy as np
import random

# Set up the game window
window_size = (640, 480)
window_name = 'Color Catcher'
cv2.namedWindow(window_name)
cv2.moveWindow(window_name, 0, 0)

# Set up the game objects
catcher_color = (0, 0, 255)
catcher_width = 80
catcher_height = 20
catcher_position = np.array([window_size[0]//2, window_size[1]-catcher_height], dtype=int)
catcher_velocity = np.array([10, 0], dtype=int)

ball_radius = 20
ball_speed = 5
ball_colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
balls = []

# Set up the video capture device
cap = cv2.VideoCapture(0)

while True:
    # Generate a new ball with a random color and position if necessary
    if len(balls) < 5:
        ball_color = random.choice(ball_colors)
        ball_position = np.array([random.randint(ball_radius, window_size[0]-ball_radius), 0], dtype=int)
        ball_velocity = np.array([0, ball_speed], dtype=int)
        balls.append((ball_color, ball_position, ball_velocity))
    
    # Move the balls and check for collisions with the catcher
    for i in range(len(balls)):
        balls[i] = (balls[i][0], balls[i][1]+balls[i][2], balls[i][2])
        ball_position = balls[i][1]
        if ball_position[1]+ball_radius >= catcher_position[1] and \
           ball_position[0] >= catcher_position[0] and \
           ball_position[0] <= catcher_position[0]+catcher_width:
            balls.pop(i)
            break
    
    # Move the catcher if necessary
    if cv2.waitKey(1) & 0xFF == ord('a') and catcher_position[0] > 0:
        catcher_position -= catcher_velocity
    elif cv2.waitKey(1) & 0xFF == ord('d') and catcher_position[0]+catcher_width < window_size[0]:
        catcher_position += catcher_velocity
    
    # Draw the game objects on the screen
    frame = np.zeros((window_size[1], window_size[0], 3), dtype=np.uint8)
    for ball in balls:
        cv2.circle(frame, tuple(ball[1]), ball_radius, ball[0], -1)
    cv2.rectangle(frame, tuple(catcher_position), tuple(catcher_position+np.array([catcher_width, catcher_height])), catcher_color, -1)
    
    # Display the frame
    cv2.imshow(window_name, frame)
    
    # Exit the game if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the game window
cap.release()
cv2.destroyAllWindows()