from tkinter import messagebox
from tkinter import filedialog
from pygame import mixer
import tkinter as tk
import threading
import psutil
import time
import sys
import os

class BatteryMonitorApp:
    
    def get_current_percentage(self):
        battery = psutil.sensors_battery()
        if battery:
            return battery.percent
        return 0

    def __init__(self):
        self.root = tk.Tk()
        iconPath = self.resource_path("Battery.ico")
        self.root.title("Battery Monitoring App") # Title
        self.root.geometry("450x300") # App dimentions
        self.is_monitoring = False
        self.charge_level_thread = None

        #Define Application Variables
        current_percentage = self.get_current_percentage()
        suggested_percentage = 100

        # Calculate the suggested percentage
        if current_percentage <= 50:
            suggested_percentage = 100 - current_percentage
        else:
            suggested_message = "It is not recommended to start charging on a higher than 50% state of charge."

        #region Top 

        # Create a frame for the top section of the window
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.charge_label = tk.Label(top_frame, text=f"Charge Level: {self.get_current_percentage()}%")        
        self.charge_label.pack() #Display the battery percentage when the app onened#

        if current_percentage <= 50:
            suggested_percentage_Label = tk.Label(top_frame, text="Suggested percentage: "+ f"{suggested_percentage}%")
            suggested_percentage_Label.pack()    
        else:
            suggested_messageLabel = tk.Label(top_frame, text= f"{suggested_message}", fg= "red")
            suggested_messageLabel.pack()

        self.label = tk.Label(top_frame, text="Desired charging percentage: ")
        self.label.pack(side=tk.LEFT, padx=10)

        self.percentage_slider = tk.Scale(top_frame, from_=0, to=100, orient=tk.HORIZONTAL)
                                          #command=self.update_charge_level)
        self.percentage_slider.set(suggested_percentage)
        self.percentage_slider.pack(side=tk.LEFT, padx=10)

        self.suggested_percentage_label = tk.Label(top_frame, text=f"{suggested_percentage}%")
        self.suggested_percentage_label.pack(side=tk.LEFT)
        #endregion

        #region Middle
        # Create a frame for the middle section of the window
        middle_frame = tk.Frame(self.root)
        middle_frame.pack(pady=10)

        # Initialize play_sound_var and show_popup_var with default values
        self.play_sound_var = tk.IntVar(value=0)
        self.show_popup_var = tk.IntVar(value=1)  # Set to 1 to have it checked by default

        # Label to display "When charged:"
        when_charged_label = tk.Label(middle_frame, text="When charged:")
        when_charged_label.pack(side=tk.TOP, padx=10)

        self.play_sound_checkbox = tk.Checkbutton(middle_frame, text="Play Custom Tune", variable=self.play_sound_var,state=tk.DISABLED,
                                                 command=self.check_enable_button_state)  # Update on checkbox change
        self.play_sound_checkbox.pack(side=tk.LEFT, padx=10)

        self.show_popup_checkbox = tk.Checkbutton(middle_frame, text="Show Popup Notification",
                                                  variable=self.show_popup_var, command=self.check_enable_button_state)  # Update on checkbox change
        self.show_popup_checkbox.pack(side=tk.LEFT, padx=10)
        #endregion

        #region Bottom
        # Create a frame for the bottom section of the window
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=5)

        # Create a frame for the monitoring buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)


        self.enable_button = tk.Button(button_frame, text="Enable Monitoring", command=lambda: self.start_monitoring(self.custom_tune_path))
        self.enable_button.pack(side=tk.LEFT, padx=10)

        self.disable_button = tk.Button(button_frame, text="Disable Monitoring", state=tk.DISABLED,command=self.stop_monitoring)
        self.disable_button.pack(side=tk.LEFT, padx=10)

        self.browse_button = tk.Button(bottom_frame, text="Browse Tune", command=self.browse_custom_tune)
        self.browse_button.pack(side=tk.LEFT, padx=10)
        self.custom_tune_path = None

        self.custom_tune_name_label = tk.Label(bottom_frame, text="Selected Tune: None")
        self.custom_tune_name_label.pack(side=tk.RIGHT, padx=10)

        if self.custom_tune_path != None:
            self.play_sound_checkbox.config(state=tk.NORMAL)# Update on checkbox change

        #endregion

    def reset_gui(self):
        # Reset the app's state to its initial values
            #self.percentage_slider.set(50)  # Set the slider back to its initial value
            self.enable_button.config(state=tk.NORMAL)
            self.disable_button.config(state=tk.DISABLED)
            self.percentage_slider.configure(state=tk.NORMAL)
            self.play_sound_checkbox.config(state=tk.DISABLED)
            self.show_popup_checkbox.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)
            self.play_sound_var.set(0)      # Uncheck the "Play Custom Tune" checkbox
            self.show_popup_var.set(1)      # Check the "Show Popup Notification" checkbox
            self.custom_tune_path = None    # Clear the selected tune path
            self.custom_tune_name_label.config(text="Selected Tune: None")  # Clear the tune name label

    def stop_monitoring(self):
        self.desired_percentage = self.get_current_percentage()
        self.is_monitoring = False
        if self.is_monitoring:
            try:
                self.monitor_thread.join()
                self.charge_level_thread.join()
                self.reset_gui()
            except RuntimeError:
                messagebox.showerror("Runtime Error","Could not join thread")
            self.is_monitoring = False
        self.reset_gui()

    def monitor_battery(self, desired_percentage, tune_file):
        while self.is_monitoring:
            battery = psutil.sensors_battery()
            if battery:
                current_percentage = battery.percent 
                if psutil.sensors_battery().power_plugged:
                    if current_percentage == desired_percentage:
                        if self.play_sound_var.get() == 1 and self.custom_tune_path != "":
                            self.stop_monitoring()
                            sound = mixer.Sound(tune_file)
                            sound.play()
                        if self.show_popup_var.get() == 1:
                            messagebox.showinfo("Charging Complete", f"Battery reached {desired_percentage}%.")
                        self.reset_gui()
                        break
                else:
                    messagebox.showerror("Charging Error","Charging stopped!")
                    self.stop_monitoring()
                    self.reset_gui()

    def start_monitoring(self, tune_file):
        # Check if monitoring is already active
        if self.is_monitoring:
            messagebox.showinfo("Monitoring Active", "Monitoring is already active.")
            return

        current_percentage = self.get_current_percentage()
        desired_percentage = self.percentage_slider.get()
        is_plugged = psutil.sensors_battery().power_plugged

        if current_percentage < desired_percentage:
            if not is_plugged:
                messagebox.showinfo("Connect Charger", "Please connect the charger to start monitoring.")
                return

        if current_percentage > desired_percentage:
            messagebox.showinfo("Very Funny!", "You can only charge above your current charge level!")
        elif current_percentage == desired_percentage:
            messagebox.showinfo("Requirement already fulfilled","Your current battery percentage\nmatches the desired level of charge")
            return

        if is_plugged:
            if self.is_monitoring == False:
                self.monitor_thread = threading.Thread(target=self.monitor_battery, args=(desired_percentage, tune_file))
                self.monitor_thread.daemon = True
                self.monitor_thread.start()
                self.is_monitoring = True

            if self.charge_level_thread:
                pass
            else:
                #Create a thread to dyamically update the percentage
                self.charge_level_thread = threading.Thread(target=self.update_charge_level)
                self.charge_level_thread.daemon = True
                self.charge_level_thread.start()
            
            self.enable_button.config(state=tk.DISABLED)
            self.disable_button.config(state=tk.NORMAL)
            self.percentage_slider.configure(state=tk.DISABLED)
            self.play_sound_checkbox.config(state=tk.DISABLED)
            self.show_popup_checkbox.config(state=tk.DISABLED)
            self.browse_button.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Monitoring Interrupted", "Charging Stopped")
            self.stop_monitoring()

    def browse_custom_tune(self):
            # Open a file dialog for the user to select a custom tune file
            tune_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav"),("Audio Files","*.mp3")])
            if tune_file:
                self.custom_tune_path = tune_file
                mixer.init()
                try:
                    mixer.music.load(tune_file)
                except Exception:
                    messagebox.showerror("Unsupported File","Could not read file. Please select another sound")
                    return
                tune_filename = os.path.basename(tune_file)
                self.custom_tune_name_label.config(text=f"Selected Tune: {tune_filename}")
                self.play_sound_checkbox.config(state=tk.NORMAL)
                self.check_enable_button_state()  # Check the state of the Enable Monitoring button
                return tune_file

    def update_charge_level(self,):
      while True:
         current_percentage = self.get_current_percentage()
         self.charge_label.config(text=f"Charge Level: {current_percentage}%")
         time.sleep(30)  # Update every minute (adjust as needed)

    def check_enable_button_state(self):
        # Check the state of the Enable Monitoring button based on checkbox states
        if (self.play_sound_var.get() == 1 and self.custom_tune_path != "" or self.show_popup_var.get() == 1):
            self.enable_button.config(state=tk.NORMAL)
        else:
            self.enable_button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BatteryMonitorApp()
    app.run()
