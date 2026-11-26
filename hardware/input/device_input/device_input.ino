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

void setup() {
  for (ButtonKey& b : buttons) {
    pinMode(b.pin, INPUT_PULLUP);
  }
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
}