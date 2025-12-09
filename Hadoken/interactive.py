import sys
import time
from collections import deque

try:
    import keyboard  # type: ignore
except ImportError:
    keyboard = None

from combos import ComboStateMachine, InputEvent


ARROW_KEYS = {
    "up": "↑",
    "down": "↓",
    "left": "←",
    "right": "→",
}


def interactive():
    if keyboard is None:
        print("Library 'keyboard' belum terpasang. Jalankan: pip install keyboard")
        sys.exit(1)

    fsm = ComboStateMachine()
    space_down = False
    space_pressed_at = None
    last_event_time = None
    events = deque()

    def handler(e):
        # e.event_type: 'down' or 'up'; e.name: key name
        events.append(e)

    keyboard.hook(handler)

    print("Mode interaktif (real-time): panah atau spasi. q/Esc untuk keluar.")
    print("Spasi: tahan 2-3 detik untuk special. Tidak perlu dua kali spasi.")

    try:
        while True:
            now = time.monotonic()

            # Idle reset (jeda > 1s) kecuali sedang menahan spasi
            if (
                last_event_time is not None
                and not space_down
                and now - last_event_time > fsm.timeout_seconds
            ):
                fsm.reset()
                last_event_time = None

            if not events:
                time.sleep(0.01)
                continue

            e = events.popleft()
            key = e.name
            event_type = e.event_type
            now = time.monotonic()

            if key in ("esc", "q"):
                break

            # Map arrows
            if key in ARROW_KEYS and event_type == "down":
                last_event_time = now
                event = InputEvent(button=ARROW_KEYS[key], timestamp=now, action="press")
                output = fsm.handle_event(event)
                if output and "combo" in output:
                    print(f"TERDETEKSI -> {output}")
                continue

            # Space handling with real hold
            if key == "space":
                if event_type == "down":
                    last_event_time = now
                    space_down = True
                    space_pressed_at = now
                    event = InputEvent(button=" ", timestamp=now, action="press")
                    _ = fsm.handle_event(event)  # defer result until release
                elif event_type == "up" and space_down:
                    last_event_time = now
                    space_down = False
                    duration = now - (space_pressed_at or now)
                    event = InputEvent(button=" ", timestamp=now, action="release")
                    output = fsm.handle_event(event)
                    if output:
                        if "error" in output:
                            print("Combo tidak lengkap")
                        else:
                            print(f"TERDETEKSI -> {output}")
                continue

    except KeyboardInterrupt:
        print("\nKeluar.")
    finally:
        keyboard.unhook(handler)


if __name__ == "__main__":
    interactive()

