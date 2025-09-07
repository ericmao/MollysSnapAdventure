#!/usr/bin/env python3
"""
🏊‍♀️ Molly's Swim & Smile Adventure - Week 1
AI Smile Camera with Pool-Blue Face Detection

This is Molly's first dive into AI programming! This camera detects faces
and draws beautiful pool-blue frames around them. It's the foundation
for our swim-themed AI adventure!

Author: Molly (with Dad's help!)
Date: September 7, 2025
"""

import cv2
import numpy as np
import sys
import os

# Pool-blue color (RGB: 0, 188, 212 -> BGR for OpenCV: 212, 188, 0)
POOL_BLUE = (212, 188, 0)
FRAME_THICKNESS = 3

def setup_camera():
    """Initialize the camera for our swim & smile adventure!"""
    print("Starting Molly's Swim & Smile Camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Oops! Camera not found. Check your camera connection!")
        return None
    
    print("Camera ready! Let's detect some faces!")
    return cap

def detect_faces(frame):
    """
    Detect faces in the camera frame using OpenCV's built-in detector.
    Returns a list of face rectangles.
    """
    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Load the face detection classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    return faces

def draw_pool_blue_frame(frame, faces):
    """
    Draw beautiful pool-blue frames around detected faces.
    This is where the swimming magic happens! 🌊
    """
    for (x, y, w, h) in faces:
        # Draw the main pool-blue rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), POOL_BLUE, FRAME_THICKNESS)
        
        # Add a fun "Swimming with AI!" label
        label_text = "Swimming with AI!"
        label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        
        # Position label above the face frame
        label_x = x
        label_y = y - 10 if y - 10 > 20 else y + h + 30
        
        # Draw label background
        cv2.rectangle(frame, 
                     (label_x, label_y - label_size[1] - 5), 
                     (label_x + label_size[0], label_y + 5), 
                     POOL_BLUE, -1)
        
        # Draw label text
        cv2.putText(frame, label_text, (label_x, label_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return frame

def add_swim_info(frame):
    """Add some fun swimming-themed info to the camera feed!"""
    height, width = frame.shape[:2]
    
    # Add title
    title = "Molly's Swim & Smile Adventure"
    cv2.putText(frame, title, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, POOL_BLUE, 2)
    
    # Add instructions
    instructions = "Press 'q' to quit, 's' to save photo"
    cv2.putText(frame, instructions, (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return frame

def save_photo(frame, photo_count):
    """Save a snapshot of our swim & smile moment!"""
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    
    filename = f"outputs/swim_smile_{photo_count:03d}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Splash! Photo saved as {filename}")
    return photo_count + 1

def main():
    """
    Main function - Let's start our swim & smile adventure!
    This is where Molly's AI journey begins! 🌊
    """
    print("Welcome to Molly's Swim & Smile Adventure!")
    print("=" * 50)
    
    # Initialize camera
    cap = setup_camera()
    if cap is None:
        return
    
    photo_count = 1
    
    print("\nInstructions:")
    print("- Look at the camera and watch the pool-blue frames!")
    print("- Press 's' to save a photo")
    print("- Press 'q' to quit")
    print("\nHave fun swimming with AI!")
    
    try:
        while True:
            # Capture frame from camera
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame. Check camera!")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect faces in the frame
            faces = detect_faces(frame)
            
            # Draw pool-blue frames around faces
            frame = draw_pool_blue_frame(frame, faces)
            
            # Add swimming-themed information
            frame = add_swim_info(frame)
            
            # Show the result
            cv2.imshow("Molly's Swim & Smile Camera", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n Thanks for swimming with AI! See you next time!")
                break
            elif key == ord('s'):
                photo_count = save_photo(frame, photo_count)
    
    except KeyboardInterrupt:
        print("\n Camera stopped. Thanks for the swim!")
    
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed. Keep swimming with code!")

if __name__ == "__main__":
    main()
