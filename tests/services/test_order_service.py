from datetime import datetime

from app.models.order_message import OrderMessage
from app.models.extracted_order import ExtractedOrder
from app.models.order import Order
from app.services.order_service import OrderService


def create_order_message():
    return OrderMessage(
        source="WhatsApp",
        phone="+212612345678",
        email="ahmed@gmail.com",
        client_name="Ahmed",
        message_text="Je souhaite commander un matelas",
        image_path="uploads/raw/matelas_01.jpg",
        timestamp=datetime.now(),
    )


def create_extracted_order():
    return ExtractedOrder(
        client_name="Ahmed",
        product="Matelas",
        length=200,
        width=160,
        height=25,
        quantity=1,
        observations="Matelas mousse",
        confidence=0.98,
    )


def test_create_order_success():

    order_message = create_order_message()
    extracted_order = create_extracted_order()

    order = OrderService.create_order(
        order_message,
        extracted_order
    )

    assert isinstance(order, Order)

    assert order.client_name == "Ahmed"
    assert order.phone == "+212612345678"
    assert order.email == "ahmed@gmail.com"

    assert order.product == "Matelas"

    assert order.length == 200
    assert order.width == 160
    assert order.height == 25

    assert order.quantity == 1

    assert order.status == "PENDING"
    assert order.validation_required is True


def test_create_order_default_quantity():

    order_message = create_order_message()

    extracted_order = ExtractedOrder(
        client_name="Ahmed",
        product="Matelas",
        length=190,
        width=140,
        height=20,
        quantity=None,
        observations=None,
        confidence=0.95,
    )

    order = OrderService.create_order(
        order_message,
        extracted_order
    )

    assert order.quantity == 1


def test_create_order_without_email():

    order_message = OrderMessage(
        source="WhatsApp",
        phone="+212600000000",
        email=None,
        client_name="Salim",
        message_text="Commande",
        image_path="uploads/raw/matelas_01.jpg",
        timestamp=datetime.now(),
    )

    extracted_order = ExtractedOrder(
        client_name="Salim",
        product="Matelas",
        length=180,
        width=90,
        height=18,
        quantity=2,
        observations=None,
        confidence=0.99,
    )

    order = OrderService.create_order(
        order_message,
        extracted_order
    )

    assert order.email is None
    assert order.quantity == 2