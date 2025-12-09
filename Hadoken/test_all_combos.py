import time

from combos import COMBO_DEFINITIONS, ComboStateMachine, InputEvent


ARROW_MAP = {
    "RIGHT": "→",
    "LEFT": "←",
    "UP": "↑",
    "DOWN": "↓",
    "SPACE": " ",
}


def to_arrow(symbol: str) -> str:
    return ARROW_MAP[symbol]


def simulate_combo(name: str, sequence: list[str], hold_space: bool = False) -> bool:
    fsm = ComboStateMachine()
    base = time.monotonic()
    delta = 0.0
    detected = None

    for idx, symbol in enumerate(sequence):
        button = to_arrow(symbol)
        action = "press"
        if symbol == "SPACE" and hold_space:
            # Press, wait 2.5s, then release for charged variant
            press_event = InputEvent(button=button, timestamp=base + delta, action="press")
            detected = fsm.handle_event(press_event) or detected
            delta += 2.5
            release_event = InputEvent(button=button, timestamp=base + delta, action="release")
            detected = fsm.handle_event(release_event) or detected
            continue

        event = InputEvent(button=button, timestamp=base + delta, action=action)
        detected = fsm.handle_event(event) or detected
        delta += 0.2  # keep under 1s timeout

    if not detected:
        return False
    return detected["combo"] == name and (detected.get("charged", False) == hold_space or not hold_space)


def run_all():
    passed = 0
    for name, seq in COMBO_DEFINITIONS.items():
        ok = simulate_combo(name, seq, hold_space=False)
        status = "OK" if ok else "FAIL"
        print(f"{status} - {name}")
        passed += 1 if ok else 0

    # Test charge on first combo
    first_name = next(iter(COMBO_DEFINITIONS))
    ok_charge = simulate_combo(first_name, COMBO_DEFINITIONS[first_name], hold_space=True)
    print(f"{'OK' if ok_charge else 'FAIL'} - {first_name} (charged)")
    passed += 1 if ok_charge else 0

    print(f"\nTotal lulus: {passed}/{len(COMBO_DEFINITIONS) + 1}")


if __name__ == "__main__":
    run_all()

