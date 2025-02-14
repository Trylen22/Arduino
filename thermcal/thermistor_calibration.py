import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Your collected data points - all individual readings
cold_readings = [308, 308, 308, 308, 308, 308, 308, 308, 307, 307, 306, 302, 300, 298, 296, 295, 292, 291, 290, 289, 288, 288, 288, 288, 287, 287, 288, 287, 287]
room_readings = [478, 477, 478, 478, 477, 477, 477, 476, 476, 476, 476, 476, 476, 476, 475, 475, 476, 476, 476, 476, 477, 477, 477, 477, 476, 476, 476, 474, 472, 472, 473, 472, 471, 472, 472, 473, 473, 474, 474]
hot_readings = [712, 717, 714, 713, 713, 714, 715, 714, 714, 715, 715, 714, 714, 714, 713, 713, 713, 713, 712, 712, 712, 713, 713, 712, 712, 713, 713, 712, 712, 713, 713, 712]

# Create arrays of temperatures (repeated for each reading)
cold_temps = [8.5] * len(cold_readings)    # 8.5°C
room_temps = [22.5] * len(room_readings)   # 22.5°C
hot_temps = [38.8] * len(hot_readings)     # 38.8°C

# Combine all data points
temp_c = np.array(cold_temps + room_temps + hot_temps)
analog_values = np.array(cold_readings + room_readings + hot_readings)

# Define the fitting function (exponential relationship for NTC thermistor)
def thermistor_curve(x, a, b, c):
    return a * np.exp(b * x) + c

# Initial parameter guesses
p0 = [400, 0.05, 200]

# Fit the curve with modified parameters
popt, _ = curve_fit(
    thermistor_curve, 
    temp_c, 
    analog_values,
    p0=p0,
    maxfev=10000,
    bounds=(
        [-np.inf, -1, 0],
        [np.inf, 1, np.inf]
    )
)
a, b, c = popt

# Generate points for smooth curve
temp_fit = np.linspace(min(temp_c), max(temp_c), 100)
analog_fit = thermistor_curve(temp_fit, a, b, c)

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(cold_temps, cold_readings, color='blue', label='Cold Readings (8.5°C)')
plt.scatter(room_temps, room_readings, color='green', label='Room Readings (22.5°C)')
plt.scatter(hot_temps, hot_readings, color='red', label='Hot Readings (38.8°C)')
plt.plot(temp_fit, analog_fit, 'k-', label='Fitted Curve')

plt.xlabel('Temperature (°C)')
plt.ylabel('Analog Value')
plt.title('Thermistor Calibration Curve - All Data Points')
plt.grid(True)
plt.legend()

# Print statistics for each temperature point
print("\nCold Temperature Statistics (8.5°C):")
print(f"Min: {min(cold_readings)}, Max: {max(cold_readings)}")
print(f"Range: {max(cold_readings) - min(cold_readings)}")
print(f"Mean: {np.mean(cold_readings):.2f}")

print("\nRoom Temperature Statistics (22.5°C):")
print(f"Min: {min(room_readings)}, Max: {max(room_readings)}")
print(f"Range: {max(room_readings) - min(room_readings)}")
print(f"Mean: {np.mean(room_readings):.2f}")

print("\nHot Temperature Statistics (38.8°C):")
print(f"Min: {min(hot_readings)}, Max: {max(hot_readings)}")
print(f"Range: {max(hot_readings) - min(hot_readings)}")
print(f"Mean: {np.mean(hot_readings):.2f}")

print(f"\nFitted equation:")
print(f"Analog Value = {a:.2f} * e^({b:.4f} * T) + {c:.2f}")
print(f"\nTo convert analog value (AV) to temperature (T):")
print(f"T = ln((AV - {c:.2f})/{a:.2f}) / {b:.4f}")

# Calculate R-squared value
residuals = analog_values - thermistor_curve(temp_c, a, b, c)
ss_res = np.sum(residuals** 2)
ss_tot = np.sum((analog_values - np.mean(analog_values)) ** 2)
r_squared = 1 - (ss_res / ss_tot)
print(f"\nR-squared value: {r_squared:.4f}")

# Calculate linear approximation for simpler Arduino implementation
temp_points = np.array([8.5, 22.5, 38.8])
analog_means = np.array([
    np.mean(cold_readings),
    np.mean(room_readings),
    np.mean(hot_readings)
])

# Linear fit
slope, intercept = np.polyfit(analog_means, temp_points, 1)

# Calculate standard deviation of readings
cold_std = np.std(cold_readings)
room_std = np.std(room_readings)
hot_std = np.std(hot_readings)
overall_std = np.std([cold_std, room_std, hot_std])

print("\nLinear Approximation for Arduino:")
print(f"TEMP_SLOPE = {slope:.4f}")
print(f"TEMP_INTERCEPT = {intercept:.4f}")
print("\nControl System Parameters:")
print(f"const float setpointC = {22.5:.1f};    // Room temperature setpoint")
print(f"const float STD_DEV = {overall_std:.4f};        // Standard deviation of readings")
print(f"const int SIGMA_MULTIPLIER = 3;     // Using 3-sigma for control limits")

# Additional plot for linear approximation
analog_fit_linear = np.linspace(min(analog_means), max(analog_means), 100)
temp_fit_linear = slope * analog_fit_linear + intercept

plt.figure(figsize=(10, 6))
plt.scatter(analog_means, temp_points, color='red', label='Average Readings')
plt.plot(analog_fit_linear, temp_fit_linear, 'b-', label='Linear Approximation')
plt.xlabel('Analog Value')
plt.ylabel('Temperature (°C)')
plt.title('Linear Approximation for Arduino Implementation')
plt.grid(True)
plt.legend()
plt.show() 