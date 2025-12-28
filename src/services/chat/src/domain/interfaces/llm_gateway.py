from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Dict,
    List,
)

from ulid import ULID

from ..enums import Model
from ..models import AIResponse


class ILlmGateway(ABC):
    """
    Gateway interface for Large Language Model interactions.

    This is a domain interface that abstracts away the specific LLM provider.
    Infrastructure layer provides concrete implementations (BedrockAdapter, etc.)
    """

    @abstractmethod
    async def generate_response(
        self, user_id: ULID, messages: List[Dict[str, str]], **kwargs: Any
    ) -> AIResponse:
        """
        Generate an AI response given a conversation history.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model identifier to use
            **kwargs: Additional model-specific parameters

        Raises:
            LlmGatewayError: If generation fails
        """
        ...

    @abstractmethod
    async def generate_embedding(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate vector embedding for text.

        Args:
            text: Text to embed
            model: Optional embedding model to use

        Returns:
            Vector embedding as list of floats

        Raises:
            LlmGatewayError: If embedding fails
        """
        ...

    @abstractmethod
    def get_available_models(self) -> Model.values:
        """
        Get list of available models.

        Returns:
            List of model identifiers
        """
        ...
