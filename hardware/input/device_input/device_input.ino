#include <Keyboard.h>
#include "input_logic.h"

// Pins and keys: keep in sync with hardware/keymap.md
struct ButtonKey {
  uint8_t pin;
  uint8_t key;
  Button button;
};

ButtonKey buttons[] = {
  {2, KEY_RIGHT_ARROW, Button()},  // Next
  {3, KEY_LEFT_ARROW,  Button()},  // Back
  {4, KEY_PAGE_UP,     Button()},  // Button 3 (aux1)
  {5, KEY_PAGE_DOWN,   Button()},  // Button 4 (aux2)
  {6, KEY_RETURN,      Button()},  // Encoder press
};

const uint8_t PIN_ENC_A = 7;
const uint8_t PIN_ENC_B = 8;
Encoder encoder;

void setup() {
  for (ButtonKey& b : buttons) {
    pinMode(b.pin, INPUT_PULLUP);
  }
  pinMode(PIN_ENC_A, INPUT_PULLUP);
  pinMode(PIN_ENC_B, INPUT_PULLUP);
  Keyboard.begin();
  
}

void loop() {
  uint32_t now = millis();

  for (ButtonKey& b : buttons) {
    bool pinHigh = digitalRead(b.pin) == HIGH;
    if (b.button.update(pinHigh, now) == Button::PRESSED) {
      Keyboard.write(b.key);
    }
  }
  int8_t click = encoder.update(digitalRead(PIN_ENC_A) == HIGH,
                                digitalRead(PIN_ENC_B) == HIGH);
  if (click > 0) Keyboard.write(KEY_UP_ARROW);
  if (click < 0) Keyboard.write(KEY_DOWN_ARROW);
}