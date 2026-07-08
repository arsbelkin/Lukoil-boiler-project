from asyncua.sync import Server
from opc_tags import TAGS


class OPCBoilerServer:
    def __init__(self, endpoint="opc.tcp://0.0.0.0:4840/freeopcua/server/"):    # функция для определения сервера
        self.server = Server()                          
        self.server.set_endpoint(endpoint)              
        uri = "http://example.org/boiler/"
        self.idx = self.server.register_namespace(uri)  
        self.nodes = {}
        self._setup_nodes()

    def _setup_nodes(self):     # функция для добавления объектов внутрь бойлера 
        boiler = self.server.nodes.objects.add_object(self.idx, "Boiler")
        for name, props in TAGS.items():
            node = boiler.add_variable(self.idx, name, props["initial"])
            if props.get("writable", False):
                node.set_writable()
            self.nodes[name] = node

    def start(self):    # функция старта сервера 
        self.server.start()                             

    def stop(self):     # функция останвоки сервера 
        self.server.stop()

    def get_value(self, name):   # функция для получения значения определенного датчика из бойлера
        return self.nodes[name].read_value()

    def set_value(self, name, value):     # функция для изменения значения, например поставить кран с 0.5 на 0.7
        self.nodes[name].write_value(value)