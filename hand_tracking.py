import cv2
import mediapipe as mp
import time
# this is a project for uni
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
# amzing 
cap = cv2.VideoCapture(0)

box_top_left = (50, 100)
box_bottom_right = (550, 300)

last_check_time = time.time()
warning_interval = 5  # Interval in seconds to check for hand presence
log_file = "problems.txt"

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        image = cv2.flip(image, 1)
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = hands.process(image_rgb)
        
        cv2.rectangle(image, box_top_left, box_bottom_right, (0, 255, 0), 2)
        
        hand_in_box = False
        hand_coordinates = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    hand_coordinates.append((cx, cy))

                    if (box_top_left[0] < cx < box_bottom_right[0]) and (box_top_left[1] < cy < box_bottom_right[1]):
                        color = (255, 0, 0)  # Blue for inside the box
                        hand_in_box = True
                        status = "Inside Box"
                    else:
                        color = (0, 0, 255)  # Red for outside the box
                        status = "Outside Box"

                    cv2.circle(image, (cx, cy), 5, color, cv2.FILLED)
                    # Display coordinates for all landmarks
                    text = f"Landmark {idx}: ({cx},{cy}) {status}"
                    cv2.putText(image, text, (cx, cy + 20), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                    # Display coordinates for thumb and index finger
                    if idx in [4, 8]:  # Thumb and index finger
                        text = f"Finger {idx}: ({cx},{cy}) {status}"
                        cv2.putText(image, text, (10, 30 if idx == 4 else 60), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    # Only print landmark positions every 30 frames to reduce output
                    if idx in [4, 8, 12, 16, 20] and cv2.getTickCount() % 30 == 0:  # Only thumb, index, middle, ring and pinky tips
                        print(f'Finger tip {idx}: ({cx}, {cy}) - {"Inside" if hand_in_box else "Outside"} box')
                    else:
                        pass

                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if not results.multi_hand_landmarks:
            warning_message = "Warning: No hand detected!"
            cv2.putText(image, warning_message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        current_time = time.time()
        if current_time - last_check_time >= warning_interval:
            last_check_time = current_time
            if not hand_in_box:
                warning_message = "Warning: Hand out of the box!"
                print(warning_message)
                with open(log_file, "a") as file:
                    file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {warning_message}\n")
        
        cv2.imshow('Hand Tracking', image)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
