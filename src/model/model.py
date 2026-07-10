class BoilerModel:
    def __init__(self, max_volume=100.0, inputHotTemp=85.0, inputColdTemp=15.0):
        self.max_volume = max_volume

        self.inputHotTemp = inputHotTemp
        self.inputColdTemp = inputColdTemp
        self.outputTemp = 25.0

        self.waterLevel = 0.0

        self.valveHot = 50.0
        self.valveCold = 50.0
        self.valveOut = 100.0

    def step(self, dt=1.0):
        in_hot = self.valveHot / 100 * dt
        in_cold = self.valveCold / 100 * dt
        out = self.valveOut / 100 * dt

        old_volume = self.waterLevel
        incoming = in_hot + in_cold
        total_mass = old_volume + incoming

        if total_mass > 0 and incoming > 0:
            mixed_temp = (in_hot * self.inputHotTemp + in_cold * self.inputColdTemp) / (
                incoming + 1e-6
            )

            self.outputTemp = (self.outputTemp * old_volume + mixed_temp * incoming) / (
                total_mass + 1e-6
            )

        delta = incoming - out
        self.waterLevel = max(0.0, min(old_volume + delta, self.max_volume))

    def get_waterLevelPercent(self):
        return (self.waterLevel / self.max_volume) * 100.0
