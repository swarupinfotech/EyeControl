import cv2
import mediapipe as mp
import pyautogui
import threading
import tkinter as tk
from tkinter import messagebox

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Screen dimensions
screen_w, screen_h = pyautogui.size()

# Global control
running = False

def start_eye_control():
    global running
    running = True
    threading.Thread(target=eye_mouse_control).start()

def stop_eye_control():
    global running
    running = False
    messagebox.showinfo("Stopped", "Eye-controlled mouse has been stopped.")

def eye_mouse_control():
    global running
    cam = cv2.VideoCapture(0)

    while running:
        _, frame = cam.read()
        if not _:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark

            # Eye landmarks for cursor
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
                if id == 1:
                    screen_x = screen_w * landmark.x
                    screen_y = screen_h * landmark.y
                    pyautogui.moveTo(screen_x, screen_y)

            # Blink detection
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

            if (left[0].y - left[1].y) < 0.004:
                pyautogui.click()
                pyautogui.sleep(1)

        cv2.imshow('Eye Controlled Mouse', frame)
        if cv2.waitKey(1) == ord('q') or not running:
            break

    cam.release()
    cv2.destroyAllWindows()

# -------------------- UI --------------------
root = tk.Tk()
root.title("Eye Controlled Mouse - Swarup Mahato")
root.geometry("420x250")
root.config(bg="#121212")

title_label = tk.Label(root, text="👁️ Eye Controlled Mouse", font=("Helvetica", 18, "bold"), bg="#121212", fg="#00FFAA")
title_label.pack(pady=10)

desc_label = tk.Label(root, text="Move your mouse with eyes & blink to click", font=("Arial", 10), bg="#121212", fg="white")
desc_label.pack(pady=5)

start_btn = tk.Button(root, text="▶ Start Eye Control", command=start_eye_control, bg="#00AAFF", fg="white", font=("Arial", 12, "bold"), width=25, height=2)
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="⛔ Stop Eye Control", command=stop_eye_control, bg="#FF5555", fg="white", font=("Arial", 12, "bold"), width=25, height=2)
stop_btn.pack(pady=10)

footer = tk.Label(root, text="Developed by Swarup Mahato | AI + CV Project", font=("Arial", 9), bg="#121212", fg="#AAAAAA")
footer.pack(side="bottom", pady=10)

root.mainloop()
