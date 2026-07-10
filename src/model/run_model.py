from model import BoilerModel
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

        model.valveHot = 50.0
        model.valveCold = 50.0
        model.valveOut = 100.0

        client.set_value("ValveHotIn", model.valveHot)
        client.set_value("ValveColdIn", model.valveCold)
        client.set_value("ValveOut", model.valveOut)

        while True:
            if not client.get_value("StartSimulation"):
                print("Ожидание запуска моделирования (StartSimulation = False)")
                time.sleep(1)
                continue

            model.valveHot = client.get_value("ValveHotIn")
            model.valveCold = client.get_value("ValveColdIn")
            model.valveOut = client.get_value("ValveOut")

            model.inputHotTemp = 85.0
            model.inputColdTemp = 15.0

            model.step()

            client.set_value("InputTempHot", model.inputHotTemp)
            client.set_value("InputTempCold", model.inputColdTemp)
            client.set_value("OutputTemp", model.outputTemp)
            client.set_value("WaterLevel", model.get_waterLevelPercent())

            time.sleep(1)

    except KeyboardInterrupt:
        print("остановка модели")
    except Exception as e:
        print(e)
    finally:
        client.set_value("StartSimulation", False)
        client.disconnect()
        print("opc клиент отключен")


if __name__ == "__main__":
    start()
