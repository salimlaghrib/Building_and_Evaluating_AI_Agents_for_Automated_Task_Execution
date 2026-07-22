import httpx

from app.models.order import Order

from app.config import BASE_URL 


class PlatformService:
    """
    Service responsible for communicating with the business platform API.
    """

    

    @staticmethod
    def create_order(order: Order) -> dict:
        """
        Send an Order to the platform.

        Returns:
            dict: JSON response returned by the platform.

        Raises:
            httpx.HTTPStatusError
            httpx.RequestError
        """

        payload = {
            "client_name": order.client_name,
            "phone": order.phone,
            "email": order.email,
            # "address": order.address,
            "product": order.product,
            "length": order.length,
            "width": order.width,
            "height": order.height,
            "quantity": order.quantity,
        }

        response = httpx.post(
            url=f"{BASE_URL}/orders",
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()