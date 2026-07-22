from app.models.order import Order


class OrderValidator:
    """
    Validate an Order according to business rules.
    """

    @staticmethod
    def validate(order: Order) -> tuple[Order, list[str]]:

        errors: list[str] = []

        # Product
        if not order.product:
            errors.append("Product is required.")

        # Length
        if order.length is None:
            errors.append("Length is required.")
        elif order.length <= 0:
            errors.append("Length must be greater than 0.")

        # Width
        if order.width is None:
            errors.append("Width is required.")
        elif order.width <= 0:
            errors.append("Width must be greater than 0.")

        # Height
        if order.height is None:
            errors.append("Height is required.")
        elif order.height <= 0:
            errors.append("Height must be greater than 0.")

        # Quantity
        if order.quantity is None:
            errors.append("Quantity is required.")
        elif order.quantity < 1:
            errors.append("Quantity must be at least 1.")

        # Client
        if not order.client_name:
            errors.append("Client name is missing.")

        # Validation status
        if errors:
            order.status = "INCOMPLETE"
            order.validation_required = True
        else:
            order.status = "READY_FOR_VALIDATION"
            order.validation_required = False

        return order, errors