import httpx

from app.models.order import Order
from app.services.platform_service import PlatformService


class MockResponse:

    def raise_for_status(self):
        pass

    def json(self):
        return {
            "id": 1,
            "status": "CREATED"
        }


def test_create_order(monkeypatch):

    def mock_post(url, json, timeout):

        assert "/orders" in url
        assert json["client_name"] == "Ahmed"
        assert timeout == 10

        return MockResponse()

    monkeypatch.setattr(httpx, "post", mock_post)

    order = Order(
        client_name="Ahmed",
        phone="+212612345678",
        email="ahmed@gmail.com",
        # address="Casablanca",
        product="Matelas",
        length=200,
        width=160,
        height=25,
        quantity=2,
        status="READY_FOR_VALIDATION",
        validation_required=False,
    )

    response = PlatformService.create_order(order)

    assert response["id"] == 1
    assert response["status"] == "CREATED"