/*
FastLED Demo - Simple LED Strip Control
=======================================

A simple demo for controlling a FastLED strip on pin 4.
Includes basic effects and serial control.

Hardware:
- FastLED strip connected to pin 4
- Optional: Serial monitor for control

Author: Your Creative Assistant
Date: 2025-01-27
*/

#include <FastLED.h>

// Configuration
#define LED_PIN     4        // FastLED strip on pin 4
#define NUM_LEDS    16       // Number of LEDs in your strip (adjust as needed)
#define BRIGHTNESS  50       // Brightness (0-255)
#define LED_TYPE    WS2812B  // LED type (change if different)
#define COLOR_ORDER GRB      // Color order (change if different)

// Create LED array
CRGB leds[NUM_LEDS];

// Effect variables
int currentEffect = 0;
int hue = 0;
int position = 0;
bool direction = true;

void setup() {
  // Initialize FastLED
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  
  // Initialize serial for control
  Serial.begin(9600);
  Serial.println("FastLED Demo Ready!");
  Serial.println("Commands:");
  Serial.println("  '1' - Rainbow wave");
  Serial.println("  '2' - Solid color");
  Serial.println("  '3' - Breathing effect");
  Serial.println("  '4' - Moving dot");
  Serial.println("  '5' - Fire effect");
  Serial.println("  '0' - Turn off");
  Serial.println("  'b' - Increase brightness");
  Serial.println("  'd' - Decrease brightness");
  
  // Start with a nice rainbow effect
  currentEffect = 1;
}

void loop() {
  switch(currentEffect) {
    case 0: // Off
      turnOff();
      break;
    case 1: // Rainbow wave
      rainbowWave();
      break;
    case 2: // Solid color
      solidColor();
      break;
    case 3: // Breathing
      breathing();
      break;
    case 4: // Moving dot
      movingDot();
      break;
    case 5: // Fire effect
      fireEffect();
      break;
  }
  
  // Check for serial commands
  if (Serial.available()) {
    char command = Serial.read();
    processCommand(command);
  }
  
  FastLED.show();
  delay(50); // Control speed
}

void processCommand(char command) {
  switch(command) {
    case '0':
      currentEffect = 0;
      Serial.println("Effect: OFF");
      break;
    case '1':
      currentEffect = 1;
      Serial.println("Effect: Rainbow Wave");
      break;
    case '2':
      currentEffect = 2;
      Serial.println("Effect: Solid Color");
      break;
    case '3':
      currentEffect = 3;
      Serial.println("Effect: Breathing");
      break;
    case '4':
      currentEffect = 4;
      Serial.println("Effect: Moving Dot");
      break;
    case '5':
      currentEffect = 5;
      Serial.println("Effect: Fire");
      break;
    case 'b':
      FastLED.setBrightness(min(255, FastLED.getBrightness() + 25));
      Serial.print("Brightness: ");
      Serial.println(FastLED.getBrightness());
      break;
    case 'd':
      FastLED.setBrightness(max(0, FastLED.getBrightness() - 25));
      Serial.print("Brightness: ");
      Serial.println(FastLED.getBrightness());
      break;
  }
}

// Effect functions
void turnOff() {
  fill_solid(leds, NUM_LEDS, CRGB::Black);
}

void rainbowWave() {
  fill_rainbow(leds, NUM_LEDS, hue, 255/NUM_LEDS);
  hue++;
}

void solidColor() {
  fill_solid(leds, NUM_LEDS, CHSV(hue, 255, 255));
  hue += 2;
}

void breathing() {
  uint8_t brightness = sin8(millis() / 10);
  fill_solid(leds, NUM_LEDS, CHSV(hue, 255, brightness));
  hue += 1;
}

void movingDot() {
  // Clear all LEDs
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  
  // Draw moving dot
  leds[position] = CHSV(hue, 255, 255);
  
  // Move dot
  if (direction) {
    position++;
    if (position >= NUM_LEDS) {
      direction = false;
      hue += 30; // Change color
    }
  } else {
    position--;
    if (position < 0) {
      direction = true;
      hue += 30; // Change color
    }
  }
}

void fireEffect() {
  // Simple fire effect
  for (int i = 0; i < NUM_LEDS; i++) {
    int heat = random(0, 255);
    leds[i] = HeatColor(heat);
  }
} 