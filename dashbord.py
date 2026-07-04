import cv2
import numpy as np
import hashlib
import os
import time
import tkinter as tk
from PIL import Image, ImageTk

VIDEO_PATH = 'results.mp4'

# --- 1. HYBRID CRYPTOGRAPHY LOGIC ---
def generate_key(fish_coords):
    # System-level secure entropy pool
    nonce = os.urandom(16)  
    # Nanosecond precision timing signature
    timestamp = str(time.time_ns()).encode()  
    
    if fish_coords:
        # Hybrid Stream: Biological Chaos + Time + Cryptographic Nonce
        entropy = fish_coords.encode() + timestamp + nonce
        mode = 'FISH'
    else:
        # Fallback Mode: OS Entropy Pool Only
        entropy = os.urandom(32) + timestamp + nonce
        mode = 'FALLBACK'
        
    # Unidirectional cryptographic hash execution
    secure_hash = hashlib.sha256(entropy).hexdigest()
    return secure_hash, mode

# --- 2. VISION DETECTION LOGIC (TRACKS RED BOXES) ---
def detect_centers(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define RED color ranges (Red wraps around 0 and 180 in HSV)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = red_mask1 | red_mask2
    
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    
    centers = []
    for cnt in contours:
        bx, by, bw, bh = cv2.boundingRect(cnt)
        if 500 < bw * bh < 100000 and bw > 20 and bh > 20:
            centers.append(f'{bx + bw // 2},{by + bh // 2}')
            
    return centers

# --- 3. TKINTER GUI SETUP ---
root = tk.Tk()
root.title('Biomimetic Underwater Cryptography')
root.configure(bg='#0a2342')

tk.Label(
    root, 
    text='BIOMIMETIC UNDERWATER CRYPTOGRAPHY',
    font=('Courier', 13, 'bold'), 
    fg='#7fb8d8',
    bg='#0a2342'
).pack(pady=8)

main = tk.Frame(root, bg='#0a2342')
main.pack(padx=10, pady=4)

vid_label = tk.Label(main, bg='#0a2342')
vid_label.grid(row=0, column=0, padx=8)

kf = tk.Frame(main, bg='#1e1e2e', width=370)
kf.grid(row=0, column=1, padx=8, sticky='nsew')

mode_lbl = tk.Label(
    kf, 
    text='STARTING...',
    font=('Courier', 10, 'bold'), 
    fg='#a6e3a1', 
    bg='#1e1e2e'
)
mode_lbl.pack(pady=(12, 3))

count_lbl = tk.Label(
    kf, 
    text='Fish: 0',
    font=('Courier', 9), 
    fg='#cdd6f4', 
    bg='#1e1e2e'
)
count_lbl.pack()

tk.Label(
    kf, 
    text='HYBRID SHA-256 KEY', 
    font=('Courier', 8),
    fg='#585b70', 
    bg='#1e1e2e'
).pack(pady=(10, 2))

key_lbl = tk.Label(
    kf, 
    text='', 
    font=('Courier', 9, 'bold'),
    fg='#a6e3a1', 
    bg='#1e1e2e', 
    wraplength=350, 
    justify='left'
)
key_lbl.pack(padx=8)

log = tk.Text(
    kf, 
    height=10, 
    width=42,
    font=('Courier', 8), 
    bg='#181825', 
    fg='#cdd6f4',
    relief='flat', 
    state='disabled'
)
log.pack(padx=8, pady=10)

# --- 4. VIDEO LOOP INTEGRATION ---
cap = cv2.VideoCapture(VIDEO_PATH)
frame_n = 0

def update():
    global frame_n
    ret, frame = cap.read()
    
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        root.after(33, update)
        return
        
    centers = detect_centers(frame)
    # Generates secure hybrid keys using live coordinates
    key, mode = generate_key('|'.join(centers))
    
    # Process and center display dimensions
    display = cv2.resize(frame, (420, 320))
    img = Image.fromarray(cv2.cvtColor(display, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    vid_label.imgtk = imgtk
    vid_label.configure(image=imgtk)
    
    # Configure context-appropriate color palettes
    color = '#a6e3a1' if mode == 'FISH' else '#f9e2af'
    mtxt = f'FISH MODE — {len(centers)} fish' if mode == 'FISH' else 'FALLBACK MODE'
    
    mode_lbl.config(text=mtxt, fg=color)
    count_lbl.config(text=f'Fish detected: {len(centers)}')
    key_lbl.config(text=key[:32] + '...', fg=color)
    
    log.config(state='normal')
    log.insert('end', f'[{frame_n:04d}] {mode:<8}| {key[:16]}...\n')
    log.see('end')
    log.config(state='disabled')
    
    frame_n += 1
    root.after(40, update)

# Initialize scheduling loop
root.after(100, update)
root.mainloop()
cap.release()
