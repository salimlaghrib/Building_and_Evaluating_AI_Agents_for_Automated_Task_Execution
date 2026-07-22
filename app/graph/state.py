from typing import Optional, TypedDict

from app.graph.workflowStatus import WorkflowStatus
from app.models.extracted_order import ExtractedOrder
from app.models.order import Order
from app.models.order_message import OrderMessage


class AgentState(TypedDict, total=False):

    order_message: OrderMessage

    extracted_order: Optional[ExtractedOrder]

    order: Optional[Order]

    current_agent: str

    status: WorkflowStatus

    validation_required: bool

    validation_comment: Optional[str]

    validated_by: Optional[str]

    validation_date: Optional[str]

    errors: list[str]

    steps: list[str]