import time

from db.config import Config
from db.db_repository import DatabaseRepositoryPattern
from .fabric import FabricDBStategy

from opc.opc_client import OPCBoilerClient


def main():
    db_type = Config.get_db_type()
    print(f"🚀 Запуск логгера с базой данных: {db_type.upper()}")
    print("=" * 60)

    strategy = FabricDBStategy(db_type)
    db = DatabaseRepositoryPattern(strategy)

    db.init_tables()

    client = OPCBoilerClient()

    try:
        client.connect()

        print("✅ Исторический логгер подключён к OPC UA")
        print("=" * 60)

        print("📊 Логгер готов к работе...")
        print("Нажмите Ctrl+C для остановки\n")

        while True:
            data = client.get_data()

            db.log_data(data)

            print(
                f"💾 Запись: "
                f"T_hot={data['inputHotTemp']:.1f}°C, "
                f"T_cold={data['inputColdTemp']:.1f}°C, "
                f"V_hot={data['valveHot']:.0f}%, "
                f"V_cold={data['valveCold']:.0f}%, "
                f"V_out={data['valveOut']:.0f}%, "
                f"T_out={data['outputTemp']:.1f}°C, "
                f"Level={data['waterLevel']:.1f}%"
            )

            time.sleep(3)

    except KeyboardInterrupt:
        print("\n⏹️  Остановка логгера по команде пользователя...")
    except Exception as e:
        print(f"❌ Ошибка логгера: {e}")
    finally:
        client.disconnect()
        db.close()
        print("🔌 Логгер остановлен. Соединения закрыты.")


if __name__ == "__main__":
    main()
