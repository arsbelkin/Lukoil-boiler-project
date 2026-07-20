from dataclasses import dataclass


@dataclass
class PIDOptions:
    kp: float = 2.1
    ki: float = 0.7
    kd: float = 0.6
    output_limits: tuple = (0.0, 1.0)

    dt: float = 1.0
