from .optionsBoiler import BoilerOptions
from .valve import ValveModel, ValveOptions


class BoilerModel:
    def __init__(self, opt: BoilerOptions|None=None):
        if opt is None:
            opt = BoilerOptions()

        self.max_volume = opt.max_volume

        self.dt = opt.dt

        self.inputHotTemp = opt.inputHotTemp
        self.inputColdTemp = opt.inputColdTemp
        self.outputTemp = opt.outputTemp

        self.targetOutputTemp = opt.outputTemp

        self.waterLevel = opt.waterLevel

        self.valveHot = ValveModel(ValveOptions(level=opt.valveHot, dt=opt.dt))
        self.valveCold = ValveModel(ValveOptions(level=opt.valveCold, dt=opt.dt))
        self.valveOut = ValveModel(ValveOptions(level=opt.valveOut, dt=opt.dt))

        self.flowSpeed = opt.flowSpeed


    def step(self):
        self.stepValve()

        in_hot = self.valveHot.level / 100 * self.dt
        in_cold = self.valveCold.level / 100 * self.dt
        out = self.valveOut.level / 100 * self.dt

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

    def stepValve(self):
        self.valveHot.step()
        self.valveCold.step()
        self.valveOut.step()

    def get_waterLevelPercent(self):
        return (self.waterLevel / self.max_volume) * 100.0
