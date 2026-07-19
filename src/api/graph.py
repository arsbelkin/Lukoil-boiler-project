from db.db_repository import DatabaseRepositoryPattern

from matplotlib.figure import Figure
from matplotlib import style

import io

db = DatabaseRepositoryPattern()


def plot_graph(limit: int = 11):
    time_array = []
    temp_array = []
    level_array = []

    data = db.get_history(limit)

    for elem in data:
        time_array.append(elem["timestamp"])
        temp_array.append(elem["output_temp"])
        level_array.append(elem["water_level"])

    with style.context("seaborn-v0_8"):
        fig = Figure(figsize=(10, 8))
        ax = fig.subplots(nrows=2, ncols=1)

    ax[0].scatter(time_array, temp_array, color="navy", s=35)
    ax[0].plot(time_array, temp_array, color="darkorange", linewidth=3)

    ax[0].set_xlabel("время")
    ax[0].set_ylabel("температура")
    ax[0].grid()

    ax[1].scatter(time_array, level_array, color="red", s=35)
    ax[1].plot(time_array, level_array, linewidth=3, color="darkslateblue")

    ax[1].set_xlabel("время")
    ax[1].set_ylabel("уровень воды")
    ax[1].grid()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")

    buf.seek(0)
    return buf
