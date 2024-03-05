import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize screen size
screen_width, screen_height = pyautogui.size()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for natural (mirror) viewing
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the index finger tip coordinates
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_x, index_finger_y = int(index_finger_tip.x * screen_width), int(index_finger_tip.y * screen_height)

            # Move the cursor to the index finger tip
            pyautogui.moveTo(index_finger_x, index_finger_y)

            # Check if the thumb is raised to simulate a click
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_x, thumb_y = int(thumb_tip.x * screen_width), int(thumb_tip.y * screen_height)
            thumb_is_raised = thumb_y < index_finger_y

            if thumb_is_raised:
                pyautogui.click()

    cv2.imshow('Media Player Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
