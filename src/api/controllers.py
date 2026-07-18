from .api_server import BASE_DIR, client
from .api_model import SetValueDTO

from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
from fastapi import status

from .graph import plot_graph

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
    g = plot_graph()

    return Response(content=g.getvalue(), media_type="image/png")
