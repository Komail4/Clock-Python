import tkinter
import time
import datetime
from tkinter import messagebox, ttk

# Frame 1 - Stopwatch Page
class Stopwatch(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.start_time = None
        self.elapsed_time = 0
        self.time_label = ttk.Label(self, font=("Arial", 24), text="00:00:00")
        self.time_label.pack(pady=50)

        # Add control buttons
        self.button_frame = tkinter.Frame(self)
        self.button_frame.pack(pady=10)

        self.start_btn = ttk.Button(self.button_frame, text="Start", command=self.start)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ttk.Button(self.button_frame, text="Stop", command=self.stop)
        self.stop_btn.pack(side="left", padx=5)

        self.reset_btn = ttk.Button(self.button_frame, text="Reset", command=self.reset)
        self.reset_btn.pack(side="left", padx=5)

    def start(self):
        if self.start_time is None:
            self.start_time = time.time()
            self.update_time()
    def stop(self):
        if self.start_time is not None:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None
    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.update_time()
    def update_time(self):
        if self.start_time is not None:
            current_time = time.time() - self.start_time + self.elapsed_time
        else:
            current_time = self.elapsed_time
        minutes, seconds = divmod(current_time, 60)
        hours, minutes = divmod(minutes, 60)
        self.time_label.config(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")
        self.after(1000, self.update_time)
    
# Frame 2 - Timer Page
class Timer(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.frame_button = tkinter.Frame(self)

        self.label_set_time = ttk.Label(self, text="Set Timer", font=("Arial", 16))
        self.label_time_format = ttk.Label(self, text="Format: HH:MM:SS", font=("Arial", 10))
        self.entry_timer = ttk.Entry(self, width=10, font=("Arial", 16), justify='center')
        self.entry_timer.insert(0, "00:00:00")
        self.button_start = ttk.Button(self, text = "Start", width=10, command=self.start)

        self.label_timer = ttk.Label(self, font=("Arial", 24), text="00:00:00")
        self.button_pause = ttk.Button(self.frame_button, text = "Pause", width=9, command=self.pause)
        self.button_pause.pack(side="left", padx=10)
        self.button_cancel = ttk.Button(self.frame_button, text="Cancel", width=9, command=self.cancel)
        self.button_cancel.pack(side="left", padx=5)
        self.button_continue = ttk.Button(self.frame_button, text="Continue", width=9, command=self.continue_time)
        self.button_continue.pack(side="left", padx=10)

        self.set_timer_page()
    
        self.timer_running = False
        self.paused = False
        self.remaining_seconds = 0
        self.timer_id = None        
    
    def start(self):
        try:
            time_str = self.entry_timer.get()
            hours, minutes, seconds = map(int, time_str.split(':'))
            total_seconds = hours * 3600 + minutes * 60 + seconds
            if total_seconds <= 0:
                raise ValueError("Time must be greater than zero.")
            self.remaining_seconds = total_seconds
            self.paused = False
            self.timer_running = True
            self.update_timer()
            self.start_timer_page()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid time in HH:MM:SS format.")

    def update_timer(self):
        if self.timer_running and not self.paused:
            if self.remaining_seconds > 0:
                hours, rem = divmod(self.remaining_seconds, 3600)
                minutes, seconds = divmod(rem, 60)
                self.label_timer.config(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")
                self.remaining_seconds -= 1
                self.timer_id = self.after(1000, self.update_timer)
            else:
                self.label_timer.config(text="00:00:00")
                self.timer_running = False
                messagebox.showinfo("Time's up!", "Timer finished!")
                self.set_timer_page()

    def pause(self):
        if self.timer_running and not self.paused:
            self.paused = True
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None

    def continue_time(self):
        if self.timer_running and self.paused:
            self.paused = False
            self.update_timer()

    def cancel(self):
        self.timer_running = False
        self.paused = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.label_timer.config(text="00:00:00")
        self.set_timer_page()

    def set_timer_page(self):
        self.label_set_time.pack(pady=10)
        self.label_time_format.pack()
        self.entry_timer.pack()
        self.button_start.pack(pady=20)
        self.label_timer.pack_forget()
        self.frame_button.pack_forget()

    def start_timer_page(self):
        self.label_set_time.pack_forget()
        self.label_time_format.pack_forget()
        self.entry_timer.pack_forget()
        self.button_start.pack_forget()
        self.label_timer.pack(pady=30)
        self.frame_button.pack()

class ClockDate(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.date = ttk.Label(self, font=("Arial", 24))
        self.date.pack(pady=20)
        self.clock = ttk.Label(self, font=("Arial", 24))
        self.clock.pack(pady=20)
        self.update_time()
    def update_time(self):
        self.date_now = datetime.datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.datetime.now().strftime("%H:%M:%S")
        self.date.config(text=f"Date: {self.date_now}")
        self.clock.config(text=f"Time: {self.time}")
        self.after(1000, self.update_time)
        
# Main App
class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stopwatch - Timer")
        self.geometry("260x185")

        # Container to hold all frames
        self.container = tkinter.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}  # Store page instances here

        # Initialize all frames once
        for F in (Stopwatch, Timer, ClockDate):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_menu()
        self.show_frame("ClockDate")

    def create_menu(self):
        menubar = tkinter.Menu(self)
        main_menu = tkinter.Menu(menubar, tearoff=0)

        main_menu.add_command(label="Clock-Date", command=lambda: self.show_frame("ClockDate"))
        main_menu.add_command(label="Stopwatch", command=lambda: self.show_frame("Stopwatch"))
        main_menu.add_command(label="Timer", command=lambda: self.show_frame("Timer"))

        menubar.add_cascade(label="Menu", menu=main_menu)
        self.config(menu=menubar)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()