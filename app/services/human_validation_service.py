from app.models.extracted_order import ExtractedOrder
from app.models.order import Order
from app.graph.workflowStatus import WorkflowStatus


class HumanValidationService:

    MIN_CONFIDENCE = 0.90

    @staticmethod
    def validate(
        order: Order,
        extracted_order: ExtractedOrder,
    ) -> tuple[bool, WorkflowStatus, str | None]:

        if order.product is None:
            return (
                True,
                WorkflowStatus.WAITING_HUMAN_VALIDATION,
                "Product is missing.",
            )

        if order.length is None:
            return (
                True,
                WorkflowStatus.WAITING_HUMAN_VALIDATION,
                "Length is missing.",
            )

        if order.width is None:
            return (
                True,
                WorkflowStatus.WAITING_HUMAN_VALIDATION,
                "Width is missing.",
            )

        if order.height is None:
            return (
                True,
                WorkflowStatus.WAITING_HUMAN_VALIDATION,
                "Height is missing.",
            )

        if order.quantity <= 0:
            return (
                True,
                WorkflowStatus.WAITING_HUMAN_VALIDATION,
                "Invalid quantity.",
            )

        if extracted_order.confidence < HumanValidationService.MIN_CONFIDENCE:
            return (
                True,
                WorkflowStatus.WAITING_HUMAN_VALIDATION,
                "Low confidence.",
            )

        return (
            False,
            WorkflowStatus.VALIDATED,
            None,
        )