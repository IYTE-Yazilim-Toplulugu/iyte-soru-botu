from shared_kernel import (
    App,
    DomainException,
)

from .config import settings
from .middleware import exception_handler
from .routes import routes

app_instance = App(routes, settings)
app = app_instance.app

# Register global exception handlers
app.add_exception_handler(DomainException, exception_handler.handle_domain_exception)
app.add_exception_handler(ValueError, exception_handler.handle_validation_exception)
app.add_exception_handler(Exception, exception_handler.handle_generic_exception)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.presentation.main:app", host="0.0.0.0", port=8080, reload=True)
