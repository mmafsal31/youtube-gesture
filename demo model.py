import cv2
import mediapipe as mp
import pyautogui


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
#drawing = mp.solutions.drawing_utils


# OpenCV setup
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame.")
        break
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)  

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks :
            #draw_landdrawingmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_x, index_finger_y = index_finger.x, index_finger.y


            index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            
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
                    pyautogui.scroll(-scroll_speed)  # Scroll up
                else:
                    pyautogui.scroll(scroll_speed)  # Scroll down


            

            if index_finger_y < thumb_y:
                hand_gesture = 'pointing up'
            elif index_finger_y > thumb_y:
                hand_gesture = 'pointing down'
            else:
                hand_gesture = 'others'

            if hand_gesture == 'pointing up':
                pyautogui.press('volumeup')
            elif hand_gesture == 'pointing down':
                pyautogui.press('volumedown')

# Display the frame
    cv2.imshow('Hand Gesture Control', frame)

    # Check for the 'q' key to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all windows
cap.release()
cv2.destroyAllWindows()
