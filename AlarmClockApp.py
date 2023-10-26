import datetime
import threading
import time
import tkinter as tk
import winsound
from tkinter import messagebox, ttk

from pytz import timezone


class Alarm:
    def __init__(self, master):
        self.master = master
        self.alarm_time = None
        self.alarm_active = False
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.master, text="Enter alarm time (HH:MM:SS):", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.master, font=("Arial", 14))
        self.entry.pack(pady=10)

        self.set_alarm_button = ttk.Button(self.master, text="Set Alarm", command=self.set_alarm, style="TButton")
        self.set_alarm_button.pack(pady=10)

        self.deactivate_button = ttk.Button(self.master, text="Deactivate", command=self.deactivate_alarm, state=tk.DISABLED, style="TButton")
        self.deactivate_button.pack(pady=10)

    def set_alarm(self):
        try:
            alarm_time_str = self.entry.get()
            self.alarm_time = datetime.datetime.strptime(alarm_time_str, "%H:%M:%S")
            self.alarm_active = True
            self.set_alarm_button.config(state=tk.DISABLED)
            self.deactivate_button.config(state=tk.NORMAL)
            self.run_alarm_thread()
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM:SS.")

    def run_alarm_thread(self):
        while self.alarm_active:
            current_time = datetime.datetime.now().time()
            if current_time >= self.alarm_time.time():
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                messagebox.showinfo("Alarm", "Time to wake up!")
                self.alarm_active = False
            time.sleep(1)

    def deactivate_alarm(self):
        self.alarm_active = False
        self.set_alarm_button.config(state=tk.NORMAL)
        self.deactivate_button.config(state=tk.DISABLED)

class Timer:
    def __init__(self, master, app_instance):
        self.master = master
        self.app_instance = app_instance
        self.timer_duration = 0
        self.timer_active = False
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.master, text="Set timer (in seconds):", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.master, font=("Arial", 14))
        self.entry.pack(pady=10)

        self.start_timer_button = ttk.Button(self.master, text="Start Timer", command=self.start_timer, style="TButton")
        self.start_timer_button.pack(pady=10)

    def start_timer(self):
        try:
            self.timer_duration = int(self.entry.get())
            if self.timer_duration < 0:
                messagebox.showerror("Error", "Timer duration must be a positive integer.")
                return

            self.timer_active = True
            self.run_timer_thread()
        except ValueError:
            messagebox.showerror("Error", "Invalid timer duration. Please enter a valid integer.")

    def run_timer_thread(self):
        for i in range(self.timer_duration, 0, -1):
            if not self.timer_active:
                break
            time.sleep(1)
        if self.timer_active:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            messagebox.showinfo("Timer", "Timer completed!")
            self.app_instance.log_exit_time()  # Log exit time after timer completion

class Stopwatch:
    def __init__(self, master):
        self.master = master
        self.stopwatch_running = False
        self.start_time = None
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.master, text="Stopwatch:", font=("Arial", 14))
        self.label.pack(pady=5)

        self.stopwatch_display = ttk.Label(self.master, text="00:00:00", font=("Arial", 20))
        self.stopwatch_display.pack(pady=5)

        self.start_stopwatch_button = ttk.Button(self.master, text="Start", command=self.start_stopwatch, style="TButton")
        self.start_stopwatch_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.stop_stopwatch_button = ttk.Button(self.master, text="Stop", command=self.stop_stopwatch, state=tk.DISABLED, style="TButton")
        self.stop_stopwatch_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.reset_stopwatch_button = ttk.Button(self.master, text="Reset", command=self.reset_stopwatch, style="TButton")
        self.reset_stopwatch_button.pack(side=tk.LEFT, padx=10, pady=5)

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.start_time = time.time()
            self.stopwatch_running = True
            self.update_stopwatch()

            self.start_stopwatch_button.config(state=tk.DISABLED)
            self.stop_stopwatch_button.config(state=tk.NORMAL)

    def stop_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_running = False
            self.start_stopwatch_button.config(state=tk.NORMAL)
            self.stop_stopwatch_button.config(state=tk.DISABLED)

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.start_time = None
        self.stopwatch_display.config(text="00:00:00")
        self.start_stopwatch_button.config(state=tk.NORMAL)
        self.stop_stopwatch_button.config(state=tk.DISABLED)

    def update_stopwatch(self):
        if self.stopwatch_running:
            elapsed_time = time.time() - self.start_time
            formatted_time = str(datetime.timedelta(seconds=int(elapsed_time)))
            self.stopwatch_display.config(text=formatted_time)
        self.master.after(1000, self.update_stopwatch)

class WorldClocks:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        london_label = ttk.Label(self.master, text="London Time:", font=("Arial", 14))
        london_label.pack(pady=5)

        self.london_time_label = ttk.Label(self.master, font=("Arial", 16))
        self.london_time_label.pack(pady=5)

        usa_label = ttk.Label(self.master, text="USA (New York) Time:", font=("Arial", 14))
        usa_label.pack(pady=5)

        self.usa_time_label = ttk.Label(self.master, font=("Arial", 16))
        self.usa_time_label.pack(pady=5)

        self.update_world_clocks()

    def update_world_clocks(self):
        london_time = self.get_time_in_timezone('Europe/London')
        usa_time = self.get_time_in_timezone('America/New_York')

        self.london_time_label.config(text=london_time)
        self.usa_time_label.config(text=usa_time)

        self.master.after(1000, self.update_world_clocks)

    def get_time_in_timezone(self, tz_name):
        tz = timezone(tz_name)
        time_now = datetime.datetime.now(tz)
        return time_now.strftime('%Y-%m-%d %H:%M:%S')

class AlarmClockApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Alarm Clock App")
        self.master.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)

        alarm_tab = ttk.Frame(self.notebook)
        timer_tab = ttk.Frame(self.notebook)
        stopwatch_tab = ttk.Frame(self.notebook)
        world_clocks_tab = ttk.Frame(self.notebook)

        self.notebook.add(alarm_tab, text="Alarm")
        self.notebook.add(timer_tab, text="Timer")
        self.notebook.add(stopwatch_tab, text="Stopwatch")
        self.notebook.add(world_clocks_tab, text="World Clocks")

        self.notebook.pack(expand=True, fill=tk.BOTH)

        Alarm(alarm_tab)
        Timer(timer_tab, self)  # Pass the app instance to Timer
        Stopwatch(stopwatch_tab)
        WorldClocks(world_clocks_tab)

    def log_exit_time(self):
        print("Timer completed. Logging exit time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()
