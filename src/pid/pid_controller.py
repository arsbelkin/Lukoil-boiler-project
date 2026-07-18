from .optionsPID import PIDOptions
from opc.opc_client import OPCBoilerClient


class PIDControllerModel:
    def __init__(self, opt: PIDOptions | None = None) -> None:
        if opt is None:
            opt = PIDOptions()

        self.dt = opt.dt

        self.kp = opt.kp
        self.ki = opt.ki
        self.kd = opt.kd

        self.output_limits = opt.output_limits

        self._integral = 0.0
        self._last_error = 0.0
        self._has_last_error = False

        self.client = OPCBoilerClient()

    def compute(self):
        if self.dt <= 0:
            return self.output_limits[0]
        
        setpoint = self.client.get_value("outputTemp")
        measurement = self.client.get_value("realOutputTemp")

        error = setpoint - measurement

        p_term = self.kp * error

        self._integral += error * self.dt
        i_term = self.ki * self._integral

        if self._has_last_error:
            d_term = self.kd * (error - self._last_error) / self.dt
        else:
            d_term = 0.0
            self._has_last_error = True

        self._last_error = error

        output = p_term + i_term + d_term

        min_limit, max_limit = self.output_limits
        if output > max_limit:
            output = max_limit
            self._integral -= error * self.dt
        elif output < min_limit:
            output = min_limit
            self._integral -= error * self.dt

        hot_ratio = output
        cold_ratio = 1.0 - hot_ratio

        total_flow = self.client.get_value("realValveOut")

        target_hot = total_flow * hot_ratio
        target_cold = total_flow * cold_ratio

        self.client.set_value("valveHot", target_hot)
        self.client.set_value("valveCold", target_cold)

    def reset(self):
        self._integral = 0.0
        self._last_error = 0.0
        self._has_last_error = False

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()
