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

// EC11-style rotary encoder: A and B pins with pull-ups, one full
// cycle (4 steps) per click, resting at A=HIGH, B=HIGH.
class Encoder {
public:
  // Call every loop. Returns +1 (clockwise click), -1 (anticlockwise), or 0.
  int8_t update(bool aHigh, bool bHigh) {
    uint8_t state = (aHigh ? 2 : 0) | (bHigh ? 1 : 0);   // two bits: A B
    if (state == last_) return 0;

    // Row = previous state, column = new state.
    // +1 / -1 for a valid step, 0 for an impossible jump.
    static const int8_t STEP[4][4] = {
      //  to 00  01  10  11
      {      0, -1, +1,  0 },   // from 00
      {     +1,  0,  0, -1 },   // from 01
      {     -1,  0,  0, +1 },   // from 10
      {      0, +1, -1,  0 },   // from 11
    };
    sum_ += STEP[last_][state];
    last_ = state;

    if (state != REST) return 0;      // only decide when back at rest

    int8_t click = 0;
    if (sum_ >= 2) click = +1;
    else if (sum_ <= -2) click = -1;
    sum_ = 0;
    return click;
  }

private:
  static const uint8_t REST = 0b11;
  uint8_t last_ = REST;
  int8_t sum_ = 0;
};