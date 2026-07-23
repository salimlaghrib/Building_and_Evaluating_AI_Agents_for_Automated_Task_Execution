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

        # Gracefully handle missing fields from ``extracted_order``
        product_val = extracted_order.product or "Mattress"
        if product_val is None:
            product_val = "Mattress"
        order = Order(
            client_name=extracted_order.client_name or order_message.sender_name,
            phone=order_message.phone,
            email=order_message.email,
            # address=extracted_order.address,
            product=product_val,
            length=extracted_order.length or 0,
            width=extracted_order.width or 0,
            height=extracted_order.height or 0,
            quantity=extracted_order.quantity or 1,
            status="PENDING",
            validation_required=True,
            created_at=datetime.now(),
        )

        return order