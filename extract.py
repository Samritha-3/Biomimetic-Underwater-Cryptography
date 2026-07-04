import cv2
import numpy as np
import csv
import os

VIDEO_PATH = 'results.mp4'
OUTPUT_CSV = 'outputs/tracking_data.csv'

# Ensure the 'outputs' directory exists so it doesn't throw a FileNotFoundError
output_dir = os.path.dirname(OUTPUT_CSV)
if output_dir and not os.path.exists(output_dir): 
    os.makedirs(output_dir)

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)

with open(OUTPUT_CSV, 'w', newline='') as f: 
    writer = csv.writer(f) 
    writer.writerow(['frame', 'timestamp_ms', 'fish_count', 'centers']) 
    
    frame_idx = 0 
    while True: 
        ret, frame = cap.read() 
        if not ret: 
            break 
            
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
        
        # Define RED color ranges (Red wraps around 0 and 180 in HSV) 
        lower_red1 = np.array([0, 70, 50]) 
        upper_red1 = np.array([10, 255, 255]) 
        lower_red2 = np.array([170, 70, 50]) 
        upper_red2 = np.array([180, 255, 255]) 
        
        red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1) 
        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2) 
        
        # Combine both red masks into a single tracking layer 
        mask = red_mask1 | red_mask2 
        
        contours, _ = cv2.findContours( 
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE 
        ) 
        
        centers = [] 
        for cnt in contours: 
            x, y, w, h = cv2.boundingRect(cnt) 
            if 500 < w * h < 100000 and w > 20 and h > 20: 
                centers.append(f'{x + w // 2},{y + h // 2}') 
                
        ts = int((frame_idx / fps) * 1000) 
        writer.writerow([frame_idx, ts, len(centers), '|'.join(centers)]) 
        frame_idx += 1

cap.release()
print(f'Done! Extracted {frame_idx} frames to {OUTPUT_CSV}')
