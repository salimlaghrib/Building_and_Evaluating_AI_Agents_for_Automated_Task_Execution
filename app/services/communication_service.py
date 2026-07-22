from app.graph.state import AgentState
from app.graph.workflowStatus import WorkflowStatus
from app.models.order_message import OrderMessage
from app.graph.workflow import graph


class CommunicationService:

    def receive(self, order_message: OrderMessage):

        # Vérifier la présence de l'image
        if not order_message.image_path:
            raise ValueError("Aucune image reçue.")

        # Vérifier téléphone ou email
        if not order_message.phone and not order_message.email:
            raise ValueError("Le téléphone ou l'email est obligatoire.")

        # Vérifier le texte
        if not order_message.message_text:
            raise ValueError("Le message est vide.")

        # Construire l'état initial du workflow
        state: AgentState = {
            "order_message": order_message,
            "status":  WorkflowStatus.RECEIVED,
            "extracted_data": {},
            "validation_required": False,
            "errors": []
        }

        # Lancer le workflow LangGraph
        result = graph.invoke(state)

        return result