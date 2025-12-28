from typing import List

from shared_kernel import Route

from .chat import ChatRouter

routes: List[Route] = [ChatRouter()]
