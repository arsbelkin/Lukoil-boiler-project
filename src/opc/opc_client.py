from asyncua.sync import Client


class OPCBoilerClient:
    def __init__(self, endpoint="opc.tcp://localhost:4840/freeopcua/server/") -> None:
        self.client = Client(endpoint)
        self.nodes = dict()

    def connect(self):
        self.client.connect()

        boiler = self.client.get_root_node().get_child(["0:Objects", "2:Boiler"])

        for v in boiler.get_variables():
            name = v.read_display_name().Text
            self.nodes[name] = v

    def disconnect(self):
        self.client.disconnect()

    def get_value(self, tag_name):
        return self.nodes[tag_name].get_value()

    def set_value(self, tag_name, value):
        self.nodes[tag_name].set_value(value)

    def get_data(self):
        return {
            "inputHotTemp": self.nodes["InputTempHot"].get_value(),
            "inputColdTemp": self.nodes["InputTempCold"].get_value(),
            "outputTemp": self.nodes["OutputTemp"].get_value(),
            "waterLevel": self.nodes["WaterLevel"].get_value(),
            "valveHot": self.nodes["ValveHotIn"].get_value(),
            "valveCold": self.nodes["ValveColdIn"].get_value(),
            "valveOut": self.nodes["ValveOut"].get_value(),
        }
