import os
from typing import Any, Optional, List, Dict
from .api_client import APIClientBase


class Central(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(url_base or os.environ.get("CENTRAL_SERVICE", ""), **kwargs)

    def activate_product(
        self, email: str, password: str, activation_key: Optional[str]
    ) -> Any:
        body: Dict = {
            "email": email,
            "password": password,
            "activation_key": activation_key,
        }
        return self.post_request("/services/licensing", body=body)

    def sync(self) -> Any:
        return self.post_request("/sync")

    def configure_monitoring(self, exporters: List[Any]) -> Any:
        body: Dict = {
            "exporters": exporters,
        }
        return self.post_request("/services/monitoring", body=body)

    def get_monitoring_details(self) -> Any:
        return self.get_request("/services/monitoring")