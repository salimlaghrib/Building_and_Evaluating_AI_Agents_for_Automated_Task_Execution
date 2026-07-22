from app.graph.state import AgentState
from app.graph.workflowStatus import WorkflowStatus
from app.logs.logger import logger
from app.services.order_service import OrderService
from app.validators.order_validator import OrderValidator


class OrderProcessingAgent:
    """
    Business Agent.

    Responsibilities:
    - Read the workflow state
    - Build a business Order
    - Validate the Order
    - Update the workflow state
    """

    def run(self, state: AgentState) -> AgentState:

        print("\n====================================")
        print("Order Processing Agent")
        print("====================================")

        logger.info("====================================")
        logger.info("Order Processing Agent")
        logger.info("====================================")

        # Vérifier que les données nécessaires existent
        if not state.get("order_message"):

            error = "Order message not found."

            print(error)
            logger.error(error)

            state.setdefault("errors", []).append(error)
            state["status"] = WorkflowStatus.FAILED

            return state

        if not state.get("extracted_order"):

            error = "Extracted order not found."

            print(error)
            logger.error(error)

            state.setdefault("errors", []).append(error)
            state["status"] =  WorkflowStatus.FAILED

            return state

        # Construction de la commande métier
        order = OrderService.create_order(
            order_message=state["order_message"],
            extracted_order=state["extracted_order"],
        )

        print("Business order created.")
        logger.info("Business order created.")

        # Validation métier
        order, errors = OrderValidator.validate(order)

        if errors:
            print("Validation errors detected:")
            logger.warning("Validation errors detected:")

            for error in errors:
                print(f"- {error}")
                logger.warning(error)
        else:
            print("Order validation successful.")
            logger.info("Order validation successful.")

        # Mise à jour du workflow
        state["order"] = order
        state["errors"] = state.get("errors", []) + errors
        state["status"] = order.status
        state["validation_required"] = order.validation_required
        state["current_agent"] = "OrderProcessingAgent"

        print(f"Status : {order.status}")
        print("Order Processing completed.")
        print("====================================\n")

        logger.info(f"Status : {order.status}")
        logger.info("Order Processing completed.")
        logger.info("====================================")

        return state