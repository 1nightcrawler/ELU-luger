// Laptop tests for input_logic.h. Run from the repo root:
//   g++ -std=c++17 -o /tmp/test_input hardware/input/test/test_input_logic.cpp && /tmp/test_input

#include <cstdio>
#include <initializer_list>
#include "../device_input/input_logic.h"

static int failures = 0;

static void check(bool ok, const char* name) {
  printf("%s  %s\n", ok ? "PASS" : "FAIL", name);
  if (!ok) failures++;
}

// Feed the encoder a sequence of (A,B) states, written as 2-bit numbers: 0b11 = both HIGH.
static int turn(Encoder& enc, std::initializer_list<int> states) {
  int total = 0;
  for (int s : states) total += enc.update(s & 0b10, s & 0b01);
  return total;
}

int main() {
  // --- Encoder ---
  {
    Encoder e;
    check(turn(e, {0b01, 0b00, 0b10, 0b11}) == +1, "one click clockwise = +1");
  }
  {
    Encoder e;
    check(turn(e, {0b10, 0b00, 0b01, 0b11}) == -1, "one click anticlockwise = -1");
  }
  {
    Encoder e;
    int total = 0;
    for (int i = 0; i < 5; i++) total += turn(e, {0b01, 0b00, 0b10, 0b11});
    check(total == 5, "five clicks = five steps, not twenty");
  }
  {
    Encoder e;  // contacts chatter in the middle of a click
    check(turn(e, {0b01, 0b11, 0b01, 0b00, 0b01, 0b00, 0b10, 0b11}) == +1,
          "bouncy click still counts once");
  }
  {
    Encoder e;  // turned halfway, then back
    check(turn(e, {0b01, 0b00, 0b01, 0b11}) == 0, "half turn and back = nothing");
  }

  // --- Button ---
  {
    Button b;
    b.update(true, 0);                                     // released
    check(b.update(false, 100) == Button::NONE, "press not accepted instantly");
    b.update(true, 102);                                   // bounce
    b.update(false, 104);                                  // bounce
    check(b.update(false, 110) == Button::NONE, "bounce restarts the 10 ms timer");
    check(b.update(false, 114) == Button::PRESSED, "steady for 10 ms = PRESSED");
    check(b.update(false, 200) == Button::NONE, "PRESSED reported only once");
    b.update(true, 300);
    check(b.update(true, 310) == Button::RELEASED, "release reported");
  }

  printf(failures ? "\n%d FAILED\n" : "\nAll tests passed\n", failures);
  return failures ? 1 : 0;
}