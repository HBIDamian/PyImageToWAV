import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance
import subprocess
from subprocess import DEVNULL
import os
import numpy as np

class AudioToWaveformApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio to Waveform Converter")
        self.root.geometry("820x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#2E2E2E")  # Dark background color

        # Styling
        self.label_font = ("Arial", 14)
        self.button_font = ("Arial", 12, "bold")
        self.title_font = ("Arial", 28, "bold")
        self.frame_bg = "#3E3E3E"  # Dark background for frames
        self.button_bg = "#4CAF50"
        self.button_fg = "white"
        self.entry_bg = "#555555"  # Dark background for entries
        self.entry_fg = "white"  # Light text color for entries

        # Title Section
        title_label = tk.Label(root, text="Audio to Waveform Converter", font=self.title_font, pady=20, bg="#2E2E2E", fg="white")
        title_label.pack()

        # File Input Section
        file_frame = tk.LabelFrame(root, text="File Selection", font=self.label_font, bg=self.frame_bg, fg="#ffffff", padx=20, pady=10)
        file_frame.pack(fill="x", padx=20, pady=10, anchor="center")

        self.create_label_entry_button(file_frame, "Audio File:", self.browse_file, 0)
        self.create_label_entry_button(file_frame, "Output Directory:", self.browse_folder, 1)

        # Action Button
        self.convert_button = tk.Button(root, text="Convert to Waveform", command=self.convert_to_waveform,
                                         font=self.button_font, bg=self.button_bg, fg=self.button_fg, width=20, height=2)
        self.convert_button.pack(pady=20, anchor="center")

        # Info and Help Buttons
        info_frame = tk.Frame(root, bg="#2E2E2E")
        info_frame.pack(fill="x", padx=20, pady=10, anchor="center")

        self.add_info_help_buttons(info_frame)

    def create_label_entry_button(self, frame, text, command, row):
        label = tk.Label(frame, text=text, font=self.label_font, bg=self.frame_bg, fg="#ffffff")
        label.grid(row=row, column=0, sticky="w", pady=5)

        entry = tk.Entry(frame, width=40, font=self.label_font, bd=2, relief="solid", bg=self.entry_bg, fg=self.entry_fg)
        entry.grid(row=row, column=1, padx=10, pady=5)
        if text.startswith("Audio"):
            self.audio_entry = entry
        else:
            self.output_entry = entry

        # Prevent typing in the entry by binding the key events
        entry.bind("<Key>", lambda e: "break")

        button = tk.Button(frame, text="Browse", command=command, font=self.button_font, bg="#007BFF", fg="white", width=10)
        button.grid(row=row, column=2, padx=10, pady=5)

    def add_info_help_buttons(self, frame):
        buttons_frame = tk.Frame(frame, bg="#2E2E2E")
        buttons_frame.pack(side="bottom", anchor="center")  # Center buttons

        tk.Button(buttons_frame, text="Information", command=self.show_info, font=self.button_font, bg="#2196F3", fg="white", width=12).pack(side="left", padx=10, pady=5)
        tk.Button(buttons_frame, text="Help", command=self.show_help, font=self.button_font, bg="#2196F3", fg="white", width=12).pack(side="left", padx=10, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Audio Files", "*.wav;*.mp3;*.flac;*.ogg;*.aac"),
            ("All Files", "*.*")
        ])
        if file_path:
            self.audio_entry.delete(0, tk.END)
            self.audio_entry.insert(0, file_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder_path)

        

    def convert_to_waveform(self):
        audio_file = self.audio_entry.get()  # Output Example: C:/Users/username/Desktop/audio.mp3
        output_dir = self.output_entry.get()

        originalNameFileNoExtension = os.path.splitext(os.path.basename(audio_file))[0]
        # Messagebox for debugging

        if not os.path.exists(audio_file):
            messagebox.showerror("Error", "Audio file not found!")
            return

        if not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Output directory not found!")
            return

        try:
            waveform_image_path = os.path.join(output_dir, originalNameFileNoExtension + ".jpg")

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            command = [
                'ffmpeg',
                '-i', audio_file,
                '-filter_complex', 'aformat=channel_layouts=mono,showwavespic=s=1920x480:colors=#ffffff',
                '-frames:v', '1',
                '-y',  # Overwrite output if exists
                waveform_image_path
            ]
            
            # Run the command and suppress the standard output and error output
            subprocess.run(command, check=True, stdout=DEVNULL, stderr=DEVNULL) 

            img = Image.open(waveform_image_path)
            img = img.convert("RGB")

            img = img.convert("L")  # Convert to grayscale

            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2) 

            # Save the enhanced grayscale image as PNG to maintain high quality
            output_png_path = os.path.splitext(waveform_image_path)[0] + "_waveform.png"
            img.save(output_png_path, "PNG", quality=100) 

            os.remove(waveform_image_path)

            messagebox.showinfo("Success", f"Waveform image saved at: {output_png_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def show_info(self):
        messagebox.showinfo("Information", "Convert audio into a waveform image. \n\nThis project uses ffmpeg to generate the waveform, which is then processed to ensure the output is a white waveform on a black background.")

    def show_help(self):
        help_text = (
            "File Selection:\n"
            "  - Audio File: Select the audio file to process.\n"
            "  - Output Directory: Choose where to save the waveform image.\n\n"
            "Options:\n"
            "  - The generated image will be a white waveform on a black background, with pixelated/blocky edges."
        )
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioToWaveformApp(root)
    root.mainloop()
