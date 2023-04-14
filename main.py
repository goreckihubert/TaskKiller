import subprocess
import pygetwindow
import win32api
import win32con
import threading
import tkinter as tk
from PIL import Image, ImageTk

process_name = "notepad++.exe"
inactive_time = 15  # seconds


class NotepadKillerApp:
    def __init__(self):
        self.killer_thread = None
        self.is_running = False
        self.window = tk.Tk()
        self.window.title("Notepad Killer")
        self.window.geometry("300x90")

        # load the image
        img = Image.open("C:/Users/HUBERT/PycharmProjects/TaskKiller/ezgif.com-resize.gif")
        img = img.resize((300, 90), Image.LANCZOS)
        image = ImageTk.PhotoImage(img)

        # create a label with the image as the background
        background_label = tk.Label(self.window, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # keep a reference to the image to prevent garbage collection,
        background_label.image = image

        # Create a label to display the status of the app
        self.status_label = tk.Label(self.window, text="Mam Cie w dupie", bg="", font=("Noto Serif", 16), fg="red")
        self.status_label.pack(side="top")
        self.status_label1 = tk.Label(self.window, bg="", text="", fg="green")
        self.status_label1.pack(side="top")

        # Create a frame to hold the start and stop buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(side="bottom")

        start_button = tk.Button(button_frame, text="Start", command=self.start_killer)
        start_button.pack(side="left")

        stop_button = tk.Button(button_frame, text="Stop", command=self.stop_killer)
        stop_button.pack(side="right")

    def start_killer(self):
        self.is_running = True
        self.status_label.config(text="Czuwam", fg="green")  # Set the label to green
        self.killer_thread = threading.Thread(target=self.kill_notepad_when_inactive)
        self.killer_thread.start()

    def stop_killer(self):
        self.is_running = False
        self.status_label.config(text="Mam Cie w dupie", fg="red")  # Set the label to red

    def kill_notepad_when_inactive(self):
        while self.is_running:
            active_window = pygetwindow.getActiveWindow()
            last_input_time = win32api.GetLastInputInfo() / 1000

            if (win32api.GetTickCount() / 1000) - last_input_time > inactive_time:
                try:
                    subprocess.run(["taskkill", "/f", "/im", process_name], check=True)
                    print(f"Proces {process_name} ujebany")
                    self.status_label1.config(text="Proces Ujebany", fg="green")  # Set the label to green
                except subprocess.CalledProcessError as e:
                    print(f"Error killing process {process_name}: {e}")
            self.window.update()


app = NotepadKillerApp()
app.window.mainloop()
