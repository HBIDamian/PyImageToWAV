import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import wave
import os
import webbrowser
import numpy as np

class imageToWAVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("imageToWAV Converter")
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
        title_label = tk.Label(root, text="Image to WAV Converter", font=self.title_font, pady=20, bg="#2E2E2E", fg="white")
        title_label.pack()

        # File Input Section
        file_frame = tk.LabelFrame(root, text="File Selection", font=self.label_font, bg=self.frame_bg, fg="#ffffff", padx=20, pady=10)
        file_frame.pack(fill="x", padx=20, pady=10, anchor="center")

        self.create_label_entry_button(file_frame, "Image File:", self.browse_file, 0)
        self.create_label_entry_button(file_frame, "Output Directory:", self.browse_folder, 1)

        # Options Section
        options_frame = tk.LabelFrame(root, text="Options", font=self.label_font, bg=self.frame_bg, fg="#ffffff", padx=20, pady=10)
        options_frame.pack(fill="x", padx=20, pady=10, anchor="center")

        self.low_sample_rate = tk.BooleanVar(value=True)
        self.add_checkbox(options_frame, "Sample Rate: 44.1 kHz", var=self.low_sample_rate, command=self.update_sample_rate_label, row=0, width=18, anchor="w")
        self.create_label_spinner(options_frame, "Filter Size:", 1, 200, 4, 1)
        self.create_label_spinner(options_frame, "Channel Count:", 1, 8, 1, 2)
        self.create_label_spinner(options_frame, "Stretch Factor:", 1, 200, 11, 3)

        # Action Button
        self.convert_button = tk.Button(root, text="Convert to WAV", command=self.convert_to_wav,
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
        if text.startswith("Image"):
            self.file_entry = entry
        else:
            self.output_entry = entry

        entry.bind("<Key>", lambda e: "break")

        button = tk.Button(frame, text="Browse", command=command, font=self.button_font, bg="#007BFF", fg="white", width=10)
        button.grid(row=row, column=2, padx=10, pady=5)



    def add_checkbox(self, frame, text, var, command, row, width=None, anchor=None):
        checkbox = tk.Checkbutton(frame, text=text, variable=var, font=self.label_font, bg=self.frame_bg, fg="#ffffff", 
                                selectcolor="#2E2E2E", activebackground=self.frame_bg, activeforeground="#ffffff",
                                command=command, width=width, anchor=anchor)
        checkbox.grid(row=row, column=0, columnspan=3, sticky="w", pady=5)
        self.low_sample_rate_label = checkbox

    def create_label_spinner(self, frame, text, from_, to, default, row):
        label = tk.Label(frame, text=text, font=self.label_font, bg=self.frame_bg, fg="#ffffff")
        label.grid(row=row, column=0, sticky="w", pady=5)

        spinner = tk.Spinbox(frame, from_=from_, to=to, width=5, font=self.label_font, bd=2, relief="solid")
        spinner.grid(row=row, column=1, sticky="w", padx=10, pady=5)

        if text.startswith("Filter"):
            self.filter_size_spinner = spinner
        elif text.startswith("Channel"):
            self.channel_count_spinner = spinner
        elif text.startswith("Stretch"):
            self.stretch_spinner = spinner

        spinner.delete(0, "end")
        spinner.insert(0, default)

    def add_info_help_buttons(self, frame):
        buttons_frame = tk.Frame(frame, bg="#2E2E2E")
        buttons_frame.pack(side="bottom", anchor="center")  # Center buttons

        tk.Button(buttons_frame, text="Information", command=self.show_info, font=self.button_font, bg="#2196F3", fg="white", width=12).pack(side="left", padx=10, pady=5)
        tk.Button(buttons_frame, text="YouTube Explanation", command=self.open_youtube, font=self.button_font, bg="#2196F3", fg="white", width=18).pack(side="left", padx=10, pady=5)
        tk.Button(buttons_frame, text="Help", command=self.show_help, font=self.button_font, bg="#2196F3", fg="white", width=12).pack(side="left", padx=10, pady=5)

    def update_sample_rate_label(self):
        text = "Sample Rate: 44.1 kHz" if self.low_sample_rate.get() else "Sample Rate: 48 kHz"
        self.low_sample_rate_label.config(text=text)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Image Files", "*.bmp;*.dib;*.rle;*.jpg;*.jpeg;*.jpe;*.jfif;*.gif;*.tif;*.tiff;*.png"),
            ("All Files", "*.*")
        ])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder_path)

    def convert_to_wav(self):
        file_path = self.file_entry.get()
        output_dir = self.output_entry.get()

        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Image file not found!")
            return

        if not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Output directory not found!")
            return

        try:
            # Process image
            img = Image.open(file_path).convert("L")
            width, height = img.size
            values = []

            for x in range(width):
                column = img.crop((x, 0, x + 1, height))
                column_data = np.array(column)
                bright_pixels = np.where(column_data > 128)[0]

                if bright_pixels.size > 0:
                    min_y = bright_pixels.min()
                    max_y = bright_pixels.max()
                else:
                    min_y = height
                    max_y = 0

                values.append(min_y)
                values.append(max_y)
            
            # Add a delay to the end of the audio
            values.extend([0] * 2000)

            # Smoothing
            filter_size = int(self.filter_size_spinner.get())
            smoothed_values = np.convolve(values, np.ones(filter_size) / filter_size, mode='valid')

            # Normalize
            smoothed_values = (smoothed_values - np.min(smoothed_values)) / (np.max(smoothed_values) - np.min(smoothed_values)) * 255

            # Write WAV file
            filename = os.path.splitext(os.path.basename(file_path))[0] + ".wav"
            output_path = os.path.join(output_dir, filename)

            sample_rate = 44100 if self.low_sample_rate.get() else 48000
            stretch = int(self.stretch_spinner.get())
            channel_count = int(self.channel_count_spinner.get())

            with wave.open(output_path, "w") as wav_file:
                wav_file.setnchannels(channel_count)
                wav_file.setsampwidth(1) # All values are in the 
                wav_file.setframerate(sample_rate)
                wav_file.setnframes(len(smoothed_values) * stretch)
                wav_file.setcomptype("NONE", "not compressed")
                wav_file.setparams((channel_count, 1, sample_rate, len(smoothed_values) * stretch, "NONE", "not compressed"))

                for value in smoothed_values:
                    wav_file.writeframes(bytes([int(value)] * stretch))

            messagebox.showinfo("Success", f"WAV file saved at: {output_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_info(self):
        info_text = (
            "Recreate audio from a wav file preview image. \n\n"
            "This program converts an image to a WAV file.\n"
            "The image must be white on a black background.\n\n"
            "Based on the work of David Domminney Fowler,\n\tunder the MIT licence.\n\n"
            "Rewritten to Python by @HBIDamian"
        )

        messagebox.showinfo("Information", info_text)

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com/watch?v=VQOdmckqNro")

    def show_help(self):
        help_text = (
            "File Selection:\n"
            "  - Image File: Select the image to process.\nThe image must be white on a black background.\n"
            "  - Output Directory: Choose where to save the WAV file.\n\n"
            "Options:\n"
            "  - Sample Rate: Select between 44.1 kHz or 48 kHz.\n"
            "  - Filter Size: Adjusts smoothing of the audio waveform.\n"
            "  - Channel Count: Sets the number of audio channels.\n"
            "  - Stretch Factor: Changes the duration of the audio."
        )
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = imageToWAVApp(root)
    root.mainloop()
