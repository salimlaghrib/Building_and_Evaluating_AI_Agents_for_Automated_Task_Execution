from app.agents.order_processing_agent import OrderProcessingAgent
from app.graph.state import AgentState

from app.models.order_message import OrderMessage
from app.models.extracted_order import ExtractedOrder
from datetime import datetime


def test_order_processing_agent_success():

    order_message = OrderMessage(
        source="WhatsApp",
        phone="+212612345678",
        email="ahmed@gmail.com",
        sender_name="Ahmed",
        message_text="Commande",
        image_path="uploads/raw/matelas_01.jpg",
        timestamp= datetime.now()
    )

    extracted_order = ExtractedOrder(
        client_name="Ahmed",
        # address="Casablanca",
        product="Matelas",
        length=200,
        width=160,
        height=25,
        quantity=2,
        confidence=0.98,
    )

    state: AgentState = {
        "order_message": order_message,
        "extracted_order": extracted_order,
        "errors": [],
    }

    result_state = OrderProcessingAgent()
    result = result_state.run(state=state)

    assert result["order"] is not None
    assert result["status"] == "READY_FOR_VALIDATION"
    assert result["validation_required"] is False
    assert result["errors"] == []