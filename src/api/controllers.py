from .api_server import BASE_DIR, client
from .api_model import SetValueDTO

from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
from fastapi import status

import matplotlib.pyplot as plt
import numpy as np
import io

router = APIRouter()


@router.get("/", response_class=FileResponse)
def index():
    html_path = BASE_DIR / "ui" / "index.html"
    return FileResponse(html_path, media_type="text/html")


@router.get("/api/v1/data")
def get_data():
    return client.get_data()


@router.post("/api/v1/data")
def set_value(dto: SetValueDTO):
    try:
        client.set_value(dto.name, dto.value)
        return status.HTTP_200_OK
    except Exception as e:
        print(e)
        return status.HTTP_400_BAD_REQUEST


@router.get("/api/v1/graph")
def get_graph():
    g = create_graph()

    return Response(content=g.getvalue(), media_type="image/png")


def create_graph():
    X = np.linspace(-7, 17, 10000)
    Y1 = X**2
    Y2 = X**3

    fig, ax = plt.subplots(nrows=2, ncols=1)
    ax[0].plot(X, Y1)
    ax[1].plot(X, Y2)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")

    plt.close(fig)

    buf.seek(0)
    return buf
