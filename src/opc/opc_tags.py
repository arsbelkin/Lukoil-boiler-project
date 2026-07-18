# список тегов
TAGS = {
    # Клапаны цель
    "valveHot": {"writable": True, "initial": 0.5},
    "valveCold": {"writable": True, "initial": 0.5},
    "valveOut": {"writable": True, "initial": 1.0},
    # Клапаны
    "realValveHot": {"writable": True, "initial": 0.5},
    "realValveCold": {"writable": True, "initial": 0.5},
    "realValveOut": {"writable": True, "initial": 1.0},
    # Температуры, °C
    "inputHotTemp": {"writable": True, "initial": 85.0},
    "inputColdTemp": {"writable": True, "initial": 15.0},
    "realOutputTemp": {"writable": True, "initial": 0.0},
    # таргет температура на выходе
    "outputTemp": {"writable": True, "initial": 0.0},
    # Уровень воды в баке, %
    "waterLevel": {"writable": True, "initial": 0.0},
    # Флаг: запущена ли симуляция
    "StartSimulation": {"writable": True, "initial": False},
    "PID": {"writable": True, "initial": False},
}
