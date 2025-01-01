import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import Canvas, Scrollbar
from PIL import Image, ImageTk  # For displaying OpenCV images in Tkinter

# Initialize variables
canvas = None
prev_point = None  # To smooth lines
movement_threshold = 10  # Minimum movement in pixels to draw
alpha = 0.2  # Interpolation factor to smooth movement
drawn_lines = []  # Store drawn lines (start and end points)
blackboard_mode = True  # Start with blackboard (White Art on Black Background)

# Video capture
cap = cv2.VideoCapture(0)

# Manually set frame dimensions (width x height)
manual_width = 650
manual_height = 600
frame_shape = (manual_height, manual_width, 3)

def reset_canvas():
    global canvas, drawn_lines
    if blackboard_mode:
        canvas = np.zeros(frame_shape, dtype=np.uint8)  # Black background
    else:
        canvas = np.ones(frame_shape, dtype=np.uint8) * 255  # White background
    drawn_lines.clear()
    print("Canvas reset!")
    messagebox.showinfo("Canvas Reset", "Canvas has been reset!")

def toggle_mode():
    global blackboard_mode, canvas, drawn_lines
    blackboard_mode = not blackboard_mode
    # Switch canvas background color
    if blackboard_mode:
        canvas = np.zeros(frame_shape, dtype=np.uint8)  # Black background
        print("Switched to Blackboard Mode: White Art on Black Background")
    else:
        canvas = np.ones(frame_shape, dtype=np.uint8) * 255  # White background
        print("Switched to Whiteboard Mode: Black Art on White Background")

    # Redraw lines with the new background
    for start_point, end_point in drawn_lines:
        color = (255, 255, 255) if blackboard_mode else (0, 0, 0)
        cv2.line(canvas, start_point, end_point, color, 5)

def erase_last_few_lines(lines_to_erase=4):
    global canvas, drawn_lines
    if drawn_lines:
        # Remove the last lines_to_erase lines
        lines_removed = min(len(drawn_lines), lines_to_erase)
        drawn_lines = drawn_lines[:-lines_removed]

        # Clear the canvas
        if blackboard_mode:
            canvas.fill(0)  # Black background
        else:
            canvas.fill(255)  # White background

        # Redraw the remaining lines
        color = (255, 255, 255) if blackboard_mode else (0, 0, 0)
        for start_point, end_point in drawn_lines:
            cv2.line(canvas, start_point, end_point, color, 5)

        print(f"Last {lines_removed} line(s) erased!")
        messagebox.showinfo("Lines Erased", f"Last {lines_removed} line(s) have been erased!")
    else:
        messagebox.showwarning("No Lines", "No lines to erase!")

def save_canvas():
    filename = "canvas_art.png"
    cv2.imwrite(filename, canvas)  # Save the current canvas
    print(f"Canvas saved as {filename}!")
    messagebox.showinfo("Canvas Saved", f"Canvas has been saved as {filename}!")

# Tkinter window setup
root = tk.Tk()
root.title("Air Drawing Application")

# Create a frame for buttons and canvas
control_frame = tk.Frame(root)
control_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Create a frame for the scrollable area
scroll_frame = tk.Frame(root)
scroll_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add Scrollbars
scrollbar_x = Scrollbar(scroll_frame, orient=tk.HORIZONTAL)
scrollbar_y = Scrollbar(scroll_frame, orient=tk.VERTICAL)

# Create a canvas area with enough width for both video and canvas
canvas_area = Canvas(
    scroll_frame,
    xscrollcommand=scrollbar_x.set,
    yscrollcommand=scrollbar_y.set,
    width=manual_width,  # Set the canvas width to manual width
    height=manual_height  # Keep the height fixed
)
canvas_area.grid(row=0, column=0, sticky="nsew")  # Place canvas in grid, stretch in all directions

# Add scrollbars
scrollbar_x.grid(row=1, column=0, sticky="ew")
scrollbar_y.grid(row=0, column=1, sticky="ns")

scrollbar_x.config(command=canvas_area.xview)
scrollbar_y.config(command=canvas_area.yview)

# Adjust scrollregion dynamically
canvas_area.bind("<Configure>", lambda e: canvas_area.config(scrollregion=canvas_area.bbox("all")))

# Add buttons
reset_button = tk.Button(control_frame, text="Reset Canvas", command=reset_canvas)
reset_button.pack(pady=5)

toggle_button = tk.Button(control_frame, text="Toggle Mode (Black/White)", command=toggle_mode)
toggle_button.pack(pady=10)

