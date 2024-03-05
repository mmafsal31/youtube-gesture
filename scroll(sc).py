import cv2
import mediapipe as mp
import pyautogui

# Initialize hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# OpenCV setup
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame.")
        break

    # Convert the image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(rgb_frame)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Calculate the distance between thumb and other fingers
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_x, thumb_y = thumb_tip.x, thumb_tip.y

            all_fingers_open = True
            for finger in [mp_hands.HandLandmark.INDEX_FINGER_TIP,
                           mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                           mp_hands.HandLandmark.RING_FINGER_TIP,
                           mp_hands.HandLandmark.PINKY_TIP]:
                finger_tip = hand_landmarks.landmark[finger]
                finger_x, finger_y = finger_tip.x, finger_tip.y
                if finger_y > thumb_y:
                    all_fingers_open = False
                    break

            # Perform scrolling based on the hand gesture
            if all_fingers_open:
                # Check if the hand is above the center of the screen
                scroll_speed = 150  # Adjust this value for the desired scroll speed

                if thumb_y < 0.5:
                    pyautogui.scroll(scroll_speed)  # Scroll up
                else:
                    pyautogui.scroll(-scroll_speed)  # Scroll down

    # Display the frame
    cv2.imshow('Hand Gesture Control', frame)

    # Check for the 'q' key to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all windows
cap.release()
cv2.destroyAllWindows()
