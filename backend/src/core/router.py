from fastapi_utils.inferring_router import InferringRouter
from common.schemas import AccessFailure, Message


class FastAPIRouter(InferringRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.route_mapping = {}
        self.responses = {
            401: {"model": Message},
            403: {"model": AccessFailure},
            404: {"model": Message},
            500: {"model": Message},
        }
