import numpy as np
import serial
import time
from typing import Tuple

class ThermCalibration:
    def __init__(self):
        # Update calibration constants based on provided equations
        self.m = 0.0815   # slope: Temperature(°C) = 0.0815 × (analog value) + -18.8333
        self.b = -18.8333 # y-intercept
        
        # Initialize data storage
        self.analog_readings = []
        self.setpoint_celsius = 22.5  # Given setpoint
        
        # Control limits from statistical analysis
        self.analog_ucl = 519  # Upper Control Limit in analog
        self.analog_lcl = 495  # Lower Control Limit in analog
        self.celsius_ucl = 23.5  # Upper Control Limit in Celsius
        self.celsius_lcl = 21.5  # Lower Control Limit in Celsius
        self.std_dev = 4  # Standard deviation from analysis
    
    def add_reading(self, analog_value: float) -> None:
        """Add a new analog reading to the dataset"""
        self.analog_readings.append(analog_value)
    
    def calculate_statistics(self) -> Tuple[float, float]:
        """Calculate mean and standard deviation of readings"""
        if not self.analog_readings:
            return 0, 0
            
        readings = np.array(self.analog_readings)
        mean = np.mean(readings)
        std_dev = np.std(readings, ddof=1)  # ddof=1 for sample standard deviation
        return mean, std_dev
    
    def analog_to_celsius(self, analog_value: float) -> float:
        """Convert analog reading to Celsius using calibration equation"""
        return self.m * analog_value + self.b
    
    def celsius_to_analog(self, celsius: float) -> float:
        """Convert Celsius to analog value using inverted calibration equation"""
        return (celsius - self.b) / self.m
    
    def calculate_control_limits(self) -> dict:
        """Calculate UCL and LCL for both analog and Celsius values"""
        # Get standard deviation
        _, std_dev = self.calculate_statistics()
        std_dev = np.ceil(std_dev)  # Round up to nearest whole number
        
        # Calculate setpoint in analog value
        setpoint_analog = self.celsius_to_analog(self.setpoint_celsius)
        
        # Calculate control limits in analog values
        analog_ucl = setpoint_analog + (3 * std_dev)
        analog_lcl = setpoint_analog - (3 * std_dev)
        
        # Convert control limits to Celsius
        celsius_ucl = self.analog_to_celsius(analog_ucl)
        celsius_lcl = self.analog_to_celsius(analog_lcl)
        
        return {
            'setpoint_celsius': self.setpoint_celsius,
            'setpoint_analog': setpoint_analog,
            'standard_deviation': std_dev,
            'analog_ucl': analog_ucl,
            'analog_lcl': analog_lcl,
            'celsius_ucl': celsius_ucl,
            'celsius_lcl': celsius_lcl
        }

def get_temperature(analog_value: float) -> float:
    """Convert analog value to temperature in Celsius"""
    calibration = ThermCalibration()
    return calibration.analog_to_celsius(analog_value)

def parse_arduino_data(serial_data: str) -> tuple:
    """Parse comma-separated data from Arduino"""
    try:
        # Format: "AV:123,TC:23.5,TF:74.3,STATUS"
        parts = serial_data.strip().split(',')
        analog = float(parts[0].split(':')[1])
        temp_c = float(parts[1].split(':')[1])
        temp_f = float(parts[2].split(':')[1])
        status = parts[3]
        return analog, temp_c, temp_f, status
    except:
        return None, None, None, None

def connect_to_arduino(port='/dev/ttyACM0', baudrate=9600):
    """Establish connection with Arduino"""
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        return ser
    except Exception as e:
        print(f"Error connecting to Arduino: {e}")
        return None

# Example usage and testing
if __name__ == "__main__":
    calibration = ThermCalibration()
    
    # Connect to Arduino
    arduino = connect_to_arduino()
    if not arduino:
        print("Failed to connect to Arduino. Exiting...")
        exit()
    
    print("\nCollecting 20 readings at room temperature...")
    print("Please don't touch the sensor during this process.")
    print("\nReading data...\n")
    
    readings_count = 0
    while readings_count < 20:
        try:
            if arduino.in_waiting:
                serial_data = arduino.readline().decode().strip()
                analog, temp_c, temp_f, status = parse_arduino_data(serial_data)
                
                if analog is not None:
                    calibration.add_reading(analog)
                    print(f"Reading {readings_count + 1}/20: Analog={analog:.0f}, Temp={temp_c:.2f}°C (Status: {status})")
                    readings_count += 1
                    
        except Exception as e:
            print(f"Error reading data: {e}")
            break
            
    # Calculate and display results
    mean, std_dev = calibration.calculate_statistics()
    print(f"\nStatistical Analysis:")
    print(f"Mean Analog Value: {mean:.2f}")
    print(f"Standard Deviation: {np.ceil(std_dev):.0f}")
    
    # Calculate and display control limits
    limits = calibration.calculate_control_limits()
    print(f"\nControl Limits:")
    print(f"Setpoint: {limits['setpoint_celsius']:.1f}°C ({limits['setpoint_analog']:.1f} analog)")
    print(f"UCL: {limits['celsius_ucl']:.1f}°C ({limits['analog_ucl']:.1f} analog)")
    print(f"LCL: {limits['celsius_lcl']:.1f}°C ({limits['analog_lcl']:.1f} analog)")
    
    # Clean up
    arduino.close()