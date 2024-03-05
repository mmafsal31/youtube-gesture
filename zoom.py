import cv2
import mediapipe as mp
import pyautogui

# Initialize hand tracking module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize PyAutoGUI
pyautogui.PAUSE = 0

# Function to perform actions based on hand gestures
def perform_action(action):
    if action == 'play_pause':
        pyautogui.press('space')
    elif action == 'volume_up':
        pyautogui.press('volumeup')
    elif action == 'volume_down':
        pyautogui.press('volumedown')
    
def perform_scroll(hand_landmarks):


    # Get the positions of all fingers
    finger_positions = [hand_landmarks.landmark[i] for i in range(5, 20)]

    # Calculate the average y-coordinate of all finger positions
    avg_y = sum([pos.y for pos in finger_positions]) / len(finger_positions)

    # Scroll up if fingers are moving up, scroll down if fingers are moving down
    if avg_y < 0.4:
        pyautogui.scroll(150)  # Scroll up
    elif avg_y > 0.6:
        pyautogui.scroll(-150)  # Scroll down


# Main loop for capturing video frames and processing hand gestures
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to get hand landmarks
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:                                                                                               
            # Perform scrolling based on hand position
            perform_scroll(hand_landmarks)
            # Perform actions based on hand landmarks
            # For simplicity, let's assume we only consider one hand
            # and a specific gesture (e.g., thumb and index finger pinch)
            # You can replace this with your gesture recognition logic
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip_x, thumb_tip_y = thumb_tip.x, thumb_tip.y
            index_tip_x, index_tip_y = index_tip.x, index_tip.y

            # Calculate the distance between thumb tip and index tip
            distance = ((thumb_tip_x - index_tip_x)**2 + (thumb_tip_y - index_tip_y)**2)**0.5

            if distance < 0.1:  # Example threshold for pinch gesture
                perform_action('play_pause')
            elif thumb_tip_x > index_tip_x:  # Example condition for volume control
                perform_action('volume_up')
            else:
                perform_action('volume_down')

    # Display the frame
    cv2.imshow('Hand Gesture Control', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy any OpenCV windows
cap.release()
cv2.destroyAllWindows()
                                                                                                                                                                                                          