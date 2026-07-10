import time
from opc import OPCBoilerServer

if __name__ == "__main__":
    server = OPCBoilerServer()
    try:
        server.start()
        print("OPC UA сервер запущен: opc.tcp://localhost:4840")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Остановка сервера...")
    finally:
        server.stop()
