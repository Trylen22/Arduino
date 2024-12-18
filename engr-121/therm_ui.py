import tkinter as tk
import serial
import threading
import time
import random
import datetime
import logging
from typing import Dict, List
from therm_calibration import get_temperature
from therm_agent import ThermalAgent
from therm_model import ThermalModel
import queue

class ThermometerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Thermal AI Monitor")
        
        # Configure main window
        self.root.configure(bg='black')
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(pady=20, expand=True, fill=tk.BOTH)
        
        # AI Analysis Display
        self.ai_display = tk.Text(
            self.main_frame,
            height=25,
            width=60,
            bg='black',
            fg='cyan',
            font=('Courier', 11),
            wrap=tk.WORD
        )
        self.ai_display.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.BOTH)
        
        # Add scrollbar for AI display
        self.ai_scrollbar = tk.Scrollbar(self.main_frame)
        self.ai_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure scrollbar
        self.ai_display.config(yscrollcommand=self.ai_scrollbar.set)
        self.ai_scrollbar.config(command=self.ai_display.yview)
        
        # Temperature display frame
        self.temp_frame = tk.Frame(self.main_frame, bg='black')
        self.temp_frame.pack(side=tk.RIGHT, padx=20)
        
        # Initialize variables
        self.serial = None
        self.running = True
        self.readings_count = 0
        self.diagnostic_interval = 50
        self.last_status = 'normal'
        self.significant_change_threshold = 2.0
        self.last_reported_temp = None
        
        # Initialize components
        self.setup_temperature_display()
        self.setup_status_display()
        self.setup_statistics()
        self.setup_monitor()
        
        # Initialize agents
        self.agent = ThermalAgent()
        self.model = ThermalModel()
        
        # Connect to Arduino
        self.connect_to_arduino()
        
        # Start reading thread
        self.thread = threading.Thread(target=self.read_serial)
        self.thread.daemon = True
        self.thread.start()
        
        # Add queue for AI messages
        self.ai_queue = queue.Queue()
        
        # Start AI message consumer
        self.root.after(100, self.process_ai_queue)

    def setup_temperature_display(self):
        """Setup temperature display labels"""
        self.celsius_label = tk.Label(
            self.temp_frame,
            text="-- °C",
            font=('Arial', 24, 'bold'),
            bg='black', fg='white'
        )
        self.celsius_label.pack(pady=10)
        
        self.fahrenheit_label = tk.Label(
            self.temp_frame,
            text="-- °F",
            font=('Arial', 24, 'bold'),
            bg='black', fg='white'
        )
        self.fahrenheit_label.pack(pady=10)
        
        self.analog_label = tk.Label(
            self.temp_frame,
            text="AR: --",
            font=('Arial', 16),
            bg='black', fg='cyan'
        )
        self.analog_label.pack(pady=5)

    def setup_status_display(self):
        """Setup status indicators"""
        self.status_label = tk.Label(
            self.temp_frame,
            text="Not Connected",
            font=('Arial', 12),
            bg='black', fg='red'
        )
        self.status_label.pack(pady=5)
        
        self.ai_status = tk.Label(
            self.temp_frame,
            text="AI: Ready",
            font=('Arial', 10),
            bg='black', fg='cyan'
        )
        self.ai_status.pack(pady=2)
        
        self.reconnect_btn = tk.Button(
            self.temp_frame,
            text="Reconnect",
            command=self.connect_to_arduino
        )
        self.reconnect_btn.pack(pady=5)

    def setup_statistics(self):
        """Setup statistics display"""
        self.stats_frame = tk.Frame(self.temp_frame, bg='black')
        self.stats_frame.pack(pady=10)
        
        self.stats_label = tk.Label(
            self.stats_frame,
            text="Statistics",
            font=('Arial', 12, 'bold'),
            bg='black', fg='white'
        )
        self.stats_label.pack()
        
        self.min_max_label = tk.Label(
            self.stats_frame,
            text="Min: -- °C  Max: -- °C",
            font=('Arial', 10),
            bg='black', fg='white'
        )
        self.min_max_label.pack()
        
        self.avg_label = tk.Label(
            self.stats_frame,
            text="Avg: -- °C",
            font=('Arial', 10),
            bg='black', fg='white'
        )
        self.avg_label.pack()

    def setup_monitor(self):
        """Setup serial monitor"""
        # Add Serial Monitor Frame
        self.monitor_frame = tk.Frame(self.root, bg='black')
        self.monitor_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Serial Monitor Label
        self.monitor_label = tk.Label(self.monitor_frame,
                                    text="Serial Monitor",
                                    font=('Arial', 12, 'bold'),
                                    bg='black', fg='white')
        self.monitor_label.pack()
        
        # Serial Monitor Text Widget
        self.monitor_text = tk.Text(self.monitor_frame,
                                  height=10,
                                  width=50,
                                  bg='black',
                                  fg='green',
                                  font=('Courier', 10))
        self.monitor_text.pack()
        
        # Autoscroll Checkbox
        self.autoscroll_var = tk.BooleanVar(value=True)
        self.autoscroll_check = tk.Checkbutton(self.monitor_frame,
                                              text="Autoscroll",
                                              variable=self.autoscroll_var,
                                              bg='black',
                                              fg='white',
                                              selectcolor='black')
        self.autoscroll_check.pack()
        
        # Clear Button
        self.clear_button = tk.Button(self.monitor_frame,
                                    text="Clear Monitor",
                                    command=self.clear_monitor)
        self.clear_button.pack(pady=5)
        
        # Add after other initializations
        self.readings_count = 0
        self.diagnostic_interval = 50  # Generate diagnostic every 50 readings
        self.readings_for_report = 20  # Number of readings before generating report
        self.min_report_interval = 30  # Minimum seconds between reports
        self.last_report_time = time.time()
        
        # Add report type tracking
        self.last_status = 'normal'
        self.significant_change_threshold = 2.0  # °C
        self.last_reported_temp = None
        
        # Add AI status indicator
        self.ai_status = tk.Label(self.temp_frame,
                                text="AI: Ready",
                                font=('Arial', 10),
                                bg='black', fg='cyan')
        self.ai_status.pack(pady=2)

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
                        try:
                            decoded_data = raw_data.decode().strip()
                            # Update monitor with raw data
                            self.root.after(0, self.update_monitor, decoded_data)
                            
                            if decoded_data.startswith('Raw:'):  # Only process data lines
                                # Parse the comma-separated data
                                data = decoded_data.split(',')
                                analog_value = float(data[0].split(':')[1])  # Get value after "Raw:"
                                temp_c = float(data[1].split(':')[1])        # Get value after "TC:"
                                temp_f = float(data[2].split(':')[1])        # Get value after "TF:"
                                led_status = data[3].split(':')[1]           # Get value after "LED:"
                                
                                # Update display with parsed values
                                self.root.after(0, lambda av=analog_value, tc=temp_c, 
                                              tf=temp_f, ls=led_status: self.update_display(av, tc, tf, ls))
                                
                                # Increment readings count and check for report
                                self.readings_count += 1
                                if self.readings_count >= self.readings_for_report:
                                    self.generate_full_report()
                                    self.readings_count = 0  # Reset counter
                                
                        except Exception as e:
                            error_msg = f"Error processing data: {str(e)}"
                            self.root.after(0, self.update_monitor, error_msg)
                except Exception as e:
                    error_msg = f"Serial error: {str(e)}"
                    self.root.after(0, self.update_monitor, error_msg)
                    self.status_label.config(text="Connection Lost", fg="red")
                    time.sleep(1)
                    self.connect_to_arduino()
            time.sleep(0.1)

    def generate_full_report(self):
        """Generate a comprehensive report"""
        try:
            # Get last 20 readings
            recent_readings = self.agent.temperature_history[-20:]
            if not recent_readings:
                return
            
            # Generate analysis
            analysis = self.model.analyze_batch(recent_readings)
            
            # Display analysis
            self.update_monitor("\n" + analysis)
            self.update_ai_display(analysis, 'info')
            
        except Exception as e:
            error_msg = f"Error generating report: {str(e)}"
            logging.error(error_msg)
            self.update_monitor(error_msg)

    def get_ai_analysis(self, stats, trend):
        """Get AI analysis in background"""
        try:
            context = f"""
            Current Stats:
            - Temperature: {stats['current']:.1f}°C
            - Range: {stats['min']:.1f}°C to {stats['max']:.1f}°C
            - Average: {stats['avg']:.1f}°C
            - Trend: {trend}
            """
            
            for response in self.model.respond(context):
                if response:
                    self.update_monitor("\nAI Analysis:\n" + response)
        except Exception as e:
            logging.error(f"AI analysis failed: {e}")

    def should_generate_report(self, temp_c: float, status: str) -> bool:
        """Determine if we should generate a report"""
        current_time = time.time()
        
        # Always report on status changes
        if status != self.last_status:
            self.last_report_time = current_time
            self.last_status = status
            return True
            
        # Report on significant temperature changes
        if self.readings_count > 0 and abs(temp_c - self.last_reported_temp) >= self.significant_change_threshold:
            self.last_report_time = current_time
            return True
            
        # Regular interval reports
        if self.readings_count >= self.readings_for_report and \
           (current_time - self.last_report_time) >= self.min_report_interval:
            self.last_report_time = current_time
            self.readings_count = 0
            return True
            
        return False

    def update_display(self, analog_value, temp_c, temp_f, led_status):
        """Optimized display updates"""
        try:
            # Update basic UI immediately
            self._safe_update_ui({
                'reading': {
                    'temp_c': temp_c,
                    'temp_f': temp_f,
                    'analog': analog_value
                },
                'ui_updates': {
                    'status_text': led_status,
                    'status_color': 'green'
                }
            })
            
            # Start AI analysis only if needed
            if self.should_update_ai():
                threading.Thread(
                    target=self._run_ai_analysis,
                    args=(analog_value, temp_c, temp_f, led_status),
                    daemon=True
                ).start()
            
        except Exception as e:
            logging.error(f"Display update error: {e}")

    def should_update_ai(self) -> bool:
        """Determine if AI update is needed"""
        current_time = time.time()
        if not hasattr(self, 'last_ai_update'):
            self.last_ai_update = 0
        
        # Update AI display every 5 seconds at most
        if current_time - self.last_ai_update >= 5:
            self.last_ai_update = current_time
            return True
        return False

    def _run_ai_analysis(self, analog_value, temp_c, temp_f, led_status):
        """Run AI analysis in background thread"""
        try:
            # Get agent's analysis
            decision = self.agent.analyze_and_decide(
                analog_value, temp_c, temp_f, led_status
            )
            
            # Queue updates
            self.ai_queue.put((
                f"Temperature: {temp_c:.1f}°C ({temp_f:.1f}°F)",
                'info'
            ))
            
            self.ai_queue.put((
                f"Status: {decision['analysis']['alert_level']}",
                'alert' if 'warning' in decision['analysis']['alert_level'] else 'info'
            ))
            
            if 'ai_insights' in decision:
                self.ai_queue.put((
                    f"\nAI Analysis:\n{decision['ai_insights']}",
                    'success'
                ))
            
            if decision['recommendations']:
                self.ai_queue.put((
                    "\nRecommendations:\n" + "\n".join(
                        f"• {rec}" for rec in decision['recommendations']
                    ),
                    'info'
                ))
            
            # Update stats in main thread
            self.root.after(0, lambda: self._safe_update_ui(decision))
            
        except Exception as e:
            error_msg = f"AI analysis failed: {str(e)}"
            logging.error(error_msg)
            self.ai_queue.put((error_msg, 'error'))

    def _safe_update_ui(self, decision: Dict):
        """Update UI based on agent's decisions"""
        try:
            reading = decision['reading']
            ui_updates = decision['ui_updates']
            
            # Update temperature displays
            self.celsius_label.config(text=f"{reading['temp_c']:.1f} °C")
            self.fahrenheit_label.config(text=f"{reading['temp_f']:.1f} °F")
            self.analog_label.config(text=f"AR: {reading['analog']:.0f}")
            
            # Update status
            self.status_label.config(
                text=ui_updates['status_text'],
                fg=ui_updates['status_color']
            )
            
            # Update statistics if available
            stats = self.agent.get_statistics()
            if stats:
                self.min_max_label.config(
                    text=f"Min: {stats['min']:.1f}°C  Max: {stats['max']:.1f}°C"
                )
                self.avg_label.config(
                    text=f"Avg: {stats['avg']:.1f}°C"
                )
            
        except Exception as e:
            logging.error(f"UI update failed: {e}")

    def on_closing(self):
        """Improved cleanup"""
        print("Shutting down...")
        self.running = False
        
        # Close serial connection
        if self.serial:
            try:
                self.serial.close()
            except:
                pass
        
        # Stop any running threads
        if hasattr(self, 'thread') and self.thread.is_alive():
            try:
                self.thread.join(timeout=1.0)
            except:
                pass
        
        # Destroy the window
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
        
        print("Shutdown complete")

    def update_monitor(self, data: str):
        """Update the serial monitor with new data"""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            formatted_data = f"[{timestamp}] {data}\n"
            
            # Use after to ensure thread safety
            self.root.after(0, lambda: self._update_monitor_text(formatted_data))
            
        except Exception as e:
            print(f"Error updating monitor: {str(e)}")

    def _update_monitor_text(self, formatted_data: str):
        """Actually update the monitor text (called from main thread)"""
        self.monitor_text.insert(tk.END, formatted_data)
        
        # Limit the number of lines (keep last 100 lines)
        num_lines = int(self.monitor_text.index('end-1c').split('.')[0])
        if num_lines > 100:
            self.monitor_text.delete('1.0', '2.0')
        
        # Autoscroll if enabled
        if self.autoscroll_var.get():
            self.monitor_text.see(tk.END)

    def clear_monitor(self):
        """Clear the serial monitor"""
        self.monitor_text.delete('1.0', tk.END)

    def generate_basic_report(self, stats: Dict, trend: str) -> str:
        """Generate a basic report without AI analysis"""
        return f"""
{'='*50}
THERMAL SYSTEM STATUS REPORT
{'='*50}
Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Temperature Statistics:
---------------------
Current: {stats['current']:.1f}°C
Minimum: {stats['min']:.1f}°C
Maximum: {stats['max']:.1f}°C
Average: {stats['avg']:.1f}°C

System Status:
------------
Temperature Trend: {trend}
Alert Level: {self.status_label.cget('text')}

Control Limits:
-------------
UCL: {self.model.system_limits['temp_ucl']}°C ({self.model.system_limits['analog_ucl']} analog)
LCL: {self.model.system_limits['temp_lcl']}°C ({self.model.system_limits['analog_lcl']} analog)

{'='*50}
"""

    def update_ai_display(self, text: str, message_type: str = 'info'):
        """Update AI analysis display with colored text"""
        self.root.after(0, lambda: self._safe_update_ai_display(text, message_type))

    def _safe_update_ai_display(self, text: str, message_type: str):
        """Thread-safe update of AI display"""
        try:
            # Color mapping for different message types
            colors = {
                'info': 'cyan',
                'alert': 'yellow',
                'error': 'red',
                'success': 'green',
                'processing': '#888888'  # Gray for processing messages
            }
            color = colors.get(message_type, 'white')
            
            # Add timestamp
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            formatted_text = f"[{timestamp}] {text}\n"
            
            # Insert text with color
            self.ai_display.tag_config(message_type, foreground=color)
            self.ai_display.insert(tk.END, formatted_text, message_type)
            
            # Limit buffer size (keep last 1000 lines)
            lines = int(self.ai_display.index('end-1c').split('.')[0])
            if lines > 1000:
                self.ai_display.delete('1.0', '2.0')
            
            # Auto-scroll if near bottom
            self.ai_display.see(tk.END)
            
        except Exception as e:
            logging.error(f"Error updating AI display: {e}")

    def process_ai_queue(self):
        """Faster queue processing"""
        try:
            # Process up to 5 messages at once
            for _ in range(5):
                try:
                    message, msg_type = self.ai_queue.get_nowait()
                    self._safe_update_ai_display(message, msg_type)
                except queue.Empty:
                    break
        finally:
            if self.running:
                # Check queue more frequently
                self.root.after(50, self.process_ai_queue)

def main():
    root = tk.Tk()
    app = ThermometerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()