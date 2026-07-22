from datetime import datetime
from app.models.order import Order
from app.models.order_message import OrderMessage
from app.models.extracted_order import ExtractedOrder

class OrderService:
    """
    Responsible for building a business Order
    from OrderMessage and ExtractedOrder.
    """
    @staticmethod
    def create_order(
        order_message: OrderMessage,
        extracted_order: ExtractedOrder,
    ) -> Order:

        order = Order(
            client_name = extracted_order.client_name or order_message.sender_name,
            phone=order_message.phone,
            email=order_message.email,
            # address=extracted_order.address,
            product=extracted_order.product,
            length=extracted_order.length,
            width=extracted_order.width,
            height=extracted_order.height,
            quantity=extracted_order.quantity or 1,
            status="PENDING",
            validation_required=True,
            created_at=datetime.now(),
        )

        return order