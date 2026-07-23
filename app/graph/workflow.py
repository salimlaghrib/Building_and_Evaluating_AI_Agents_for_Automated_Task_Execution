from langgraph.graph import END, StateGraph

from app.graph.state import AgentState
from app.graph.workflowStatus import WorkflowStatus

from app.agents.communication_agent import CommunicationAgent
from app.agents.multimodal_ai_agent import MultimodalAIAgent
from app.agents.order_processing_agent import OrderProcessingAgent
from app.agents.platform_integration_agent import PlatformIntegrationAgent


# ==========================================================
# Agents
# ==========================================================

communication_agent = CommunicationAgent()
multimodal_agent = MultimodalAIAgent()
order_processing_agent = OrderProcessingAgent()
platform_integration_agent = PlatformIntegrationAgent()


# ==========================================================
# Nodes
# ==========================================================

def communication_node(state: AgentState):
    return communication_agent.run(state)


def multimodal_node(state: AgentState):
    return multimodal_agent.run(state)


def order_processing_node(state: AgentState):
    return order_processing_agent.run(state)


def platform_integration_node(state: AgentState):
    return platform_integration_agent.run(state)


# ==========================================================
# Routers
# ==========================================================

def communication_router(state: AgentState):

    if state["status"] == WorkflowStatus.FAILED:
        return "end"

    return "multimodal"


def multimodal_router(state: AgentState):

    if state["status"] == WorkflowStatus.FAILED:
        return "end"

    return "order_processing"


def order_router(state: AgentState):

    if state["status"] == WorkflowStatus.FAILED:
        return "end"

    return "platform"


# ==========================================================
# Graph
# ==========================================================

builder = StateGraph(AgentState)

builder.add_node(
    "communication",
    communication_node,
)

builder.add_node(
    "multimodal_ai",
    multimodal_node,
)

builder.add_node(
    "order_processing",
    order_processing_node,
)

builder.add_node(
    "platform_integration",
    platform_integration_node,
)

builder.set_entry_point("communication")


builder.add_conditional_edges(
    "communication",
    communication_router,
    {
        "multimodal": "multimodal_ai",
        "end": END,
    },
)

builder.add_conditional_edges(
    "multimodal_ai",
    multimodal_router,
    {
        "order_processing": "order_processing",
        "end": END,
    },
)

builder.add_conditional_edges(
    "order_processing",
    order_router,
    {
        "platform": "platform_integration",
        "end": END,
    },
)

builder.add_edge(
    "platform_integration",
    END,
)

graph = builder.compile()


def run_health_workflow():

    return {
        "status": "ok",
        "nodes": [
            "communication",
            "multimodal_ai",
            "order_processing",
            "platform_integration",
        ],
    }