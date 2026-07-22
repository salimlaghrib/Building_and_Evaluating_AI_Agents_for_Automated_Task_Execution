import json

from app.graph.state import AgentState
from app.graph.workflowStatus import WorkflowStatus
from app.services.vision_service import VisionService
from app.logs.logger import logger


class MultimodalAIAgent:

    def __init__(self):
        self.vision_service = VisionService()

    def run(self, state: AgentState) -> AgentState:

        print("\n====================================")
        print("Multimodal AI Agent")
        print("====================================")

        order_message = state["order_message"]
        
        print(f"Image : {order_message.image_path}")
        print("Image analysée")
        print("Vision Model : GPT-4.1")
        print()
        state["current_agent"] = "MultimodalAIAgent"
    
        try:
            extracted_order = self.vision_service.analyze(
                order_message.image_path
            )

            state["extracted_order"] = extracted_order
            state["status"] = WorkflowStatus.IMAGE_ANALYZED
        except FileNotFoundError:

            state["errors"].append(
                "Image inexistante."
            )

            state["status"] = WorkflowStatus.FAILED
            return state
        except json.JSONDecodeError:

            state["errors"].append(
                "Le modèle Vision n'a pas retourné un JSON valide."
            )

            state["status"] = WorkflowStatus.FAILED
            return state
        except Exception as e:

            state["errors"].append(str(e))

            state["status"] = WorkflowStatus.FAILED
            return state
        print("Dimensions détectées")
        print("--------------------")
        print(f"Client      : {order_message.sender_name}")
           
        print(f"Longueur    : {extracted_order.length} cm")
        print(f"Largeur     : {extracted_order.width} cm")
        print(f"Hauteur     : {extracted_order.height} cm")
        print(f"Quantité    : {extracted_order.quantity}")
        print(f"Confiance   : {extracted_order.confidence}")

        if extracted_order.observations:
            print(f"Observations: {extracted_order.observations}")

        print()
        print("Analyse terminée")
        logger.info("====================================\n")    
#log
        logger.info("Dimensions détectées")
        logger.info("--------------------")
        logger.info(f"Client      : {extracted_order.client_name}")
        logger.info(f"Produit     : {extracted_order.product}")
        logger.info(f"Longueur    : {extracted_order.length} cm")
        logger.info(f"Largeur     : {extracted_order.width} cm")
        logger.info(f"Hauteur     : {extracted_order.height} cm")
        logger.info(f"Quantité    : {extracted_order.quantity}")
        logger.info(f"Confiance   : {extracted_order.confidence}")

        if extracted_order.observations:
            logger.info(f"Observations: {extracted_order.observations}")

        logger.info("\n")
        logger.info("Analyse terminée")
        logger.info("====================================\n")

        return state