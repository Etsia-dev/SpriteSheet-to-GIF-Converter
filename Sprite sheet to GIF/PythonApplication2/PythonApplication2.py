import os
from glob import glob
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

# Sprite sheet frame extraction
def CalculateFrames(sheet):
    frame_size = sheet.height
    num_frames = sheet.width // frame_size
    frames = []
    for i in range(num_frames):
        box = (i * frame_size, 0, (i + 1) * frame_size, frame_size)
        frame = sheet.crop(box).convert("RGBA")
        frames.append(frame)
    return frames, num_frames

# Save sprite frames to animated GIF
def SaveFramesToGif(frames, output_path, duration=100):
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        disposal=2
    )

# List files in folder
def list_files(folder):
    files = glob(os.path.join(folder, "*.png"))
    file_list.delete(0, tk.END)
    for f in files:
        file_list.insert(tk.END, os.path.basename(f))
    return files

# Play animated GIF in tkinter, you can disable this if you have a lot of files to run
def play_gif(filepath, row, col):
    img = Image.open(filepath)
    frames = []

    try:
        while True:
            frame = ImageTk.PhotoImage(img.copy())
            frames.append(frame)
            img.seek(len(frames))
    except EOFError:
        pass

    panel = tk.Label(gif_frame)
    panel.grid(row=row, column=col, padx=5, pady=5)

    def update(index=0):
        frame = frames[index]
        panel.config(image=frame)
        panel.image = frame
        root.after(100, update, (index + 1) % len(frames))

    update()

# Main conversion process
def run_conversion():
    files = list_files("input images") # input file name
    if not files:
        messagebox.showerror("Error", "No .png files found in this folder.")
        return

    output_folder = "output gifs" # output file name
    os.makedirs(output_folder, exist_ok=True)

    file_list.delete(0, tk.END)

    for i, filepath in enumerate(files):
        sheet = Image.open(filepath)
        frames, num_frames = CalculateFrames(sheet)

        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_path = os.path.join(output_folder, f"{base_name}.gif")

        SaveFramesToGif(frames, output_path, duration=100)

        play_gif(output_path, row=i // 4, col=i % 4)

        file_list.insert(
            tk.END,
            f"{base_name}: {num_frames} frames -> {base_name}.gif saved"
        )

    messagebox.showinfo("Done", f"All GIFs saved in '{output_folder}'")

# GUI setup
root = tk.Tk()
root.title("Sprite Sheet to GIF")
file_list = tk.Listbox(root, width=60, height=10)
file_list.pack(padx=10, pady=5)
tk.Button(root, text="Run", command=run_conversion).pack(pady=10)
gif_frame = tk.Frame(root)
gif_frame.pack(padx=10, pady=10)

list_files("input images") # input file name

root.mainloop()
