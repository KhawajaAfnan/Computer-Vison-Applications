import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def capture_image_and_mark_points():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
    
    if not image_path:
        return

    focal_length = simpledialog.askfloat("Input", "Enter the focal length of your camera in mm (3.8 for redmi 8):")
    
    if focal_length is None or focal_length <= 0:
        messagebox.showerror("Error", "Invalid focal length entered.")
        return

    img = cv2.imread(image_path)
    img_copy = img.copy()

    def click_event(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            positions.append((x, y))
            cv2.circle(img_copy, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Mark the head and feet", img_copy)
            
            if len(positions) == 2:
                calculate_height(positions, img, focal_length)

    positions = []
    cv2.imshow("Mark the head and feet", img_copy)
    cv2.setMouseCallback("Mark the head and feet", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def calculate_height(positions, img, focal_length):
    D_real = 1 #default distance 
    
    head_point, feet_point = positions
    h_image = abs(feet_point[1] - head_point[1])  
    
    sensor_height_mm = 10.16 #for my redmi 8 mobile

    H_image = img.shape[0]  
    
    focal_length_pixels = (focal_length / sensor_height_mm) * H_image
    
    H_real = (h_image * D_real) / focal_length_pixels
    
    messagebox.showinfo("Height Calculation", f"The calculated real-world height is: {H_real:.2f} meters")


def create_gui():
    root = tk.Tk()
    root.title("Height Estimation")
    btn = tk.Button(root, text="Select Image and Mark Points", command=capture_image_and_mark_points)
    btn.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    create_gui()
