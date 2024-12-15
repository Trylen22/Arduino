import tkinter as tk
import serial
import threading
import time
import random
from therm_calibration import get_temperature

class ThermometerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Thermal Fluid Visualizer")
        
        # Configure main window
        self.root.configure(bg='black')
        
        # Frame for the visualization
        self.viz_frame = tk.Frame(root, bg='black')
        self.viz_frame.pack(pady=20)
        
        # Canvas for drawing
        self.canvas = tk.Canvas(self.viz_frame, width=300, height=500, bg='black')
        self.canvas.pack(side=tk.LEFT, padx=20)
        
        # Temperature display frame
        self.temp_frame = tk.Frame(self.viz_frame, bg='black')
        self.temp_frame.pack(side=tk.LEFT, padx=20)
        
        # Labels for both temperature scales
        self.celsius_label = tk.Label(self.temp_frame, 
                                    text="-- °C", 
                                    font=('Arial', 24, 'bold'),
                                    bg='black', fg='white')
        self.celsius_label.pack(pady=10)
        
        self.fahrenheit_label = tk.Label(self.temp_frame, 
                                       text="-- °F",
                                       font=('Arial', 24, 'bold'),
                                       bg='black', fg='white')
        self.fahrenheit_label.pack(pady=10)
        
        # Status indicators
        self.flow_label = tk.Label(self.temp_frame, 
                                 text="Flow: Stable",
                                 font=('Arial', 12),
                                 bg='black', fg='white')
        self.flow_label.pack(pady=5)
        
        self.status_label = tk.Label(self.temp_frame, 
                                   text="Not Connected",
                                   font=('Arial', 12),
                                   bg='black', fg='red')
        self.status_label.pack(pady=5)
        
        # Reconnect button
        self.reconnect_btn = tk.Button(self.temp_frame, 
                                     text="Reconnect",
                                     command=self.connect_to_arduino)
        self.reconnect_btn.pack(pady=5)
        
        # Draw the container and decorations
        self.draw_container()
        
        # Initialize variables
        self.serial = None
        self.last_temp = 20
        self.current_color = '#0000FF'  # Start with blue
        self.color_transition_speed = 0.1  # Adjust for transition speed
        self.particle_positions = []
        
        # Connect to Arduino
        self.connect_to_arduino()
        
        # Start reading thread
        self.running = True
        self.thread = threading.Thread(target=self.read_serial)
        self.thread.daemon = True
        self.thread.start()
        
        # Start animation
        self.animate_particles()

    def draw_container(self):
        # Draw container outline with gradient border
        self.container = self.canvas.create_rectangle(
            75, 50, 225, 450,
            outline='white', width=3
        )
        
        # Draw fill level marks with labels
        for y in range(100, 450, 50):
            # Level marks
            self.canvas.create_line(
                75, y, 85, y,
                fill='white', width=2
            )
            # Level numbers
            self.canvas.create_text(
                60, y,
                text=f"{450-y}",
                fill='white',
                font=('Arial', 8)
            )
            
        # Add decorative elements
        self.canvas.create_text(
            150, 30,
            text="Temperature",
            fill='white',
            font=('Arial', 12, 'bold')
        )

    def get_temperature_color(self, temp_c):
        # Calculate target color based on temperature
        if temp_c < 0:
            target_color = '#0000FF'  # Deep blue for very cold
        elif temp_c < 20:
            ratio = temp_c / 20
            blue = int(255 * (1 - ratio))
            target_color = f'#00{blue:02x}FF'
        elif temp_c < 30:
            ratio = (temp_c - 20) / 20
            red = int(255 * ratio)
            target_color = f'#{red:02x}00FF'
        else:
            target_color = '#FF0000'  # Red for very hot

        # Gradually transition current color to target color
        current_rgb = [int(self.current_color[i:i+2], 16) for i in (1, 3, 5)]
        target_rgb = [int(target_color[i:i+2], 16) for i in (1, 3, 5)]
        
        # Interpolate between current and target colors
        new_rgb = [
            int(current_rgb[i] + (target_rgb[i] - current_rgb[i]) * self.color_transition_speed)
            for i in range(3)
        ]
        
        # Convert back to hex color
        self.current_color = '#{:02x}{:02x}{:02x}'.format(
            max(0, min(255, new_rgb[0])),
            max(0, min(255, new_rgb[1])),
            max(0, min(255, new_rgb[2]))
        )
        
        return self.current_color

    def animate_particles(self):
        self.canvas.delete("particle")
        
        # More particles and faster movement at higher temperatures
        num_particles = int(10 + max(0, (self.last_temp - 20) / 2))
        
        for _ in range(num_particles):
            x = 85 + (225-85) * random.random()
            y = 60 + (450-60) * random.random()
            size = 2 + (self.last_temp / 40)  # Particles grow with temperature
            
            # Create particle with slight glow effect
            self.canvas.create_oval(
                x-size-1, y-size-1, x+size+1, y+size+1,
                fill='white', outline='gray90',
                tags="particle"
            )
        
        self.root.after(100, self.animate_particles)

    def connect_to_arduino(self):
        if self.serial:
            self.serial.close()
            
        try:
            print("Attempting to connect to Arduino...")
            self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            time.sleep(2)  # Give Arduino time to reset
            print("Successfully connected to Arduino")
            self.status_label.config(text="Connected", fg="green")
            return True
        except Exception as e:
            print(f"Failed to connect: {str(e)}")
            self.status_label.config(text=f"Connection Failed", fg="red")
            return False

    def read_serial(self):
        while self.running:
            if self.serial:
                try:
                    if self.serial.in_waiting:
                        raw_data = self.serial.readline()
                        print(f"Raw data received: {raw_data}")
                        analog_value = float(raw_data.decode().strip())
                        self.root.after(0, self.update_display, analog_value)
                except Exception as e:
                    print(f"Error reading serial data: {str(e)}")
                    self.status_label.config(text="Connection Lost", fg="red")
                    time.sleep(1)
                    self.connect_to_arduino()
            time.sleep(0.1)

    def update_display(self, analog_value):
        try:
            # Get temperature in Celsius
            temp_c = get_temperature(analog_value)
            # Convert to Fahrenheit
            temp_f = (temp_c * 9/5) + 32
            
            # Update labels
            self.celsius_label.config(text=f"{temp_c:.1f} °C")
            self.fahrenheit_label.config(text=f"{temp_f:.1f} °F")
            
            # Update container color with smooth transition
            color = self.get_temperature_color(temp_c)
            self.canvas.delete("fill")
            self.canvas.create_rectangle(
                77, 52, 223, 448,
                fill=color, tags="fill"
            )
            
            # Update flow status with enhanced visuals
            if abs(temp_c - self.last_temp) > 2:
                self.flow_label.config(text="Flow: Turbulent", fg='yellow')
            else:
                self.flow_label.config(text="Flow: Laminar", fg='green')
            
            self.last_temp = temp_c
            
        except ValueError as e:
            print(f"Error updating display: {str(e)}")
            self.celsius_label.config(text="Error")
            self.fahrenheit_label.config(text="Error")

    def on_closing(self):
        self.running = False
        if self.serial:
            self.serial.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ThermometerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()