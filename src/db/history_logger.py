from asyncua.sync import Client
import time
from db.config import Config
from db.database_strategy import DatabaseContext, create_database_strategy


def main():
    # Определяем тип БД из конфигурации
    db_type = Config.get_db_type()
    print(f"🚀 Запуск логгера с базой данных: {db_type.upper()}")
    print("=" * 60)

    # Создаём стратегию и контекст
    strategy = create_database_strategy(db_type)
    db = DatabaseContext(strategy)

    # Инициализируем таблицы (создаём если нет)
    db.init_tables()

    # Подключение к OPC UA серверу
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")

    try:
        client.connect()
        print("✅ Исторический логгер подключён к OPC UA")
        print("=" * 60)

        # Получаем узлы бойлера
        boiler = client.get_root_node().get_child(["0:Objects", "2:Boiler"])
        input_temp_hot = boiler.get_child("2:InputTempHot")
        input_temp_cold = boiler.get_child("2:InputTempCold")
        valve_hot = boiler.get_child("2:ValveHotIn")
        valve_cold = boiler.get_child("2:ValveColdIn")
        valve_out = boiler.get_child("2:ValveOut")
        output_temp = boiler.get_child("2:OutputTemp")
        water_level = boiler.get_child("2:WaterLevel")

        print("📊 Логгер готов к работе...")
        print("Нажмите Ctrl+C для остановки\n")

        while True:
            # Читаем значения из OPC UA
            data = {
                "input_temp_hot": input_temp_hot.get_value(),
                "input_temp_cold": input_temp_cold.get_value(),
                "valve_hot": valve_hot.get_value(),
                "valve_cold": valve_cold.get_value(),
                "valve_out": valve_out.get_value(),
                "output_temp": output_temp.get_value(),
                "water_level": water_level.get_value(),
            }

            # Записываем в БД
            db.log_data(data)

            # Выводим в консоль
            print(
                f"💾 Запись: "
                f"T_hot={data['input_temp_hot']:.1f}°C, "
                f"T_cold={data['input_temp_cold']:.1f}°C, "
                f"V_hot={data['valve_hot']:.0f}%, "
                f"V_cold={data['valve_cold']:.0f}%, "
                f"V_out={data['valve_out']:.0f}%, "
                f"T_out={data['output_temp']:.1f}°C, "
                f"Level={data['water_level']:.1f}%"
            )

            time.sleep(5)

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
