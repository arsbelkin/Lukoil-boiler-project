from dataclasses import dataclass


@dataclass
class BoilerOptions:
    max_volume: float = 100.0

    inputHotTemp: float = 85.0
    inputColdTemp: float = 15.0
    outputTemp: float = 25.0

    waterLevel: float = 0.0

    valveHot: float = 50.0
    valveCold: float = 50.0
    valveOut: float = 100.0

    flowSpeed: float = 1.0
    valveSpeed: float = 2.0

    dt: float = 1.0

    criticalLevel: float = 95.0
