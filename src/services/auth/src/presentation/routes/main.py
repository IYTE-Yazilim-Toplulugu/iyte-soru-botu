from typing import List

from shared_kernel import Route

from .auth import AuthRouter
from .user import UserRouter

routes: List[Route] = [AuthRouter(), UserRouter()]