erase_button = tk.Button(control_frame, text="Erase Last Few Lines", command=lambda: erase_last_few_lines(4))
erase_button.pack(pady=10)

save_button = tk.Button(control_frame, text="Save Canvas", command=save_canvas)
save_button.pack(pady=5)

# Create a frame for both the video and blackboard (side by side)
side_by_side_frame = tk.Frame(canvas_area)
side_by_side_frame.grid(row=0, column=0, sticky="nsew")

# Add labels for video and blackboard inside the side_by_side_frame
video_label = tk.Label(side_by_side_frame)
video_label.grid(row=0, column=0, padx=5, pady=5)  # Video on the left side

blackboard_label = tk.Label(side_by_side_frame)
blackboard_label.grid(row=0, column=1, padx=5, pady=5)  # Blackboard on the right side

# Configure grid weights to ensure proper resizing
side_by_side_frame.grid_columnconfigure(0, weight=1, uniform="equal")  # Video takes equal space
side_by_side_frame.grid_columnconfigure(1, weight=1, uniform="equal")  # Blackboard takes equal space
side_by_side_frame.grid_rowconfigure(0, weight=1)

# Start the frame processing loop
def process_frame():
    global frame, canvas, prev_point

    ret, frame = cap.read()
    if not ret:
        root.quit()  # Exit the application if frame capture fails
        return

    frame = cv2.flip(frame, 1)  # Mirror the frame

    if canvas is None:
        if blackboard_mode:
            canvas = np.zeros(frame_shape, dtype=np.uint8)  # Black background
        else:
            canvas = np.ones(frame_shape, dtype=np.uint8) * 255  # White background

    # Resize frame to match canvas size
    frame_resized = cv2.resize(frame, (manual_width, manual_height))

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)

    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Create a mask for skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply morphological transformations
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    mask_inv = cv2.bitwise_not(mask)

# Blur the background by applying the inverse mask
    blurred_background = cv2.GaussianBlur(frame_resized, (21, 21), 0)
# Use the mask to combine the original image and blurred background
    foreground = cv2.bitwise_and(frame_resized, frame_resized, mask=mask)
    background = cv2.bitwise_and(blurred_background, blurred_background, mask=mask_inv)

    final_frame = cv2.add(foreground, background)


    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Find the largest contour (assume it's the hand)
        largest_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(largest_contour) > 5000:
            # Calculate the palm center
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                palm_center = (cx, cy)

                # Draw palm center for debugging
                cv2.circle(final_frame, palm_center, 5, (255, 0, 0), -1)

                # Check movement
                if prev_point is not None:
                    smooth_point = (
                        int(alpha * palm_center[0] + (1 - alpha) * prev_point[0]),
                        int(alpha * palm_center[1] + (1 - alpha) * prev_point[1]),
                    )

                    distance_moved = np.linalg.norm(np.array(prev_point) - np.array(smooth_point))
                    if distance_moved > movement_threshold:
                        color = (255, 255, 255) if blackboard_mode else (0, 0, 0)
                        cv2.line(canvas, prev_point, smooth_point, color, 5)
                        drawn_lines.append((prev_point, smooth_point))
                        prev_point = smooth_point
                else:
                    prev_point = palm_center

    # Resize the canvas to match frame size
    canvas_resized = cv2.resize(canvas, (manual_width, manual_height))

    # Combine the canvas with the resized frame (this will blur the background)
    combined = cv2.addWeighted(final_frame, 0.5, canvas_resized, 0.5, 0)

    # Convert video feed to ImageTk format
    video_img = Image.fromarray(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB))
    video_imgtk = ImageTk.PhotoImage(image=video_img)

    # Convert canvas to ImageTk format
    blackboard_img = Image.fromarray(cv2.cvtColor(canvas_resized, cv2.COLOR_BGR2RGB))
    blackboard_imgtk = ImageTk.PhotoImage(image=blackboard_img)

    # Display video feed and blackboard canvas side by side
    video_label.imgtk = video_imgtk
    video_label.configure(image=video_imgtk)

    blackboard_label.imgtk = blackboard_imgtk
    blackboard_label.configure(image=blackboard_imgtk)

    # Adjust scrollable region
    canvas_area.update_idletasks()
    canvas_area.config(scrollregion=canvas_area.bbox("all"))

    # Schedule the next frame processing
    video_label.after(10, process_frame)

# Start the frame processing
process_frame()

# Start the Tkinter event loop
root.mainloop()

# Release resources
cap.release()
cv2.destroyAllWindows()