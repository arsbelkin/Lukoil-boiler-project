from dataclasses import dataclass


@dataclass
class PIDOptions:
    kp: float = 2.0
    ki: float = 0.5
    kd: float = 1.0
    output_limits: tuple = (0.0, 1.0)

    dt: float = 1.0
