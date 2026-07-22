from langgraph.graph import END, StateGraph

from app.graph.state import AgentState

from app.agents.communication_agent import CommunicationAgent
from app.agents.multimodal_ai_agent import MultimodalAIAgent
from app.agents.order_processing_agent import OrderProcessingAgent
from app.agents.platform_integration_agent import PlatformIntegrationAgent


# Initialisation des agents
communication_agent = CommunicationAgent()
multimodal_agent = MultimodalAIAgent()
order_processing_agent = OrderProcessingAgent()
platform_integration_agent = PlatformIntegrationAgent()



# Nodes
def communication_node(state: AgentState):
    return communication_agent.run(state)


def multimodal_node(state: AgentState):
    return multimodal_agent.run(state)


def order_processing_node(state: AgentState):
    return order_processing_agent.run(state)


def platform_integration_node(state: AgentState):
    return platform_integration_agent.run(state)


# Workflow
builder = StateGraph(AgentState)

builder.add_node("communication", communication_node)
builder.add_node("multimodal_ai", multimodal_node)
builder.add_node("order_processing", order_processing_node)
builder.add_node("platform_integration", platform_integration_node)


builder.set_entry_point("communication")

builder.add_edge("communication", "multimodal_ai")
builder.add_edge("multimodal_ai", "order_processing")
builder.add_edge("order_processing", "platform_integration")
builder.add_edge("platform_integration", END)


graph = builder.compile()

def run_health_workflow() -> dict:
    return {
        "status": "ok",
        "nodes": [
            "communication",
            "multimodal_ai",
            "order_processing",
            "platform_integration",
        ],
    }