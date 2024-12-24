import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

def enlarge(image, factor):
    orig_height, orig_width, channels = image.shape
    new_height = orig_height * factor
    new_width = orig_width * factor
    enlarged_image = np.zeros((new_height, new_width, channels), dtype=np.float32)

    for i in range(orig_height):
        for j in range(orig_width):
            for c in range(channels):
                enlarged_image[i * factor, j * factor, c] = image[i, j, c]

    enlarged_image = np.clip(enlarged_image, 0, 255).astype(np.uint8)
    return enlarged_image


def convolution(image, kernel, mode='zero'):
    orig_height, orig_width, channels = image.shape
    kernel_height, kernel_width = kernel.shape

    output_image = np.zeros_like(image, dtype=np.float32)
    
    for c in range(channels):
        for i in range(orig_height):
            for j in range(orig_width):
                if (i + kernel_height > orig_height) or (j + kernel_width > orig_width):
                    continue

                region = image[i:i+kernel_height, j:j+kernel_width, c]

                pixel_value = np.sum(region * kernel)
                
                if mode == 'zero':
                    output_image[i, j, c] = pixel_value
                elif mode == 'first':
                    output_image[i, j, c] = pixel_value

    output_image = np.clip(output_image, 0, 255).astype(np.uint8)
    return output_image

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
    ogImage, original_image = open_image()
    if ogImage is None:
        return


    factor = simpledialog.askinteger("Input", "Enter the enlargement factor (e.g., 2, 3):")
    if not factor or factor <= 1:
        print("Invalid enlargement factor.")
        return

    enlarged_image = ogImage

    for _ in range(factor - 1):
        zeroEnlarge = enlarge(enlarged_image, 2)
        zerokernel = np.array([[1, 1], [1, 1]])
        zeroConvoluted = convolution(zeroEnlarge, zerokernel, mode='zero')
        

        firstEnlarge = enlarge(enlarged_image, 2)
        firstkernel = np.array([[1/4, 1/2, 1/4], [1/2, 1, 1/2], [1/4, 1/2, 1/4]])
        firstConvoluted = convolution(firstEnlarge, firstkernel, mode='first')

      

        

    display_image(root, ogImage, "Original Image")
    display_image(root, zeroConvoluted, "Zero-Order Hold Convoluted Image")
    display_image(root, firstConvoluted, "First-Order Hold Convoluted Image")

root = tk.Tk()
root.title("CV ASSIGNMENT 1")
root.geometry("400x400")

button = tk.Button(root, text="Open Image", command=main)
button.pack(expand=True)

root.mainloop()
