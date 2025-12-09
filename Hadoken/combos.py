from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, Optional

# Allowed input: arrows and literal space
BUTTON_ALIASES = {
    "→": "RIGHT",
    "←": "LEFT",
    "↑": "UP",
    "↓": "DOWN",
    " ": "SPACE",  # literal space
}


def normalize_button(raw: str) -> Optional[str]:
    """Return normalized button name or None if unsupported. Accepts only arrows or literal space."""
    if raw is None:
        return None
    if raw == " ":
        return "SPACE"
    normalized = raw.strip().upper()
    if normalized == "" and " " in raw:
        return "SPACE"
    return BUTTON_ALIASES.get(normalized)


@dataclass
class InputEvent:
    """
    Represents a button event.

    action: "press" or "release". Only SPACE releases are interpreted for
    charge detection; other releases are ignored by the FSM.
    """

    button: str
    timestamp: float
    action: str = "press"

    def normalized_button(self) -> Optional[str]:
        return normalize_button(self.button)


@dataclass
class ComboNode:
    transitions: Dict[str, "ComboNode"] = field(default_factory=dict)
    combo_name: Optional[str] = None


COMBO_DEFINITIONS: Dict[str, list[str]] = {
    "Hadoken": ["RIGHT", "RIGHT", "RIGHT", "SPACE"],
    "Shoryuken": ["UP", "DOWN", "UP", "RIGHT", "SPACE"],
    "Tatsumaki": ["LEFT", "RIGHT", "LEFT", "RIGHT", "SPACE"],
    "Dragon Punch": ["UP", "UP", "DOWN", "RIGHT", "SPACE"],
    "Hurricane Kick": ["RIGHT", "DOWN", "RIGHT", "RIGHT", "SPACE"],
    "Giga Hadoken": ["RIGHT", "RIGHT", "RIGHT", "DOWN", "UP", "RIGHT", "SPACE"],
    "Ultra Shoryuken": ["RIGHT", "RIGHT", "DOWN", "RIGHT", "UP", "DOWN", "RIGHT", "SPACE"],
    "Mega Tatsumaki": ["UP", "UP", "DOWN", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "SPACE"],
    "Final Dragon Punch": ["LEFT", "UP", "RIGHT", "RIGHT", "DOWN", "UP", "RIGHT", "SPACE"],
    "Ultimate Hurricane Kick": ["RIGHT", "RIGHT", "UP", "DOWN", "RIGHT", "UP", "RIGHT", "RIGHT", "SPACE"],
}


class ComboStateMachine:
    def __init__(self, timeout_seconds: float = 1.0):
        self.timeout_seconds = timeout_seconds
        self.root = ComboNode()
        self.current = self.root
        self.last_press_time: Optional[float] = None
        self.pending_combo: Optional[str] = None
        self.space_press_time: Optional[float] = None
        self._build_trie()

    def _build_trie(self) -> None:
        for name, sequence in COMBO_DEFINITIONS.items():
            node = self.root
            for symbol in sequence:
                node = node.transitions.setdefault(symbol, ComboNode())
            node.combo_name = name

    def reset(self) -> None:
        self.current = self.root
        self.last_press_time = None
        self.pending_combo = None
        self.space_press_time = None

    def handle_event(self, event: InputEvent):
        """
        Process a button press/release.

        Returns a dict with keys:
        - combo: name of combo
        - charged: bool indicating charged space
        - hold_duration: optional float if charged
        Otherwise returns None when no combo is completed.
        """
        normalized = event.normalized_button()
        if normalized is None:
            self.reset()
            return None

        if event.action == "release":
            return self._handle_release(normalized, event.timestamp)

        # Press flow with timeout handling
        if self.last_press_time is not None:
            if event.timestamp - self.last_press_time > self.timeout_seconds:
                self.reset()
        self.last_press_time = event.timestamp

        # Traverse transitions; allow restarting from root on mismatch
        next_node = self.current.transitions.get(normalized)
        if next_node is None:
            self.current = self.root
            next_node = self.current.transitions.get(normalized)

        if next_node is None:
            return None

        self.current = next_node

        if self.current.combo_name:
            # All combos end with SPACE, so defer emission until SPACE release
            self.pending_combo = self.current.combo_name
            if normalized == "SPACE":
                self.space_press_time = event.timestamp
            self.current = self.root
            return None
        return None

    def _handle_release(self, normalized_button: str, timestamp: float):
        if normalized_button != "SPACE":
            return None
        if not self.pending_combo or self.space_press_time is None:
            # Space dilepas tanpa combo lengkap
            return {"error": "incomplete_combo"}

        hold_duration = timestamp - self.space_press_time
        charged = 2.0 <= hold_duration <= 3.0
        result = {
            "combo": self.pending_combo,
            "charged": charged,
        }
        if charged:
            result["hold_duration"] = round(hold_duration, 3)

        # Cleanup after release
        self.pending_combo = None
        self.space_press_time = None
        self.current = self.root
        return result


def demo():
    """
    Quick scripted demo for sanity checks.
    """
    machine = ComboStateMachine()
    start = time.monotonic()
    steps = [
        ("→", 0.0),
        ("→", 0.2),
        ("→", 0.3),
        (" ", 0.4, "press"),
        (" ", 2.6, "release"),
        ("↑", 5.0),
        ("↓", 5.4),
        ("↑", 5.8),
        ("→", 6.1),
        (" ", 6.5),
    ]
    for step in steps:
        if len(step) == 2:
            button, delta = step
            action = "press"
        else:
            button, delta, action = step
        timestamp = start + delta
        event = InputEvent(button=button, timestamp=timestamp, action=action)
        output = machine.handle_event(event)
        if output:
            print(f"[{delta:4.1f}s] Detected -> {output}")


__all__ = [
    "BUTTON_ALIASES",
    "normalize_button",
    "InputEvent",
    "ComboNode",
    "COMBO_DEFINITIONS",
    "ComboStateMachine",
    "demo",
]

