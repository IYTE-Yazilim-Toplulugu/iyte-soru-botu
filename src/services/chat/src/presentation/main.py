from shared_kernel import App

from .config import Settings
from .routes.main import routes

app_instance = App(routes, Settings)
app = app_instance.app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.presentation.main:app", host="0.0.0.0", port=8080, reload=True)
