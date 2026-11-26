#pragma once
#include <stdint.h>

// One push button wired from a pin to GND with a pull-up:
// the pin reads HIGH when released and LOW when pressed.
class Button {
public:
  enum Event { NONE, PRESSED, RELEASED };

  // Call every loop with the pin level and the current time (millis()).
  Event update(bool pinHigh, uint32_t nowMs) {
    bool pressed = !pinHigh;

    if (pressed != candidate_) {      // level changed: start timing again
      candidate_ = pressed;
      changedAt_ = nowMs;
      return NONE;
    }
    if (candidate_ != stable_ && nowMs - changedAt_ >= DEBOUNCE_MS) {
      stable_ = candidate_;           // held long enough: accept it
      return stable_ ? PRESSED : RELEASED;
    }
    return NONE;
  }

private:
  static const uint32_t DEBOUNCE_MS = 10;
  bool candidate_ = false;   // latest level we've seen
  bool stable_ = false;      // level we've accepted
  uint32_t changedAt_ = 0;   // when the latest level started
};