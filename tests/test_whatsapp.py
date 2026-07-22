from app.communication.whatsapp.simulator import WhatsAppSimulator
from app.services.communication_service import CommunicationService


def main():
    simulator = WhatsAppSimulator()
    service = CommunicationService()

    message = simulator.simulate()

    result = service.receive(message)

    print(result)


if __name__ == "__main__":
    main()