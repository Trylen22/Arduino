import tkinter as tk
import serial
import threading
import time
import datetime
import logging
from typing import Dict, List
import subprocess

class ThermalAgent:
    def __init__(self):
        self.batch_size = 20
        self.current_batch = []
        self.last_analysis = None
        self.analyzing = False
    
    def add_reading(self, temp_reading: Dict) -> None:
        """Add a new reading to current batch"""
        self.current_batch.append(temp_reading)
        
        # When we have enough readings, trigger analysis
        if len(self.current_batch) >= self.batch_size and not self.analyzing:
            self.analyze_batch()
    
    def analyze_batch(self) -> None:
        """Analyze a complete batch in background thread"""
        self.analyzing = True
        threading.Thread(target=self._run_analysis, daemon=True).start()
    
    def _run_analysis(self) -> None:
        """Run AI analysis on current batch"""
        try:
            temps = [r['temp'] for r in self.current_batch]
            times = [r['time'] for r in self.current_batch]
            
            # Calculate metrics
            avg_temp = sum(temps)/len(temps)
            min_temp = min(temps)
            max_temp = max(temps)
            total_time = (times[-1] - times[0]).total_seconds() / 60
            rate = (temps[-1] - temps[0]) / total_time if total_time > 0 else 0
            
            # Determine component states more precisely
            is_heating = rate > 0.1
            is_cooling = rate < -0.1
            in_range = 20 <= temps[-1] <= 25
            
            prompt = f"""You are diagnosing a temperature-controlled canister system.
Current System State:
• Temperature: {temps[-1]:.1f}°C (Target: 20-25°C)
• Rate of Change: {rate:+.2f}°C/min
• Heater is {'ACTIVE' if is_heating else 'INACTIVE'}
• Fan is {'ACTIVE' if is_cooling else 'INACTIVE'}
• Control Status: {'IN RANGE' if in_range else 'OUT OF RANGE'}

History:
• Last {total_time:.1f} minutes
• Range: {min_temp:.1f}°C to {max_temp:.1f}°C
• Average: {avg_temp:.1f}°C

Provide a brief analysis focusing on:
1. Is the system responding as expected to current conditions?
2. What actions should be taken (if any)?
3. Are there any concerns about system performance?

Note: Only suggest component issues if behavior clearly indicates a malfunction."""

            # Run analysis with shorter timeout
            process = subprocess.Popen(
                ["ollama", "run", "mistral"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            process.stdin.write(prompt)
            process.stdin.close()
            
            # Collect response with shorter timeout
            response = []
            start = time.time()
            while time.time() - start < 5:  # Reduced timeout
                line = process.stdout.readline().strip()
                if not line:
                    break
                response.append(line)
            
            process.terminate()
            
            # Add engineering context to the display
            if response:
                system_state = (
                    'heating' if rate > 0.1 
                    else 'cooling' if rate < -0.1 
                    else 'stable'
                )
                
                self.last_analysis = {
                    'time': datetime.datetime.now(),
                    'text': "\n".join(response),
                    'data': {
                        'current_temp': temps[-1],
                        'avg_temp': avg_temp,
                        'min_temp': min_temp,
                        'max_temp': max_temp,
                        'rate': rate,
                        'duration': total_time,
                        'readings': len(temps),
                        'stability': round(max_temp - min_temp, 2),
                        'system_state': system_state,
                        'components': {
                            'heater': 'active' if rate > 0.1 else 'inactive',
                            'fan': 'active' if rate < -0.1 else 'inactive',
                            'in_range': 20 <= temps[-1] <= 25
                        }
                    }
                }
        
        except Exception as e:
            print(f"Batch analysis error: {e}")
        
        finally:
            # Clear batch and reset flag
            self.current_batch = []
            self.analyzing = False
    
    def get_latest_analysis(self) -> Dict:
        """Get the most recent analysis"""
        return self.last_analysis

class ThermalMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Thermal Monitor")
        self.root.configure(bg='black')
        
        # Main display
        self.setup_display()
        
        # Data storage
        self.readings = []
        self.running = True
        
        # Control limits
        self.limits = {
            'warning_high': 25.0,
            'warning_low': 20.0,
            'critical_high': 30.0,
            'critical_low': 15.0
        }
        
        # Connect to Arduino
        try:
            self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            time.sleep(2)
            self.status_label.config(text="Connected", fg="green")
        except:
            self.serial = None
            self.status_label.config(text="No Connection", fg="red")
        
        # Start reading thread
        self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
        self.read_thread.start()
        
        # Add AI agent
        self.agent = ThermalAgent()
        
        # Add AI display
        self.setup_ai_display()

    def setup_display(self):
        # Temperature display
        self.temp_frame = tk.Frame(self.root, bg='black')
        self.temp_frame.pack(pady=20)
        
        self.temp_label = tk.Label(
            self.temp_frame,
            text="--.- °C",
            font=('Arial', 48, 'bold'),
            bg='black', fg='cyan'
        )
        self.temp_label.pack()
        
        # Status display
        self.status_label = tk.Label(
            self.temp_frame,
            text="Starting...",
            font=('Arial', 14),
            bg='black', fg='yellow'
        )
        self.status_label.pack(pady=10)
        
        # Analysis display
        self.analysis = tk.Text(
            self.root,
            height=20,
            width=60,
            bg='black',
            fg='white',
            font=('Courier', 12)
        )
        self.analysis.pack(pady=20, padx=20)

    def setup_ai_display(self):
        # AI Analysis display
        self.ai_frame = tk.Frame(self.root, bg='black')
        self.ai_frame.pack(pady=10, fill=tk.X)
        
        self.ai_label = tk.Label(
            self.ai_frame,
            text="System Analysis",
            font=('Arial', 16, 'bold'),
            bg='black', fg='cyan'
        )
        self.ai_label.pack()
        
        # Create a frame for the text box and scrollbar
        text_frame = tk.Frame(self.ai_frame, bg='black')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Larger text box
        self.ai_text = tk.Text(
            text_frame,
            height=20,
            width=70,
            bg='black',
            fg='green',
            font=('Courier', 12),
            wrap=tk.WORD
        )
        self.ai_text.pack(side=tk.LEFT, pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Connect scrollbar to text box
        self.ai_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.ai_text.yview)

    def analyze_readings(self, readings: List[Dict]) -> str:
        if len(readings) < 2:
            return "Collecting data..."
            
        temps = [r['temp'] for r in readings]
        current = temps[-1]
        avg = sum(temps) / len(temps)
        rate = (temps[-1] - temps[-2]) / (readings[-1]['time'] - readings[-2]['time']).total_seconds() * 60
        
        analysis = f"""
Temperature Analysis ({len(readings)} readings)
Time: {datetime.datetime.now().strftime('%H:%M:%S')}

Current: {current:.1f}°C
Average: {avg:.1f}°C
Rate: {rate:+.2f}°C/min

Status: """
        
        if current > self.limits['critical_high']:
            analysis += "CRITICAL HIGH TEMPERATURE"
        elif current < self.limits['critical_low']:
            analysis += "CRITICAL LOW TEMPERATURE"
        elif current > self.limits['warning_high']:
            analysis += "Warning: Temperature High"
        elif current < self.limits['warning_low']:
            analysis += "Warning: Temperature Low"
        else:
            analysis += "Normal Operation"
            
        if abs(rate) > 2:
            analysis += "\nWARNING: Rapid temperature change"
            
        return analysis

    def read_serial(self):
        while self.running:
            if self.serial and self.serial.in_waiting:
                try:
                    data = self.serial.readline().decode().strip()
                    if data.startswith('Raw:'):
                        parts = data.split(',')
                        temp_c = float(parts[1].split(':')[1])
                        
                        # Store reading
                        self.readings.append({
                            'time': datetime.datetime.now(),
                            'temp': temp_c
                        })
                        
                        # Keep last 20 readings
                        if len(self.readings) > 20:
                            self.readings.pop(0)
                        
                        # Update display
                        self.root.after(0, self.update_display, temp_c)
                        
                except Exception as e:
                    print(f"Error reading serial: {e}")
            time.sleep(0.1)

    def update_display(self, temp_c: float):
        try:
            # Update temperature
            self.temp_label.config(text=f"{temp_c:.1f} °C")
            
            # Update basic analysis
            analysis = self.analyze_readings(self.readings)
            self.analysis.delete('1.0', tk.END)
            self.analysis.insert('1.0', analysis)
            
            # Update color
            if temp_c > self.limits['critical_high'] or temp_c < self.limits['critical_low']:
                self.temp_label.config(fg='red')
            elif temp_c > self.limits['warning_high'] or temp_c < self.limits['warning_low']:
                self.temp_label.config(fg='yellow')
            else:
                self.temp_label.config(fg='cyan')
            
            # Add reading to agent
            self.agent.add_reading({
                'time': datetime.datetime.now(),
                'temp': temp_c
            })
            
            # Check for new analysis
            analysis = self.agent.get_latest_analysis()
            if analysis and (not hasattr(self, 'last_shown_time') or 
                           analysis['time'] != self.last_shown_time):
                self.last_shown_time = analysis['time']
                self.ai_text.delete('1.0', tk.END)
                
                # Format engineering-focused display
                components = analysis['data']['components']
                self.ai_text.insert('1.0', f"""
{'='*70}
THERMAL SYSTEM ANALYSIS
Time: {analysis['time'].strftime('%H:%M:%S')}
{'='*70}

CURRENT STATE: {analysis['data']['system_state'].upper()}
Temperature: {analysis['data']['current_temp']:.1f}°C
Rate of Change: {'+' if analysis['data']['rate'] > 0 else ''}{analysis['data']['rate']:.2f}°C/min
Operating Range: {analysis['data']['min_temp']:.1f}°C to {analysis['data']['max_temp']:.1f}°C

COMPONENT STATUS:
• Heater: {components['heater'].upper()}
• Fan: {components['fan'].upper()}
• Temperature Control: {'IN RANGE' if components['in_range'] else 'OUT OF RANGE'}

ENGINEER'S ANALYSIS:
{analysis['text']}

{'='*70}
""")
                
        except Exception as e:
            print(f"Display update error: {e}")

    def on_closing(self):
        self.running = False
        if self.serial:
            self.serial.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ThermalMonitor(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 