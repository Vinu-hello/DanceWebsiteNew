import cv2
import numpy as np

# Initialize canvas and previous point
canvas = None
prev_point = None  # To smooth lines
movement_threshold = 10  # Minimum movement in pixels to draw
alpha = 0.2  # Interpolation factor to slow down movement

# Video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror the frame

    if canvas is None:
        canvas = np.zeros_like(frame)  # Create a black canvas with the same size as the frame

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Create a mask for skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply morphological transformations to reduce noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Find the largest contour (assume it's the hand)
        largest_contour = max(contours, key=cv2.contourArea)

        # Check contour size to filter out noise
        if cv2.contourArea(largest_contour) > 5000:
            # Calculate the palm center
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                palm_center = (cx, cy)

                # Draw palm center for debugging
                cv2.circle(frame, palm_center, 5, (255, 0, 0), -1)

                # Check if movement is significant before drawing
                if prev_point is not None:
                    # Interpolate between previous point and palm center
                    smooth_point = (
                        int(alpha * palm_center[0] + (1 - alpha) * prev_point[0]),
                        int(alpha * palm_center[1] + (1 - alpha) * prev_point[1]),
                    )

                    distance_moved = np.linalg.norm(np.array(prev_point) - np.array(smooth_point))
                    if distance_moved > movement_threshold:
                        # Draw line if movement is significant
                        cv2.line(canvas, prev_point, smooth_point, (255, 255, 255), 5)
                        prev_point = smooth_point
                else:
                    # Initialize prev_point if it's None
                    prev_point = palm_center

    # Combine the canvas with the original frame
    combined = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Show the result in the "Air Drawing" window
    cv2.imshow("Air Drawing", combined)

    # Show the canvas window to see the drawing separately
    cv2.imshow("Canvas", canvas)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()