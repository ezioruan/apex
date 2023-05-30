import uvicorn

from .settings import settings
from .app import app


def start():
    print("Sample Service start", settings, app)
    uvicorn.run(
        "app.app:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
