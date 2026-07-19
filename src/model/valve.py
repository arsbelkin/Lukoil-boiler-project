from .optionsValve import ValveOptions


class ValveModel:
    def __init__(self, opt: ValveOptions | None = None):
        if opt is None:
            opt = ValveOptions()

        self.level = opt.level
        self.targetLevel = opt.level

        self.speed = opt.speed

        self.dt = opt.dt

    def step(self):
        maxdDelta = self.speed * self.dt

        if abs(self.targetLevel - self.level) <= maxdDelta:
            self.level = self.targetLevel
        else:
            if self.targetLevel > self.level:
                self.level += maxdDelta
            else:
                self.level -= maxdDelta
