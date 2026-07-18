from .pid_controller import PIDControllerModel
import time


def start():
    pid = PIDControllerModel()

    try:
        pid.connect()
        print("pid подключен")

        while True:
            if not (
                pid.client.get_value("StartSimulation") and pid.client.get_value("PID")
            ):
                pid.reset()
                time.sleep(1)
                continue

            pid.compute()

            time.sleep(1)

    except KeyboardInterrupt:
        print("остановка pid")

        pid.client.set_value("PID", False)
        pid.client.disconnect()
    except Exception as e:
        print(e)
    finally:
        print("PID отключен")


if __name__ == "__main__":
    start()
