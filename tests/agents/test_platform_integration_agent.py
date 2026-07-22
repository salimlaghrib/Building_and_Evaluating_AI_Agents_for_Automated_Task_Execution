from app.agents.platform_integration_agent import PlatformIntegrationAgent

from app.graph.state import AgentState

from app.models.order import Order

from app.services.platform_service import PlatformService


def test_platform_integration_agent(monkeypatch):

    def mock_create_order(order):

        return {
            "id": 10,
            "status": "CREATED"
        }

    monkeypatch.setattr(
        PlatformService,
        "create_order",
        mock_create_order,
    )

    state: AgentState = {

        "order": Order(
            client_name="Ahmed",
            phone="+212612345678",
            email="ahmed@gmail.com",
            address="Casablanca",
            product="Matelas",
            length=200,
            width=160,
            height=25,
            quantity=2,
            status="READY_FOR_VALIDATION",
            validation_required=False,
        ),

        "errors": []
    }

    agent = PlatformIntegrationAgent()

    result = agent.run(state)

    assert result["status"] == "completed"

    assert result["platform_response"]["status"] == "CREATED"

    assert result["platform_response"]["id"] == 10

    assert result["errors"] == []

    assert result["current_agent"] == "PlatformIntegrationAgent"