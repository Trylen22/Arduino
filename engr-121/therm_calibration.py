import matplotlib.pyplot as plt

# Your calibration data
analog_values = [495, 353, 705]   #average over 12 readings per each catagory.
temperatures_f = [70.7, 47.5, 101.5] #readings from thermometer, I accidentally took them in Fahrenheit.

# Convert F to C
def f_to_c(f):
    return (f - 32) * 5/9

# Convert all temperatures to Celsius
temperatures_c = [f_to_c(t) for t in temperatures_f]

# Calculate slope (m) and y-intercept (b) for y = mx + b
x1, x2 = analog_values[0], analog_values[-1]
y1, y2 = temperatures_c[0], temperatures_c[-1]
slope = (y2 - y1) / (x2 - x1)
intercept = y1 - (slope * x1)

print(f"Linear Calibration Equation:")
print(f"Temperature(°C) = {slope:.4f} × (analog value) + {intercept:.4f}")

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(analog_values, temperatures_c, color='red', label='Data Points')
plt.plot(analog_values, [slope * x + intercept for x in analog_values], 
         color='blue', label='Calibration Line')

plt.xlabel('Analog Value')
plt.ylabel('Temperature (°C)')
plt.title('Thermistor Calibration')
plt.legend()
plt.grid(True)
plt.show()

#calibration function
def get_temperature(analog):
    return (slope * analog) + intercept