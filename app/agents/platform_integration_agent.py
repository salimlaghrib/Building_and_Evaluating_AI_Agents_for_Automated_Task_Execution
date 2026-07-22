from app.graph.workflowStatus import WorkflowStatus
from app.logs.logger import logger
from app.graph.state import AgentState
from app.services.platform_service import PlatformService


class PlatformIntegrationAgent:
    """
    Responsible for sending the business order
    to the external platform.
    """

    def run(self, state: AgentState) -> AgentState:

        print("\n====================================")
        print("Platform Integration Agent")
        print("====================================")

        logger.info("====================================")
        logger.info("Platform Integration Agent")
        logger.info("====================================")

        # Vérifier qu'une commande existe
        if not state.get("order"):

            error = "Order not found."

            print(error)
            logger.error(error)

            state.setdefault("errors", []).append(error)
            state["status"] =  WorkflowStatus.FAILED

            return state

        try:

            response = PlatformService.create_order(
                state["order"]
            )

            state["platform_response"] = response
            state["status"] =  WorkflowStatus.COMPLETED
            
            state["current_agent"] = "PlatformIntegrationAgent"

            print("Order successfully sent to the platform.")
            print(f"Platform Response : {response}")

            logger.info("Order successfully sent to the platform.")
            logger.info(f"Platform Response : {response}")

        except Exception as e:

            print(f"Platform error : {e}")

            logger.error(str(e))

            state.setdefault("errors", []).append(str(e))
            state["status"] = WorkflowStatus.FAILED

        print("====================================\n")

        logger.info("====================================")

        return state