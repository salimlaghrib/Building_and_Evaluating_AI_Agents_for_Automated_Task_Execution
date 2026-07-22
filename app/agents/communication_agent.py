from app.graph.state import AgentState
from app.graph.workflowStatus import WorkflowStatus
from app.logs.logger import logger


class CommunicationAgent:

    def run(self, state: AgentState) -> AgentState:
        order = state["order_message"]

        print("\n=================================")
        print("Communication Agent")
        print("=================================")

        print(f"Source      : {order.source}")

        if order.phone:
            print(f"Téléphone   : {order.phone}")

        if order.email:
            print(f"Email       : {order.email}")

        if order.sender_name:
            print(f"Expéditeur  : {order.sender_name}")

        if order.image_path:
            print("✅ Image reçue")
        else:
            print("❌ Aucune image")

        print("Workflow démarré")
        print("=================================\n")

        #########log
        logger.info("\n=================================")
        logger.info("Communication Agent")
        logger.info("=================================")

        logger.info(f"Source      : {order.source}")

        if order.phone:
            logger.info(f"Téléphone   : {order.phone}")

        if order.email:
            logger.info(f"Email       : {order.email}")

        if order.sender_name:
            logger.info(f"Expéditeur  : {order.sender_name}")

        if order.image_path:
            logger.info("✅ Image reçue")
        else:
            logger.info("❌ Aucune image")

        logger.info("Workflow démarré")
        logger.info("=================================\n")


        # Mise à jour du statut
        state["status"] = WorkflowStatus.RECEIVED

        state["current_agent"] = "CommunicationAgent"

        return state