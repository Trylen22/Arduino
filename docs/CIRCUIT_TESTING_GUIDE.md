# Circuit Testing Guide
## Environmental Monitoring System

This guide will help you systematically test each of your 5 circuits before combining them into the full system.

### Testing Order
1. **LED Indicator** (simplest, good starting point)
2. **Photoresistor** (light sensor)
3. **Thermistor** (temperature sensor)
4. **MQ-135 CO2 Sensor** (most complex sensor)
5. **Transistor-Controlled Fan** (actuator)

---

## 1. LED Indicator Test

### Hardware Setup
- Connect LED positive (longer leg) to Arduino pin 3
- Connect LED negative (shorter leg) to GND through a 220Ω resistor

### Software Test
1. Upload `test_led.ino` to your Arduino
2. Open Serial Monitor (9600 baud)
3. Test commands:
   - Send `1` to turn LED ON
   - Send `0` to turn LED OFF
   - Send `B` for blink pattern
   - Send `F` for fade pattern

### Expected Results
- LED should turn on/off immediately when commanded
- Blink pattern: 5 cycles of 1-second on/off
- Fade pattern: smooth fade in and out

---

## 2. Photoresistor Test

### Hardware Setup
- Connect one terminal of photoresistor to 5V
- Connect other terminal to Arduino pin A2
- Connect 10kΩ resistor between A2 and GND

### Software Test
1. Upload `test_photoresistor.ino` to your Arduino
2. Open Serial Monitor (9600 baud)
3. Observe readings:
   - Cover sensor with hand (should read low values)
   - Expose to bright light (should read high values)

### Expected Results
- Dark: 0-200 ADC values
- Low light: 200-400 ADC values
- Normal room light: 400-800 ADC values
- Bright light: 800-1023 ADC values

---

## 3. Thermistor Test

### Hardware Setup
- Connect one terminal of thermistor to 5V
- Connect other terminal to Arduino pin A5
- Connect 10kΩ resistor between A5 and GND

### Software Test
1. Upload `test_thermistor.ino` to your Arduino
2. Open Serial Monitor (9600 baud)
3. Test readings:
   - Room temperature should be ~20-25°C
   - Touch thermistor with finger (should increase)
   - Hold ice near thermistor (should decrease)

### Expected Results
- Room temperature: 20-25°C (68-77°F)
- Body temperature when touched: ~37°C (98.6°F)
- Readings should be stable and responsive to temperature changes

---

## 4. MQ-135 CO2 Sensor Test

### Hardware Setup
- Connect VCC to 5V
- Connect GND to GND
- Connect AOUT to Arduino pin A0
- Add 10kΩ load resistor between AOUT and GND

### Software Test
1. Upload `test_mq135_co2.ino` to your Arduino
2. Open Serial Monitor (9600 baud)
3. Test readings:
   - Clean air: ~400 ppm
   - Breathe near sensor (should increase)
   - Poor ventilation: 800-1000 ppm

### Expected Results
- Clean air: 400-600 ppm
- Poor ventilation: 800-1000 ppm
- Very poor air: 1000+ ppm
- Sensor needs warm-up time (2-3 minutes)

---

## 5. Transistor-Controlled Fan Test

### Hardware Setup
- Connect transistor base to Arduino pin 8 through 1kΩ resistor
- Connect transistor collector to fan positive
- Connect transistor emitter to GND
- Connect fan negative to GND
- Use 12V power supply for fan if needed

### Software Test
1. Upload `test_fan_transistor.ino` to your Arduino
2. Open Serial Monitor (9600 baud)
3. Test commands:
   - Send `1` to turn fan ON
   - Send `0` to turn fan OFF
   - Send `P` for pulse pattern
   - Send `S` for speed test

### Expected Results
- Fan should start/stop immediately when commanded
- Pulse pattern: 5 cycles of 1-second on/off
- Speed test: fan should run at different speeds

---

## Troubleshooting Tips

### Common Issues
1. **No response from sensor**: Check wiring and power connections
2. **Erratic readings**: Check for loose connections
3. **Fan not spinning**: Check transistor orientation and power supply
4. **LED not lighting**: Check resistor value and LED orientation

### Calibration Notes
- **Thermistor**: Adjust `THERMISTOR_NOMINAL` and `BETA_COEFFICIENT` for your specific thermistor
- **MQ-135**: Adjust `MQ135_RO` for your specific sensor
- **Photoresistor**: Values may vary based on your specific photoresistor

### Next Steps
Once all circuits are working individually:
1. Create the combined system sketch
2. Test all sensors together
3. Implement the LLM agent for intelligent control

---

## Testing Checklist

- [ ] LED turns on/off correctly
- [ ] LED responds to serial commands
- [ ] Photoresistor reads light levels
- [ ] Thermistor reads temperature accurately
- [ ] MQ-135 sensor provides CO2 readings
- [ ] Fan turns on/off with transistor control
- [ ] All serial communication works
- [ ] No hardware conflicts between circuits

Once you've checked off all items, you're ready to combine the circuits into the full system! 