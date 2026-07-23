from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from app.communication.gmail.simulator import GmailSimulator
from app.communication.whatsapp.simulator import WhatsAppSimulator
from app.config import BASE_URL, ENV, GEMINI_API_KEY, MODEL_NAME, MODEL_PROVIDER
from app.graph.workflow import run_health_workflow
from app.services.communication_service import CommunicationService
from app.communication.whatsapp.webhook import router as whatsapp_router

app = FastAPI(title="Multi-Agent Order Automation")
communication_service = CommunicationService()

##Whastsapp
app.include_router(whatsapp_router) 

@app.get("/")
async def health_check():
    return {
        "status": "running",
        "health": "/health",
        "simulate_whatsapp": "/simulate/whatsapp",
        "simulate_gmail": "/simulate/gmail",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "env": ENV,
        "platform_base_url": BASE_URL,
        "gemini_configured": bool(GEMINI_API_KEY),
        "model_provider": MODEL_PROVIDER,
        "model_name": MODEL_NAME,
        "workflow": run_health_workflow(),
    }


@app.post("/simulate/whatsapp")
async def simulate_whatsapp():
    message = WhatsAppSimulator().simulate()
    result = communication_service.receive(message)
    return jsonable_encoder(result)


@app.post("/simulate/gmail")
async def simulate_gmail():
    message = GmailSimulator().simulate()
    result = communication_service.receive(message)
    return jsonable_encoder(result)