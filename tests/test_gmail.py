from app.communication.gmail.simulator import GmailSimulator
from app.services.communication_service import CommunicationService


def main():
    simulator = GmailSimulator()
    service = CommunicationService()

    message = simulator.simulate()

    result = service.receive(message)

    print(result)


if __name__ == "__main__":
    main()