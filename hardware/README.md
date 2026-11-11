# Hardware

Device-level setup for the Raspberry Pi 400: everything that runs on the Pi
itself rather than in the Flask app. Nothing here should import from `app/`
or change `app/models.py`.

## Planned contents

- `boot/` – `config.txt` snippets (e.g. `gpio-key` overlays that turn buttons into keyboard keys)
- `systemd/` – service units that start Flask and the Chromium kiosk at boot
- `input/` – rotary encoder script (gpiozero + uinput)
- `audio/` – sound card and PipeWire configuration notes
- `wiring.md` – pin assignments and wiring diagram

## Reserved pins

Keep these free for later use:

- GPIO 2/3 – I²C (UPS board, haptic driver)
- GPIO 18–21 – I²S (possible audio upgrade)

Buttons are wired from a GPIO pin to GND and use the internal pull-ups.
