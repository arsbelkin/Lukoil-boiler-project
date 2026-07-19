from dataclasses import dataclass


@dataclass
class ValveOptions:
    level: float = 0.0
    speed: float = 5.0
    dt: float = 1.0
