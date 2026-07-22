from app.agents.communication_agent import CommunicationAgent
from app.agents.multimodal_ai_agent import MultimodalAIAgent
from app.communication.whatsapp.simulator import WhatsAppSimulator


def test_multimodal_agent_workflow():
    simulator = WhatsAppSimulator()
    order_message = simulator.simulate()

    state = {
        "order_message": order_message,
        "extracted_order": None,
        "status": "received",
        "validation_required": False,
        "errors": []
    }

    communication_agent = CommunicationAgent()
    state = communication_agent.run(state)

    multimodal_agent = MultimodalAIAgent()
    state = multimodal_agent.run(state)

    assert state["status"] is not None
    assert "errors" in state