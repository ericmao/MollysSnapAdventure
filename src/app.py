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
from PIL import Image

# Pool-blue color (RGB: 0, 188, 212 -> BGR for OpenCV: 212, 188, 0)
POOL_BLUE = (212, 188, 0)
FRAME_THICKNESS = 3

# Global variables for smile detection
pool_image = None
smile_cascade = None
smile_counter = 0  # Counter for stable smile detection
SMILE_THRESHOLD = 3  # Need 3 consecutive frames of smile detection

def load_pool_image():
    """Load and prepare the swimming pool image for overlay"""
    global pool_image
    try:
        # Load the pool image
        pool_img = cv2.imread('assets/image.png', cv2.IMREAD_UNCHANGED)
        if pool_img is None:
            print("Warning: Could not load pool image from assets/image.png")
            return False
        
        # Resize the pool image to a reasonable size (e.g., 150x150)
        pool_image = cv2.resize(pool_img, (150, 150))
        print("Pool image loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading pool image: {e}")
        return False

def initialize_smile_detector():
    """Initialize the smile detection cascade classifier"""
    global smile_cascade
    try:
        smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        if smile_cascade.empty():
            print("Warning: Could not load smile cascade classifier")
            return False
        print("Smile detector initialized!")
        return True
    except Exception as e:
        print(f"Error initializing smile detector: {e}")
        return False

def setup_camera():
    """Initialize the camera for our swim & smile adventure!"""
    print("Starting Molly's Swim & Smile Camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Oops! Camera not found. Check your camera connection!")
        return None
    
    print("Camera ready! Let's detect some faces!")
    return cap

def detect_faces_and_smiles(frame):
    """
    Detect faces and smiles in the camera frame.
    Returns a list of face rectangles and smile information.
    """
    # Convert frame to grayscale for detection
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
    
    faces_with_smiles = []
    
    # For each detected face, check for smiles
    for (x, y, w, h) in faces:
        # Extract the face region
        roi_gray = gray[y:y+h, x:x+w]
        
        # Detect smiles in this face region with stricter parameters
        has_smile = False
        if smile_cascade is not None:
            smiles = smile_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.7,      # Smaller scale factor for more precise detection
                minNeighbors=22,      # Higher neighbor requirement for confidence
                minSize=(30, 30),     # Larger minimum size for better accuracy
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            # Additional confidence check: require multiple detections or larger smile area
            if len(smiles) > 0:
                # Calculate the total area of detected smiles
                total_smile_area = sum(w * h for (x, y, w, h) in smiles)
                face_area = w * h
                smile_ratio = total_smile_area / face_area
                
                # Only consider it a smile if the ratio is significant enough
                has_smile = smile_ratio > 0.02  # At least 2% of face area should be smile
        
        faces_with_smiles.append({
            'face': (x, y, w, h),
            'has_smile': has_smile
        })
    
    return faces_with_smiles

