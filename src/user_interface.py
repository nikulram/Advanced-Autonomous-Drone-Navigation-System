import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class DroneControlPanel:
    def __init__(self, master):
        self.master = master
        master.title("Drone Control Panel")

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        self.label = ttk.Label(master, text="Drone Navigation and Swarm System")
        self.label.grid(columnspan=2, row=0, sticky=tk.EW)

        self.start_button = ttk.Button(master, text="Start All Drones", command=self.start_all_drones)
        self.start_button.grid(row=1, column=0, sticky=tk.EW)
        self.stop_button = ttk.Button(master, text="Stop All Drones", command=self.stop_all_drones)
        self.stop_button.grid(row=1, column=1, sticky=tk.EW)

        self.status = tk.StringVar()
        self.status.set("Status: Idle")
        self.status_label = ttk.Label(master, textvariable=self.status)
        self.status_label.grid(columnspan=2, row=2, sticky=tk.EW)

        self.live_data_display = scrolledtext.ScrolledText(master, height=10)
        self.live_data_display.grid(columnspan=2, row=3, sticky=tk.EW)

        self.advanced_frame = ttk.LabelFrame(master, text="Advanced Controls and Overrides", padding=10)
        self.advanced_frame.grid(columnspan=2, row=4, sticky=tk.EW)
        ttk.Button(self.advanced_frame, text="Emergency Override", command=self.emergency_override).pack(expand=True, fill=tk.BOTH)
        ttk.Button(self.advanced_frame, text="Weather Updates", command=self.display_weather).pack(expand=True, fill=tk.BOTH)
     #start all drones
    def start_all_drones(self):
        self.status.set("Status: All Drones Started")
        self.log_data("All drones start sequence initiated.")

     #stop all drones
    def stop_all_drones(self):
        self.status.set("Status: All Drones Stopped")
        self.log_data("All drones stop sequence initiated.")
     
     #configure all drones
    def configure_drone(self):
        self.log_data("Drone configuration settings opened.")

     #log data
    def log_data(self, message):
        self.live_data_display.insert(tk.END, message + '\n')
        self.live_data_display.yview(tk.END)

     #emergency overriding  
    def emergency_override(self):
        response = messagebox.askyesno("Emergency Override", "Do you want to override and continue the mission?")
        if response:
            self.log_data("User has overridden the emergency protocol.")
        else:
            self.log_data("User has upheld the emergency protocol.")

    def display_weather(self):
        self.log_data("Weather update displayed.")

if __name__ == "__main__":
    root = tk.Tk()
    panel = DroneControlPanel(root)
    root.mainloop()
