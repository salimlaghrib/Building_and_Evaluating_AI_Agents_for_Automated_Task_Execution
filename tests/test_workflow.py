from datetime import datetime

from app.graph.workflow import graph

from app.graph.state import AgentState

from app.models.order_message import OrderMessage
from app.models.extracted_order import ExtractedOrder

from app.services.vision_service import VisionService
from app.services.platform_service import PlatformService


def test_complete_workflow(monkeypatch):

    # -------------------------
    # Mock Vision
    # -------------------------

    def mock_extract(self, image_path):
        return ExtractedOrder(
            client_name="Ahmed",
            product="Matelas",
            length=200,
            width=160,
            height=25,
            quantity=2,
            confidence=0.98,
        )

    monkeypatch.setattr(
        VisionService,
        "analyze",
        mock_extract,
    )

    # -------------------------
    # Mock Platform
    # -------------------------

    def mock_create(order):

        return {
            "id": 1,
            "status": "CREATED"
        }

    monkeypatch.setattr(
        PlatformService,
        "create_order",
        mock_create,
    )

    # -------------------------
    # Initial State
    # -------------------------

    state: AgentState = {

        "order_message": OrderMessage(
            source="WhatsApp",
            phone="+212612345678",
            email="ahmed@gmail.com",
            sender_name="Ahmed",
            # address="Casablanca",
            message_text="Commande",
            image_path="uploads/raw/matelas_01.jpg",
            timestamp=datetime.now()
        ),

        "errors": []
    }

    # -------------------------
    # Execute Workflow
    # -------------------------

    result = graph.invoke(state)

    # -------------------------
    # Assertions
    # -------------------------

    assert result["status"] == "completed"

    assert result["order"] is not None

    # assert result["platform_response"]["status"] == "CREATED"

    # assert result["platform_response"]["id"] == 1

    assert result["errors"] == []