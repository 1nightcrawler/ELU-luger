#include <Keyboard.h>

const int PIN_NEXT = 2;

void setup() {
  pinMode(PIN_NEXT, INPUT_PULLUP);  // pin reads HIGH; pressing the button pulls it to GND (LOW)
  Keyboard.begin();
}

void loop() {
  if (digitalRead(PIN_NEXT) == LOW) {
    Keyboard.write(KEY_RIGHT_ARROW);
    delay(300);                      // crude: stops one press from typing many arrows
  }
}