from .api_server import BASE_DIR, client
from .api_model import SetValueDTO

from fastapi import APIRouter, Response, status, HTTPException
from fastapi.responses import FileResponse

from .graph import plot_graph

router = APIRouter()


@router.get("/", response_class=FileResponse)
def index():
    html_path = BASE_DIR / "ui" / "index.html"
    return FileResponse(html_path, media_type="text/html")


@router.get("/api/v1/data")
def get_data():
    try:
        return client.get_data()
    except Exception as e:
        print(f"API: {e}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка получения данных"
        )


@router.post("/api/v1/data", status_code=status.HTTP_200_OK, response_class=Response)
def set_value(dto: SetValueDTO):
    try:
        client.set_value("PID", dto.name == "outputTemp")

        client.set_value(dto.name, dto.value)

        return Response()

    except Exception as e:
        print(f"API: {e}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка установки значения"
        )


@router.get("/api/v1/graph")
def get_graph(limit: int = 11):
    try:
        g = plot_graph(limit=limit)

        return Response(content=g.getvalue(), media_type="image/png")
    except Exception as e:
        print(f"API: {e}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка графика"
        )
