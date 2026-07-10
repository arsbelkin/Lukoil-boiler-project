# список тегов
TAGS = {
    "ValveHotIn": {"writable": True, "initial": 0.5},
    "ValveColdIn": {"writable": True, "initial": 0.5},
    "ValveOut": {"writable": True, "initial": 1.0},
    # Температуры, °C
    "InputTempHot": {"writable": True, "initial": 85.0},
    "InputTempCold": {"writable": True, "initial": 15.0},
    "OutputTemp": {"writable": True, "initial": 0.0},
    # Уровень воды в баке, %
    "WaterLevel": {"writable": True, "initial": 0.0},
    # Флаг: запущена ли симуляция
    "StartSimulation": {"writable": True, "initial": False},
}
