import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

is_full_screen = False
thumb_up = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[4]  # Thumb tip landmark index is 4

            # Check if thumb is up
            if thumb_tip.y < hand_landmarks.landmark[3].y:  # Compare with the base of the thumb (landmark index 3)
                thumb_up = True
            else:
                thumb_up = False

    if thumb_up and not is_full_screen:
        # Activate full screen mode
        pyautogui.press('f')  # Press the 'f' key (assuming 'f' is the full-screen shortcut)
        is_full_screen = True

    elif not thumb_up and is_full_screen:
        # Exit full screen mode
        pyautogui.press('f')  # Press the 'f' key (assuming 'f' is the full-screen shortcut)
        is_full_screen = False

    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