def overlay_pool_image(frame, x, y):
    """
    Overlay the swimming pool image at the specified position
    """
    global pool_image
    if pool_image is None:
        return frame
    
    h_frame, w_frame = frame.shape[:2]
    h_pool, w_pool = pool_image.shape[:2]
    
    # Calculate position to center the pool image
    start_x = max(0, min(x - w_pool//2, w_frame - w_pool))
    start_y = max(0, min(y - h_pool//2, h_frame - h_pool))
    end_x = start_x + w_pool
    end_y = start_y + h_pool
    
    # Handle transparency if the pool image has an alpha channel
    if pool_image.shape[2] == 4:  # RGBA
        # Extract the alpha channel
        alpha = pool_image[:, :, 3] / 255.0
        
        # Overlay the RGB channels
        for c in range(3):
            frame[start_y:end_y, start_x:end_x, c] = (
                alpha * pool_image[:, :, c] + 
                (1 - alpha) * frame[start_y:end_y, start_x:end_x, c]
            )
    else:  # RGB
        # Simple overlay without transparency
        frame[start_y:end_y, start_x:end_x] = pool_image
    
    return frame

def draw_pool_blue_frame_and_effects(frame, faces_data):
    """
    Draw beautiful pool-blue frames around detected faces and add special effects for stable smiles.
    """
    for face_data in faces_data:
        x, y, w, h = face_data['face']
        has_smile = face_data.get('has_smile', False)
        stable_smile = face_data.get('stable_smile', False)
        
        # Choose frame color based on stable smile detection
        if stable_smile:
            frame_color = (0, 255, 0)  # Bright green for confirmed smile
            frame_thickness = FRAME_THICKNESS + 3
        elif has_smile:
            frame_color = (0, 255, 255)  # Yellow for detected but not stable smile
            frame_thickness = FRAME_THICKNESS + 1
        else:
            frame_color = POOL_BLUE  # Pool blue for normal detection
            frame_thickness = FRAME_THICKNESS
        
        # Draw the main rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), frame_color, frame_thickness)
        
        # Add appropriate label and effects
        if stable_smile:
            label_text = "BIG SMILE! Pool Time!"
            # Show pool image when stable smile is detected
            center_x = x + w // 2
            center_y = y + h // 2
            frame = overlay_pool_image(frame, center_x, center_y - h//2 - 80)
        elif has_smile:
            label_text = "Keep Smiling..."
        else:
            label_text = "Swimming with AI!"
        
        label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        
        # Position label above the face frame
        label_x = x
        label_y = y - 10 if y - 10 > 20 else y + h + 30
        
        # Draw label background
        cv2.rectangle(frame, 
                     (label_x, label_y - label_size[1] - 5), 
                     (label_x + label_size[0], label_y + 5), 
                     frame_color, -1)
        
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
    instructions = "Press 'q' to quit, 's' to save photo - SMILE for pool magic!"
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
    This is where Molly's AI journey begins!
    """
    print("Welcome to Molly's Swim & Smile Adventure!")
    print("=" * 50)
    
    # Initialize components
    print("Loading swimming pool image...")
    if not load_pool_image():
        print("Warning: Pool image not loaded. Continuing without pool effects.")
    
    print("Initializing smile detector...")
    if not initialize_smile_detector():
        print("Warning: Smile detector not loaded. Continuing with face detection only.")
    
    # Initialize camera
    cap = setup_camera()
    if cap is None:
        return
    
    photo_count = 1
    
    print("\nInstructions:")
    print("- Look at the camera and watch the pool-blue frames!")
    print("- SMILE BIG and HOLD IT to see the swimming pool appear!")
    print("- Yellow frame = smile detected, Green frame = confirmed smile!")
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
            
            # Detect faces and smiles in the frame
            faces_data = detect_faces_and_smiles(frame)
            
            # Check for stable smile detection
            global smile_counter
            current_smiles = sum(1 for face_data in faces_data if face_data['has_smile'])
            
            if current_smiles > 0:
                smile_counter += 1
            else:
                smile_counter = max(0, smile_counter - 1)  # Gradually decrease counter
            
            # Only show pool effect if we have stable smile detection
            stable_smile_detected = smile_counter >= SMILE_THRESHOLD
            
            # Update faces_data with stable smile information
            for face_data in faces_data:
                face_data['stable_smile'] = face_data['has_smile'] and stable_smile_detected
            
            # Draw pool-blue frames and special effects for smiles
            frame = draw_pool_blue_frame_and_effects(frame, faces_data)
            
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
                # Check if anyone was smiling when photo was taken
                smiling_faces = sum(1 for face_data in faces_data if face_data['has_smile'])
                if smiling_faces > 0:
                    print(f"Great! Captured {smiling_faces} smile(s) with pool magic!")
    
    except KeyboardInterrupt:
        print("\n Camera stopped. Thanks for the swim!")
    
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed. Keep swimming with code!")

if __name__ == "__main__":
    main()
