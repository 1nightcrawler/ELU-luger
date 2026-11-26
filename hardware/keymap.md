# Key map

The device's buttons and rotary encoder are read by an Arduino UNO R4,
which acts as a USB keyboard. Each input sends an ordinary key press, and
the app turns the key into a named action. Pages listen for the action,
not the key, so changing a key or pin never affects them.

| Control               | Pin            | Key          | Action  |
| --------------------- | -------------- | ------------ | ------- |
| Next button           | D2             | `ArrowRight` | `next`  |
| Back button           | D3             | `ArrowLeft`  | `prev`  |
| Button 3              | D4             | `PageUp`     | `aux1`  |
| Button 4              | D5             | `PageDown`   | `aux2`  |
| Encoder press         | D6             | `Enter`      | `press` |
| Encoder clockwise     | D7 (A), D8 (B) | `ArrowUp`    | `up`    |
| Encoder anticlockwise | D7 (A), D8 (B) | `ArrowDown`  | `down`  |

What `aux1`, `aux2`, `press`, `up` and `down` do is not decided yet. Each
page can give them its own meaning.

## Wiring

Each button is wired between its pin and GND. The encoder's middle pin (C)
goes to GND. The Arduino's internal pull-up resistors are used, so no
external resistors are needed.

## Why these keys

Only layout-independent keys are used (arrows, Page Up/Down, Enter). A USB
keyboard sends key positions, not characters, so a key like `+` could come
out differently if the Pi uses the Estonian layout.

A laptop keyboard sends the same keys, so the app can be developed and
tested without the hardware. On a Mac, Page Up/Down is `fn + ↑` / `fn + ↓`.