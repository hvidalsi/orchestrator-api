# src/tools/external_api_tool.py

from typing import Any, Dict, Optional

import requests

from models.exceptions import ExternalAPIError


class ExternalAPITool:
    """
    Utilitario para realizar peticiones a APIs externas.
    """

    def __init__(
        self,
        url: str,
        verify: bool = False,
        timeout: int = 60,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
    ):
        self.url = url
        self.verify = verify
        self.timeout = timeout
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.json = json

    def set_body(self, body: Dict[str, Any]) -> None:
        """
        Establece el cuerpo de la petición.
        """
        self.data = body

    def request(self) -> Dict[str, Any]:
        """
        Realiza una petición HTTP a una API externa.
        """
        try:
            response = requests.request(
                url=self.url,
                verify=self.verify,
                timeout=self.timeout,
                method=self.method,
                headers=self.headers,
                params=self.params,
                data=self.data,
                json=self.json,
            )
            response.raise_for_status()
            return {
                "status": response.status_code,
                "data": response.json()
                if "application/json" in response.headers.get("Content-Type", "")
                else response.text,
            }
        except ExternalAPIError as e:
            raise ExternalAPIError(f"Error en la petición a la API externa: {e}")
