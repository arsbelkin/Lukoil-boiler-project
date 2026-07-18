from .model import BoilerModel
from opc import OPCBoilerClient
import time


def start():
    model = BoilerModel()
    client = OPCBoilerClient()

    try:
        client.connect()
        print("opc клиент подключен")

        client.set_value("StartSimulation", True)
        print("Моделирование запущено (StartSimulation = True)")

        client.set_value("valveHot", model.valveHot.targetLevel)
        client.set_value("valveCold", model.valveCold.targetLevel)
        client.set_value("valveOut", model.valveOut.targetLevel)

        client.set_value("realValveHot", model.valveHot.level)
        client.set_value("realValveCold", model.valveCold.level)
        client.set_value("realValveOut", model.valveOut.level)

        while True:
            if not client.get_value("StartSimulation"):
                print("Ожидание запуска моделирования (StartSimulation = False)")
                time.sleep(1)
                continue

            model.valveHot.targetLevel = client.get_value("valveHot")
            model.valveCold.targetLevel = client.get_value("valveCold")
            model.valveOut.targetLevel = client.get_value("valveOut")

            model.step()

            client.set_value("realValveHot", model.valveHot.level)
            client.set_value("realValveCold", model.valveCold.level)
            client.set_value("realValveOut", model.valveOut.level)

            client.set_value("inputHotTemp", model.inputHotTemp)
            client.set_value("inputColdTemp", model.inputColdTemp)
            client.set_value("outputTemp", model.outputTemp)
            client.set_value("waterLevel", model.get_waterLevelPercent())

            time.sleep(1)

    except KeyboardInterrupt:
        print("остановка модели")

        client.set_value("StartSimulation", False)
        client.disconnect()
    except Exception as e:
        print(e)
    finally:
        print("opc клиент отключен")


if __name__ == "__main__":
    start()
