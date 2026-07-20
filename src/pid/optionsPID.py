from dataclasses import dataclass


@dataclass
class PIDOptions:
    kp: float = 0.4
    ki: float = 0.7
    kd: float = 0.001
    output_limits: tuple = (0.0, 1.0)

    dt: float = 1.0
