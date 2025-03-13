# Hand Tracking Application

A real-time hand tracking application that monitors hand position within a defined area using OpenCV and MediaPipe.

## Features

- Real-time hand tracking using webcam
- Visual boundary box for hand positioning
- Live coordinate display for hand landmarks
- Color-coded tracking points:
  - Blue: Inside the boundary box
  - Red: Outside the boundary box
- Automatic warning system:
  - On-screen warnings when no hand is detected
  - Logs warnings to `problems.txt` when hand is outside the box for >5 seconds

## Requirements

```
opencv-python
mediapipe
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/hand-tracking.git
cd hand-tracking
```

2. Install dependencies:
```bash
pip install opencv-python mediapipe
```

## Usage

1. Run the application:
```bash
python hand_tracking.py
```

2. Interface elements:
   - Green rectangle: Target area for hand positioning
   - Blue dots: Hand landmarks inside the target area
   - Red dots: Hand landmarks outside the target area
   - Text display: Shows coordinates for each landmark
   - Top-left display: Shows thumb and index finger positions

3. Controls:
   - Press 'Esc' to exit the application

## Warning System

The application includes an automated warning system that:
- Displays "Warning: No hand detected!" on screen when no hand is visible
- Logs warnings to `problems.txt` when the hand remains outside the target area for more than 5 seconds
- Timestamps all warnings for easy tracking

## Hand Landmarks

The application tracks 21 hand landmarks using MediaPipe:
- Landmark 0: Wrist
- Landmarks 1-4: Thumb
- Landmarks 5-8: Index finger
- Landmarks 9-12: Middle finger
- Landmarks 13-16: Ring finger
- Landmarks 17-20: Pinky finger

## License

This project is open source and available under the MIT License.
