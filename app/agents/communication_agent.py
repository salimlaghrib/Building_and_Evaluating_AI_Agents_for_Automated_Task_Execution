from app.graph.state import AgentState
from app.graph.workflowStatus import WorkflowStatus
from app.logs.logger import logger


class CommunicationAgent:
    """
    First business agent of the workflow.

    Responsibilities:
        - Validate the incoming OrderMessage
        - Log communication information
        - Initialize workflow state
    """

    def run(self, state: AgentState) -> AgentState:

        order = state.get("order_message")

        print("\n=================================")
        print("Communication Agent")
        print("=================================")

        logger.info("\n=================================")
        logger.info("Communication Agent")
        logger.info("=================================")

        # -------------------------
        # OrderMessage validation
        # -------------------------

        if order is None:

            error = "OrderMessage not found."

            print(error)
            logger.error(error)

            state.setdefault("errors", []).append(error)
            state["status"] = WorkflowStatus.FAILED

            return state

        # -------------------------
        # Contact validation
        # -------------------------

        if not order.phone and not order.email:

            error = "Customer contact information is missing."

            print(error)
            logger.error(error)

            state.setdefault("errors", []).append(error)
            state["status"] = WorkflowStatus.FAILED

            return state

        # -------------------------
        # Image validation
        # -------------------------

        if not order.image_path:

            error = "No image received."

            print(error)
            logger.error(error)

            state.setdefault("errors", []).append(error)
            state["status"] = WorkflowStatus.FAILED

            return state

        # -------------------------
        # Logging
        # -------------------------

        print(f"Source      : {order.source}")

        logger.info(f"Source      : {order.source}")

        if order.phone:
            print(f"Phone       : {order.phone}")
            logger.info(f"Phone       : {order.phone}")

        if order.email:
            print(f"Email       : {order.email}")
            logger.info(f"Email       : {order.email}")

        if order.sender_name:
            print(f"Sender      : {order.sender_name}")
            logger.info(f"Sender      : {order.sender_name}")

        if order.message_text:
            print(f"Message     : {order.message_text}")
            logger.info(f"Message     : {order.message_text}")

        print(f"Image       : {order.image_path}")
        logger.info(f"Image       : {order.image_path}")

        print("Workflow started.")
        logger.info("Workflow started.")

        print("=================================\n")
        logger.info("=================================")

        # -------------------------
        # Update workflow state
        # -------------------------

        state["status"] = WorkflowStatus.RECEIVED
        state["current_agent"] = "CommunicationAgent"

        state.setdefault("steps", []).append(
            "CommunicationAgent completed"
        )

        return state