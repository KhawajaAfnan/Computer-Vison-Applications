import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

def linear_interpolation(image, K):
    orig_height, orig_width, channels = image.shape
    new_height = orig_height * K
    new_width = orig_width * K
    
    image = image.astype(np.float32)
    interpolated_image = np.zeros((new_height, new_width, channels), dtype=np.float32)

    for i in range(orig_height):
        for j in range(orig_width):
            for c in range(channels):
                interpolated_image[i * K, j * K, c] = image[i, j, c]

    # Horizontal 
    for i in range(orig_height):
        for j in range(orig_width - 1):
            for c in range(channels):
                start_value = image[i, j, c]
                end_value = image[i, j + 1, c]
                step = (end_value - start_value) / K
                for k in range(1, K):
                    interpolated_image[i * K, j * K + k, c] = start_value + step * k

    # Vertical 
    for i in range(orig_height - 1):
        for j in range(new_width):
            for c in range(channels):
                start_value = interpolated_image[i * K, j, c]
                end_value = interpolated_image[(i + 1) * K, j, c]
                step = (end_value - start_value) / K
                for k in range(1, K):
                    interpolated_image[i * K + k, j, c] = start_value + step * k

    interpolated_image = np.clip(interpolated_image, 0, 255).astype(np.uint8)
    return interpolated_image

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img_np = np.array(img)
        return img_np, img
    return None, None

def display_image(root, image, title):
    img = Image.fromarray(image.astype('uint8'))
    img_tk = ImageTk.PhotoImage(img)

    window = tk.Toplevel(root)
    window.title(title)

    label = tk.Label(window, image=img_tk)
    label.image = img_tk
    label.pack()

def main():
    ogImage = open_image()
    if ogImage is None:
        return

    K = simpledialog.askinteger("Input", "Enter the enlargement factor K (e.g., 2, 3):")
    if not K or K <= 1:
        print("Invalid enlargement factor.")
        return

    enlarged_image = linear_interpolation(ogImage, K)
    display_image(root, ogImage, "Original Image")
    display_image(root, enlarged_image, "Linear Interpolated Image")

root = tk.Tk()
root.title("CV ASSIGNMENT 1")
root.geometry("400x400")

button = tk.Button(root, text="Open Image", command=main)
button.pack(expand=True)

root.mainloop()
