from shared_kernel import DomainException


class ModelNotAvailableException(DomainException):
    """Exception raised when an agent model is not available."""

    model_name: str

    def __init__(self, model_name: str):
        self.model_name = model_name
        super().__init__(f"The model '{model_name}' is not available.")
